"""Copy only website files into the Pages artifact (never the local preview tools)."""
from pathlib import Path
import shutil

BASE = Path(__file__).resolve().parents[1]
DEST = BASE / ".site"
if DEST.exists():
    # This helper owns only this fixed directory inside the project.
    if DEST.is_symlink() or DEST.resolve() != BASE.resolve() / ".site":
        raise ValueError("Refusing to clear an unexpected output directory")
    shutil.rmtree(DEST)
DEST.mkdir()
for name in ("index.html", "404.html", "favicon.ico", ".nojekyll"):
    shutil.copy2(BASE / name, DEST / name)
for name in ("about", "note", "music", "gallery", "publication", "assets", "files"):
    shutil.copytree(BASE / name, DEST / name, ignore=shutil.ignore_patterns(".*"))
print("Packaged static website in .site/")
