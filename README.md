# Manus Skills

A collection of reusable AI agent skills and standalone CLI tools. Each skill is designed to work with **Manus**, and also ships as an independent Python CLI tool that runs in any environment — **Claude Code**, **Qodo**, **Cursor**, **Windsurf**, or plain terminal.

## Skills

| Skill | Description | Install |
|---|---|---|
| [pdf-watermark-remover](./pdf-watermark-remover/) | Remove tiling-pattern and semi-transparent text watermarks from PDF files | `pip install pymupdf` |

## Quick Start

```bash
# Clone the repo
git clone https://github.com/yuanqi99/manus-skills.git
cd manus-skills

# Use any skill directly
cd pdf-watermark-remover
pip install -e .
pdf-watermark-remover input.pdf output.pdf
```

## Usage in AI Coding Tools

### Claude Code / Qodo / Cursor / Windsurf

Each skill can be used as a standalone CLI tool. Just clone this repo into your project and run:

```bash
# Direct script execution (no install needed)
python pdf-watermark-remover/pdf_watermark_remover/cli.py input.pdf output.pdf

# Or install as CLI tool
cd pdf-watermark-remover && pip install -e .
pdf-watermark-remover input.pdf output.pdf
```

### Manus Platform

Skills are automatically detected when placed in `/home/ubuntu/skills/`. Copy the skill directory:

```bash
cp -r pdf-watermark-remover /home/ubuntu/skills/pdf-watermark-remover
```

## Project Structure

```
manus-skills/
├── README.md                          # This file
├── pdf-watermark-remover/             # Skill: PDF Watermark Remover
│   ├── README.md                      # Skill documentation
│   ├── SKILL.md                       # Manus skill metadata
│   ├── pyproject.toml                 # Python package config
│   ├── pdf_watermark_remover/         # Python package
│   │   ├── __init__.py
│   │   ├── remover.py                 # Core logic
│   │   └── cli.py                     # CLI entry point
│   └── tests/
│       └── test_remover.py
└── ...                                # More skills to come
```

## Contributing

To add a new skill:

1. Create a new directory under the repo root
2. Include a `SKILL.md` (for Manus) and `README.md` (for humans)
3. Include a `pyproject.toml` if the skill is a Python CLI tool
4. Submit a PR

## License

MIT License
