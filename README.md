# Manus Skills

[中文说明](./README_CN.md) | English

A collection of reusable AI agent skills and standalone CLI tools. Each skill is designed to work seamlessly with **Manus**, and also ships as an independent Python CLI tool that runs in any environment — **Claude Code**, **Qodo**, **Cursor**, **Windsurf**, or plain terminal.

## Skills

| Skill | Description | Status |
|---|---|---|
| [pdf-watermark-remover](./pdf-watermark-remover/) | Remove tiling-pattern and semi-transparent text watermarks from PDF files | Stable |

## Quick Start

```bash
# Clone the repo
git clone https://github.com/yuanqi99/manus-skills.git
cd manus-skills

# Use any skill — example: PDF Watermark Remover
cd pdf-watermark-remover
pip install -e .
pdf-watermark-remover input.pdf output.pdf
```

## Multi-Environment Support

Every skill in this repo is designed to be **universal** — use it wherever you work.

### Claude Code / Qodo / Cursor / Windsurf

Clone the repo into your workspace and use any skill as a CLI tool:

```bash
git clone https://github.com/yuanqi99/manus-skills.git
cd manus-skills/pdf-watermark-remover
pip install -e .
pdf-watermark-remover input.pdf output.pdf
```

Or run the script directly without installation:

```bash
python pdf-watermark-remover/pdf_watermark_remover/cli.py input.pdf output.pdf
```

### Manus Platform

Skills are automatically detected when placed in `/home/ubuntu/skills/`. Simply copy:

```bash
cp -r pdf-watermark-remover /home/ubuntu/skills/pdf-watermark-remover
```

### Any Terminal / CI Pipeline

Install as a standard Python package:

```bash
cd pdf-watermark-remover && pip install .
pdf-watermark-remover input.pdf output.pdf
```

## Project Structure

```
manus-skills/
├── README.md                          # English README
├── README_CN.md                       # 中文 README
├── LICENSE                            # MIT License
├── .gitignore
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

[MIT License](./LICENSE)
