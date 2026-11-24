"""Check every XHTML document in the generated EPUB for XML well-formedness."""
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile

with ZipFile(Path(__file__).resolve().parents[1] / "Spanish reference.epub") as epub:
    documents = [name for name in epub.namelist() if name.endswith(".xhtml")]
    if not documents:
        raise SystemExit("EPUB contains no XHTML documents")
    for name in documents:
        ElementTree.fromstring(epub.read(name))
print(f"Checked {len(documents)} XHTML documents")
