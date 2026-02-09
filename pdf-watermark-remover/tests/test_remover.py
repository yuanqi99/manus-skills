"""Basic tests for pdf_watermark_remover."""

import os
import tempfile
import pytest

try:
    import fitz
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False


@pytest.mark.skipif(not HAS_PYMUPDF, reason="PyMuPDF not installed")
class TestDetectWatermarkType:
    def test_empty_pdf(self):
        """A blank PDF should have no watermarks."""
        from pdf_watermark_remover import detect_watermark_type

        doc = fitz.open()
        doc.new_page()
        types = detect_watermark_type(doc)
        assert types == set()
        doc.close()


@pytest.mark.skipif(not HAS_PYMUPDF, reason="PyMuPDF not installed")
class TestRemoveWatermark:
    def test_blank_pdf_passthrough(self):
        """A blank PDF should pass through without error."""
        from pdf_watermark_remover import remove_watermark

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "input.pdf")
            output_path = os.path.join(tmpdir, "output.pdf")

            doc = fitz.open()
            doc.new_page()
            doc.save(input_path)
            doc.close()

            info = remove_watermark(input_path, output_path, verbose=False)
            assert info["pages"] == 1
            assert os.path.exists(output_path)
