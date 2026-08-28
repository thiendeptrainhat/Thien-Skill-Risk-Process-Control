"""Read-only PDF structure and native-text inspection; no active-content execution."""
import hashlib
import json
import sys
from pathlib import Path

import pypdf
from pypdf.generic import ArrayObject, DictionaryObject, IndirectObject

pdf_path = Path(sys.argv[1]).resolve(strict=True)
source_bytes = pdf_path.read_bytes()
reader = pypdf.PdfReader(pdf_path, strict=True)
target_keys = {
    "/JS", "/JavaScript", "/AA", "/OpenAction", "/Launch", "/EmbeddedFiles",
    "/URI", "/XFA", "/AcroForm", "/Sig", "/RichMedia", "/Encrypt",
}
seen = set()
hits = []

def visit(obj, locator):
    if isinstance(obj, IndirectObject):
        identity = (obj.idnum, obj.generation)
        if identity in seen:
            return
        seen.add(identity)
        obj = obj.get_object()
    if isinstance(obj, DictionaryObject):
        for key, value in obj.items():
            if key in target_keys:
                hits.append({"locator": locator + str(key), "key": str(key), "value_type": type(value).__name__})
            if str(value) in target_keys and not isinstance(value, (DictionaryObject, ArrayObject, IndirectObject)):
                hits.append({"locator": locator + str(key), "name_value": str(value)})
            visit(value, locator + str(key) + "/")
    elif isinstance(obj, ArrayObject):
        for i, value in enumerate(obj):
            visit(value, locator + str(i) + "/")

visit(reader.trailer, "trailer/")
pages = []
for n, page in enumerate(reader.pages, 1):
    raw_text = page.extract_text()
    xobjects = page.get("/Resources", {}).get("/XObject", {})
    if hasattr(xobjects, "get_object"):
        xobjects = xobjects.get_object()
    images = []
    for key, obj in xobjects.items():
        image = obj.get_object()
        if image.get("/Subtype") == "/Image":
            images.append({"name": str(key), "width": image.get("/Width"), "height": image.get("/Height"), "filter": str(image.get("/Filter")), "bits_per_component": image.get("/BitsPerComponent")})
    pages.append({"page": n, "media_box_points": [float(x) for x in page.mediabox], "rotation": page.get("/Rotate", 0), "raw_native_text": raw_text, "native_text_char_count": len(raw_text or ""), "images": images})

print(json.dumps({"reader": "pypdf", "reader_version": pypdf.__version__, "mode": "LOCAL_STATIC_READ_ONLY", "source_path": str(pdf_path), "size_bytes": len(source_bytes), "sha256": hashlib.sha256(source_bytes).hexdigest(), "is_encrypted": reader.is_encrypted, "metadata": dict(reader.metadata or {}), "page_count": len(reader.pages), "active_content_key_hits": hits, "visited_indirect_objects": len(seen), "limitations": ["Static parsed-key inspection, not malware scanning or authentication; no action executed.", "Does not identify page-rendered warnings without visual inspection."], "pages": pages}, ensure_ascii=False, indent=2))
