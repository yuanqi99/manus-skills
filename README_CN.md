# Manus Skills

中文说明 | [English](./README.md)

一套可复用的 AI 智能体技能和独立命令行工具集合。每个技能既可在 **Manus** 平台上自动识别使用，也可以作为独立的 Python CLI 工具在任何环境中运行 —— **Claude Code**、**Qodo**、**Cursor**、**Windsurf** 或普通终端均可。

## 技能列表

| 技能 | 说明 | 状态 |
|---|---|---|
| [pdf-watermark-remover](./pdf-watermark-remover/) | 去除 PDF 文件中的平铺图案水印和半透明文字水印 | 稳定 |
| [claude-code-extensions](https://github.com/yuanqi99/claude-code-extensions) | 专门针对 Claude Code 的记忆增强插件与技能集合 | 持续更新 |

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/yuanqi99/manus-skills.git
cd manus-skills

# 使用任意技能 —— 以 PDF 去水印为例
cd pdf-watermark-remover
pip install -e .
pdf-watermark-remover input.pdf output.pdf
```

## 多环境支持

本仓库中的每个技能都设计为**通用工具**，在任何环境下都能使用。

### Claude Code / Qodo / Cursor / Windsurf

将仓库克隆到工作区，直接作为 CLI 工具使用：

```bash
git clone https://github.com/yuanqi99/manus-skills.git
cd manus-skills/pdf-watermark-remover
pip install -e .
pdf-watermark-remover input.pdf output.pdf
```

也可以不安装，直接运行脚本：

```bash
python pdf-watermark-remover/pdf_watermark_remover/cli.py input.pdf output.pdf
```

### Manus 平台

将技能目录复制到 `/home/ubuntu/skills/` 即可自动识别：

```bash
cp -r pdf-watermark-remover /home/ubuntu/skills/pdf-watermark-remover
```

### 任意终端 / CI 流水线

作为标准 Python 包安装后全局使用：

```bash
cd pdf-watermark-remover && pip install .
pdf-watermark-remover input.pdf output.pdf
```

## 项目结构

```
manus-skills/
├── README.md                          # 英文说明
├── README_CN.md                       # 中文说明
├── LICENSE                            # MIT 开源协议
├── .gitignore
├── pdf-watermark-remover/             # 技能：PDF 去水印
│   ├── README.md                      # 技能文档
│   ├── SKILL.md                       # Manus 平台元数据
│   ├── pyproject.toml                 # Python 包配置
│   ├── pdf_watermark_remover/         # Python 源码包
│   │   ├── __init__.py
│   │   ├── remover.py                 # 核心逻辑
│   │   └── cli.py                     # 命令行入口
│   └── tests/
│       └── test_remover.py
└── ...                                # 更多技能持续添加中
```

## 贡献指南

添加新技能的步骤：

1. 在仓库根目录下创建新的技能目录
2. 包含 `SKILL.md`（Manus 平台用）和 `README.md`（人类阅读用）
3. 如果是 Python CLI 工具，包含 `pyproject.toml`
4. 提交 PR

## 开源协议

[MIT License](./LICENSE)
