---
name: pdf-watermark-remover
description: Remove watermarks from PDF files. Use when users request watermark removal, cleaning watermarks, or de-watermarking PDF documents. Supports tiling pattern watermarks (repeated image/text tiles) and semi-transparent text overlay watermarks.
---

# PDF Watermark Remover

Remove watermarks from PDF files using PyMuPDF. Supports tiling pattern watermarks (most common in enterprise document systems) and semi-transparent text overlays.

## Prerequisites

Ensure PyMuPDF is installed:

```bash
sudo pip3 install pymupdf
```

## Usage

Run the bundled script:

```bash
python3 pdf_watermark_remover/cli.py <input.pdf> <output.pdf> [--mode auto|pattern|text|both]
```

Or if installed via pip:

```bash
pdf-watermark-remover <input.pdf> <output.pdf> [--mode auto|pattern|text|both]
```

### Modes

| Mode | Description |
|---|---|
| `auto` | Detect watermark type automatically and remove (default) |
| `pattern` | Remove only tiling pattern watermarks (repeated tiles covering pages) |
| `text` | Remove only semi-transparent text watermarks |
| `both` | Force remove both types |

### Typical Workflow

1. Receive PDF file from user
2. Run script with `--mode auto` (default)
3. Verify output by viewing 2-3 pages of the result PDF
4. If watermarks remain, retry with `--mode both` or investigate manually
5. Deliver the cleaned PDF to the user

## How It Works

- **Pattern watermarks**: Detected by `/Pattern CS` operators in content streams. Removed by excising `q...Q` graphics state blocks containing pattern fill operations.
- **Text watermarks**: Detected by ExtGState objects with fill opacity (`/ca`) less than 1.0.

## Limitations

- Cannot remove watermarks baked into rasterized images (scanned PDFs)
- Cannot remove watermarks embedded as part of the actual page content (same opacity as normal text)
- For encrypted/password-protected PDFs, decryption must be done first
