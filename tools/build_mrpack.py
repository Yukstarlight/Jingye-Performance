import json, os, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "pack", "modrinth.index.json")
CONFIG = os.path.join(ROOT, "config")
DIST = os.path.join(ROOT, "dist")

index = json.load(open(INDEX, encoding="utf-8"))
out = os.path.join(DIST, f"Jingye-Performance-{index['versionId']}.mrpack")
os.makedirs(DIST, exist_ok=True)

with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    z.write(INDEX, "modrinth.index.json")
    for dirpath, dirnames, filenames in os.walk(CONFIG):
        dirnames[:] = sorted(d for d in dirnames if d != "__pycache__")
        for name in sorted(filenames):
            src = os.path.join(dirpath, name)
            rel = os.path.relpath(src, ROOT).replace(os.sep, "/")
            z.write(src, "overrides/" + rel)
    entries = len(z.namelist())

print(f"built {out} ({os.path.getsize(out)} bytes, {entries} entries)")
