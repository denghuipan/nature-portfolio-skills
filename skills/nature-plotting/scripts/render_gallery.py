"""Render every template in ../templates with its mock data into ../gallery as PNG previews.

    python scripts/render_gallery.py            # all templates
    python scripts/render_gallery.py L0 M03     # only names starting with these prefixes
    python scripts/render_gallery.py --dpi 300  # sharper previews

Each template runs in its own process (exactly as a user would run it), with NATURE_GALLERY set so that
nature_charts.export() writes one PNG instead of PNG + PDF. Prints the text-size audit of every figure.
"""
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TEMPLATES = ROOT / "templates"
GALLERY = ROOT / "gallery"


def main(argv):
    dpi = "200"
    if "--dpi" in argv:
        i = argv.index("--dpi"); dpi = argv[i + 1]; argv = argv[:i] + argv[i + 2:]
    prefixes = argv or [""]
    files = sorted(p for p in TEMPLATES.glob("*.py") if not p.name.startswith("_")
                   and any(p.stem.startswith(x) for x in prefixes))
    env = dict(os.environ, NATURE_GALLERY=str(GALLERY), NATURE_GALLERY_DPI=dpi, MPLBACKEND="Agg",
               PYTHONWARNINGS="ignore")
    failed = []
    for f in files:
        t0 = time.time()
        r = subprocess.run([sys.executable, str(f)], env=env, capture_output=True, text=True, cwd=ROOT)
        notes = [l for l in (r.stdout + r.stderr).splitlines()
                 if l.startswith(("[export]", "[layout]")) or "Error" in l or "Traceback" in l]
        status = "ok " if r.returncode == 0 else "ERR"
        print(f"{status} {f.stem:28s} {time.time() - t0:5.1f}s  " + " | ".join(notes)[:300])
        if r.returncode:
            failed.append(f.stem)
            print(r.stderr[-2500:])
    print(f"\n{len(files) - len(failed)}/{len(files)} rendered into {GALLERY}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
