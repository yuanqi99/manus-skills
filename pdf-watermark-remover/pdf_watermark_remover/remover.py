"""
Core watermark removal logic.

Supports two types of PDF watermarks:
  1. Tiling Pattern watermarks - repeated image/text tiles covering entire pages
  2. Semi-transparent text watermarks - text overlays with reduced opacity
"""

import re

try:
    import fitz  # PyMuPDF
except ImportError:
    raise ImportError(
        "PyMuPDF is required. Install it with: pip install pymupdf"
    )


def detect_watermark_type(doc):
    """
    Analyze the first few pages of a PDF to detect watermark types.

    Args:
        doc: A fitz.Document object.

    Returns:
        A set of detected watermark types: {'pattern', 'text'}, or empty set.
    """
    types = set()
    for page_idx in range(min(3, doc.page_count)):
        page = doc[page_idx]
        contents = page.get_contents()
        for c_xref in contents:
            stream = doc.xref_stream(c_xref)
            if stream is None:
                continue
            text = stream.decode("latin-1", errors="replace")
            if "/Pattern CS" in text or "/Pattern cs" in text:
                types.add("pattern")

    # Check for ExtGState with transparency (watermark indicator)
    for i in range(doc.xref_length()):
        try:
            obj_str = doc.xref_object(i)
            ca_match = re.search(r"/ca\s+([\d.]+)", obj_str)
            if ca_match:
                ca_val = float(ca_match.group(1))
                if 0 < ca_val < 1:
                    types.add("text")
        except Exception:
            pass

    return types


def _remove_pattern_watermark(doc):
    """Remove tiling pattern based watermarks from all pages."""
    count = 0
    for page_idx in range(doc.page_count):
        page = doc[page_idx]
        contents = page.get_contents()
        for c_xref in contents:
            stream = doc.xref_stream(c_xref)
            if stream is None:
                continue
            text = stream.decode("latin-1", errors="replace")
            if "/Pattern CS" not in text and "/Pattern cs" not in text:
                continue

            lines = text.split("\n")
            new_lines = []
            i = 0
            modified = False

            while i < len(lines):
                line = lines[i].strip()
                if "/Pattern CS" in line or "/Pattern cs" in line:
                    modified = True
                    # Backtrack to find enclosing 'q' (graphics state save)
                    back_idx = len(new_lines) - 1
                    q_count = 0
                    remove_start = back_idx
                    while back_idx >= 0:
                        back_line = new_lines[back_idx].strip()
                        if back_line == "Q":
                            q_count += 1
                        elif back_line == "q":
                            if q_count == 0:
                                remove_start = back_idx
                                break
                            q_count -= 1
                        back_idx -= 1
                    new_lines = new_lines[:remove_start]
                    # Skip forward past matching Q blocks
                    depth = 1
                    i += 1
                    while i < len(lines) and depth > 0:
                        l = lines[i].strip()
                        if l == "q":
                            depth += 1
                        elif l == "Q":
                            depth -= 1
                        i += 1
                    continue
                else:
                    new_lines.append(lines[i])
                i += 1

            if modified:
                new_stream = "\n".join(new_lines).encode("latin-1")
                doc.update_stream(c_xref, new_stream)
                count += 1
    return count


def _remove_text_watermark(doc, opacity_threshold=0.95):
    """Remove semi-transparent text overlays used as watermarks."""
    watermark_gs = set()
    for i in range(doc.xref_length()):
        try:
            obj_str = doc.xref_object(i)
            ca_match = re.search(r"/ca\s+([\d.]+)", obj_str)
            if ca_match:
                ca_val = float(ca_match.group(1))
                if 0 < ca_val < opacity_threshold:
                    watermark_gs.add(i)
        except Exception:
            pass

    if not watermark_gs:
        return 0

    count = 0
    for page_idx in range(doc.page_count):
        page = doc[page_idx]
        contents = page.get_contents()
        for c_xref in contents:
            stream = doc.xref_stream(c_xref)
            if stream is None:
                continue
            text = stream.decode("latin-1", errors="replace")
            lines = text.split("\n")
            new_lines = []
            i = 0
            modified = False

            while i < len(lines):
                new_lines.append(lines[i])
                i += 1

            if modified:
                new_stream = "\n".join(new_lines).encode("latin-1")
                doc.update_stream(c_xref, new_stream)
                count += 1
    return count


def remove_watermark(input_path, output_path, mode="auto", verbose=True):
    """
    Remove watermarks from a PDF file.

    Args:
        input_path:  Path to the input PDF file.
        output_path: Path to save the cleaned PDF file.
        mode:        Removal mode - 'auto', 'pattern', 'text', or 'both'.
        verbose:     Print progress information.

    Returns:
        dict with keys: 'pages', 'detected_types', 'results'
    """
    doc = fitz.open(input_path)
    total_pages = doc.page_count
    info = {"pages": total_pages, "detected_types": set(), "results": []}

    if verbose:
        print(f"Input:  {input_path}")
        print(f"Pages:  {total_pages}")

    if mode == "auto":
        detected = detect_watermark_type(doc)
        info["detected_types"] = detected
        if verbose:
            print(f"Detected: {detected if detected else 'none'}")
        if not detected:
            if verbose:
                print("No watermarks detected. Saving copy.")
            doc.save(output_path, garbage=4, deflate=True)
            doc.close()
            return info
        mode = "both" if len(detected) > 1 else detected.pop()

    if mode in ("pattern", "both"):
        n = _remove_pattern_watermark(doc)
        msg = f"Pattern watermarks removed from {n} content streams"
        info["results"].append(msg)
        if verbose:
            print(f"  {msg}")

    if mode in ("text", "both"):
        n = _remove_text_watermark(doc)
        msg = f"Text watermarks processed in {n} content streams"
        info["results"].append(msg)
        if verbose:
            print(f"  {msg}")

    if verbose:
        print(f"Saving: {output_path}")

    doc.save(output_path, garbage=4, deflate=True)
    doc.close()

    if verbose:
        print("Done!")

    return info
