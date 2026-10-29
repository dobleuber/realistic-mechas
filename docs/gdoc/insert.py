"""Inserta en el Google Doc los bloques de content.py que todavía no están, sin tocar el resto.

  python insert.py text DOC.json      -> lote 1: inserta los párrafos nuevos (de abajo arriba) y aplica
                                          los reemplazos de texto de RENOMBRAR
  python insert.py styles DOC.json    -> lote 2: estilos de los párrafos nuevos
  python build.py objects DOC.json    -> lote 3: tablas e imágenes de los marcadores

Un párrafo nuevo se inserta al final del párrafo de content.py que lo precede y que ya está en el documento.
"""
import json
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from build import FONT, GRAY, LINK, TAB, load, paragraphs, rng  # noqa: E402

# reemplazos de texto que acompañan a la inserción (numeración de sección, tablas y figuras)
RENOMBRAR = [
    ("10. Conclusión General", "11. Conclusión General"),
    ("se desprenden cuatro conclusiones", "se desprenden cinco conclusiones"),
    ("La Tabla 5 resume", "La Tabla 6 resume"),
    ("Tabla 5: Altura a la que", "Tabla 6: Altura a la que"),
    ("Figura 6: Altura máxima de un mecha", "Figura 7: Altura máxima de un mecha"),
    ("parámetros (sección 10)", "parámetros (sección 11)"),
]


# marcadores de tablas e imágenes que se añaden ahora
NUEVOS = {"[[TABLA:elefante]]", "[[IMG:elefante_mecha.png]]"}


def doc_paragraphs(body):
    out = []
    for el in body:
        p = el.get("paragraph")
        if p is not None:
            txt = "".join(e.get("textRun", {}).get("content", "") for e in p["elements"]).rstrip("\n")
            out.append((el["startIndex"], el["endIndex"], txt))
    return out


def renamed(t):
    for a, b in RENOMBRAR:
        t = t.replace(b, a)
    return t


def text_batch(doc_json):
    rev, body = load(doc_json)
    dps = doc_paragraphs(body)
    existing = {}
    for s, e, t in dps:
        existing.setdefault(t, (s, e))
    paras = paragraphs()
    inserts = []          # (índice, texto)

    def present(k, t):
        # las tablas e imágenes que ya están no tienen texto en el documento; solo son nuevas las de NUEVOS
        if k == "ph":
            return t not in NUEVOS
        return t in existing or renamed(t) in existing
    i = 0
    while i < len(paras):
        k, t, _ = paras[i]
        if present(k, t):
            i += 1
            continue
        # bloque de párrafos nuevos consecutivos
        j = i
        while j < len(paras) and not present(paras[j][0], paras[j][1]):
            j += 1
        prev = paras[i - 1][1]
        anchor = existing.get(prev) or existing.get(renamed(prev))
        if anchor is None:
            raise SystemExit(f"no encuentro el párrafo anterior a: {t[:80]}")
        inserts.append((anchor[1] - 1, "\n" + "\n".join(p[1] for p in paras[i:j])))
        i = j
    reqs = [{"insertText": {"location": {"index": idx, "tabId": TAB}, "text": txt}}
            for idx, txt in sorted(inserts, reverse=True)]
    reqs += [{"replaceAllText": {"containsText": {"text": a, "matchCase": True}, "replaceText": b,
                                 "tabsCriteria": {"tabIds": [TAB]}}} for a, b in RENOMBRAR]
    for idx, txt in sorted(inserts):
        print(f"inserción en {idx}: {txt.count(chr(10))} párrafos, empieza «{txt[1:60]}»", file=sys.stderr)
    return {"requests": reqs, "writeControl": {"requiredRevisionId": rev}}


def styles_batch(doc_json, new_texts):
    """Estilos de los párrafos cuyo texto está en new_texts (los insertados en el lote 1)."""
    rev, body = load(doc_json)
    dps = doc_paragraphs(body)
    paras = {t: (k, sp) for k, t, sp in paragraphs()}
    reqs = []
    for s, e, t in dps:
        if t not in new_texts:
            continue
        k, spans = paras[t]
        listed = k in ("bullet", "src")
        if not listed:
            reqs.append({"updateParagraphStyle": {"range": rng(s, e), "paragraphStyle": {
                "namedStyleType": "NORMAL_TEXT", "spaceAbove": {"magnitude": 0, "unit": "PT"},
                "spaceBelow": {"magnitude": 12, "unit": "PT"}, "lineSpacing": 115,
                "indentStart": {"magnitude": 0, "unit": "PT"}, "indentFirstLine": {"magnitude": 0, "unit": "PT"},
                "alignment": "START", "keepWithNext": False, "keepLinesTogether": False},
                "fields": "namedStyleType,spaceAbove,spaceBelow,lineSpacing,indentStart,indentFirstLine,alignment,"
                          "keepWithNext,keepLinesTogether"}})
        if e - 1 > s:
            ts = {"weightedFontFamily": FONT, "foregroundColor": GRAY}
            if k == "src":
                ts["fontSize"] = {"magnitude": 12, "unit": "PT"}
            reqs.append({"updateTextStyle": {"range": rng(s, e - 1), "textStyle": ts,
                                             "fields": "weightedFontFamily,foregroundColor,fontSize,bold,italic,underline,"
                                                       "link,strikethrough,baselineOffset,smallCaps,backgroundColor"}})
        if k in ("h2", "h3", "h4"):
            reqs.append({"updateParagraphStyle": {"range": rng(s, e), "paragraphStyle": {
                "namedStyleType": {"h2": "HEADING_2", "h3": "HEADING_3", "h4": "HEADING_4"}[k],
                "spaceBelow": {"magnitude": 6, "unit": "PT"}, "keepWithNext": True, "keepLinesTogether": True},
                "fields": "namedStyleType,spaceBelow,keepWithNext,keepLinesTogether"}})
        elif listed:
            reqs.append({"updateParagraphStyle": {"range": rng(s, e), "paragraphStyle": {
                "spaceBelow": {"magnitude": 6, "unit": "PT"}}, "fields": "spaceBelow"}})
        elif k == "cap":
            reqs.append({"updateParagraphStyle": {"range": rng(s, e), "paragraphStyle": {
                "spaceAbove": {"magnitude": 12, "unit": "PT"}, "spaceBelow": {"magnitude": 12, "unit": "PT"}},
                "fields": "spaceAbove,spaceBelow"}})
            reqs.append({"updateTextStyle": {"range": rng(s, e - 1), "textStyle": {"italic": True}, "fields": "italic"}})
        for a, b_, what in spans:
            r = rng(s + a, s + b_)
            if what == "bold":
                reqs.append({"updateTextStyle": {"range": r, "textStyle": {"bold": True}, "fields": "bold"}})
            elif what == "sup":
                reqs.append({"updateTextStyle": {"range": r, "textStyle": {"baselineOffset": "SUPERSCRIPT"},
                                                 "fields": "baselineOffset"}})
            else:
                reqs.append({"updateTextStyle": {"range": r, "textStyle": {"link": {"url": what}, "underline": True,
                                                                           "foregroundColor": LINK},
                                                 "fields": "link,underline,foregroundColor"}})
    return {"requests": reqs, "writeControl": {"requiredRevisionId": rev}}


def new_paragraph_texts(old_doc_json):
    """Textos de content.py que no estaban en el documento antes del lote 1."""
    _, body = load(old_doc_json)
    old = {t for _, _, t in doc_paragraphs(body)}
    return {t for _, t, _ in paragraphs() if t not in old and renamed(t) not in old}


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "text":
        print(json.dumps(text_batch(sys.argv[2]), ensure_ascii=False))
    elif cmd == "styles":
        # styles NUEVO.json ANTERIOR.json
        print(json.dumps(styles_batch(sys.argv[2], new_paragraph_texts(sys.argv[3])), ensure_ascii=False))
