"""Command-line interface for PDF Watermark Remover."""

import argparse
import sys
from .remover import remove_watermark


def main():
    parser = argparse.ArgumentParser(
        prog="pdf-watermark-remover",
        description="Remove watermarks from PDF files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  pdf-watermark-remover input.pdf output.pdf
  pdf-watermark-remover input.pdf output.pdf --mode pattern
  pdf-watermark-remover input.pdf cleaned.pdf --mode both --quiet

Modes:
  auto     Detect watermark type and remove automatically (default)
  pattern  Remove tiling pattern watermarks (repeated tiles)
  text     Remove semi-transparent text watermarks
  both     Force remove both types
""",
    )
    parser.add_argument("input", help="Input PDF file path")
    parser.add_argument("output", help="Output PDF file path")
    parser.add_argument(
        "--mode",
        choices=["auto", "pattern", "text", "both"],
        default="auto",
        help="Watermark removal mode (default: auto)",
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress output messages",
    )

    args = parser.parse_args()

    try:
        remove_watermark(
            args.input,
            args.output,
            mode=args.mode,
            verbose=not args.quiet,
        )
    except FileNotFoundError:
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
