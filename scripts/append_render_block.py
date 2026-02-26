import sys
from pathlib import Path


BLOCK = (
    "\n\n"
    "def Scope \"Render\"\n"
    "{\n"
    "    def RenderProduct \"Product\"\n"
    "    {\n"
    "        rel camera = </Camera>\n"
    "        int2 resolution = (1920, 1080)\n"
    "        asset productName = \"Capture.####.png\"\n"
    "    }\n\n"
    "    def RenderSettings \"Settings\"\n"
    "    {\n"
    "        rel products = [</Render/Product>]\n"
    "    }\n"
    "}\n"
)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: append_render_block.py <path_to_usda>")
        return 2
    p = Path(sys.argv[1])
    if not p.exists():
        print(f"ERROR: file not found: {p}")
        return 1
    text = p.read_text(encoding="utf-8", errors="ignore")
    if "RenderProduct" in text:
        print("SKIP: RenderProduct already present")
        return 0
    # Backup then append
    backup = p.with_suffix(p.suffix + ".bak")
    backup.write_text(text, encoding="utf-8")
    p.write_text(text + BLOCK, encoding="utf-8")
    print("OK: Render block appended")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

