# PDF Watermark Remover

Remove tiling-pattern and semi-transparent text watermarks from PDF files.

## Features

- **Auto-detection**: Automatically identifies watermark type and removes it
- **Pattern watermarks**: Removes tiling pattern watermarks (repeated image/text tiles covering pages)
- **Text watermarks**: Removes semi-transparent text overlay watermarks
- **Standalone CLI**: Works as a command-line tool in any environment
- **Python API**: Import and use programmatically in your own scripts
- **Manus Skill**: Drop into Manus `/home/ubuntu/skills/` for automatic integration

## Installation

```bash
# From source
git clone https://github.com/yuanqi99/manus-skills.git
cd manus-skills/pdf-watermark-remover
pip install -e .

# Or just install the dependency and run directly
pip install pymupdf
python pdf_watermark_remover/cli.py input.pdf output.pdf
```

## Usage

### Command Line

```bash
# Auto-detect and remove watermarks (recommended)
pdf-watermark-remover input.pdf output.pdf

# Remove only pattern watermarks
pdf-watermark-remover input.pdf output.pdf --mode pattern

# Remove only text watermarks
pdf-watermark-remover input.pdf output.pdf --mode text

# Force remove both types
pdf-watermark-remover input.pdf output.pdf --mode both

# Quiet mode (no output)
pdf-watermark-remover input.pdf output.pdf --quiet
```

### Python API

```python
from pdf_watermark_remover import remove_watermark, detect_watermark_type
import fitz

# Simple usage
remove_watermark("input.pdf", "output.pdf")

# With options
remove_watermark("input.pdf", "output.pdf", mode="pattern", verbose=False)

# Detect watermark type only
doc = fitz.open("input.pdf")
types = detect_watermark_type(doc)  # Returns {'pattern', 'text'} or subset
doc.close()
```

## Modes

| Mode | Description |
|---|---|
| `auto` | Detect watermark type automatically and remove (default) |
| `pattern` | Remove only tiling pattern watermarks |
| `text` | Remove only semi-transparent text watermarks |
| `both` | Force remove both types |

## How It Works

The tool analyzes PDF content streams at the operator level:

1. **Pattern watermarks** are detected by `/Pattern CS` or `/Pattern cs` operators. These create tiling patterns (XStep/YStep) that fill pages with repeated tiles. The tool removes the entire `q...Q` graphics state block containing the pattern fill.

2. **Text watermarks** are detected by ExtGState objects with fill opacity (`/ca`) less than 1.0. These are semi-transparent text overlays rendered on top of page content.

## Limitations

- Cannot remove watermarks baked into rasterized images (scanned PDFs)
- Cannot remove watermarks with the same opacity as normal text
- Encrypted/password-protected PDFs must be decrypted first

## License

MIT
