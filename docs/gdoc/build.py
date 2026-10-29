"""Peticiones de la API de Docs con las que se reescribió el Google Doc con el contenido corregido.

DOC.json es la salida de documents.get. «objects» usa docs_index.py, el ayudante de índices
de la skill google-workspace de Claude (ruta en SK).

  python build.py text                 -> texto plano completo (para insertText)
  python build.py styles DOC.json      -> lote de estilos (verifica antes que el texto coincide)
  python build.py objects DOC.json     -> lote de tablas e imágenes
  python build.py md                   -> copia en Markdown
"""
import json
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from content import B, RAW  # noqa: E402

TAB = "t.0"
SK = "/root/.claude/skills/synced/bbc03e69-a18b-4fc5-965c-3a1d28d9c489_e05548c1-1a7e-4e03-90f5-a72175d66a4c/google-workspace/scripts"
INLINE = re.compile(r"\*\*(.+?)\*\*|\[([^\]]+)\]\(([^)]+)\)|\^(\d+(?:\.\d+)?|[a-z])")
GRAY = {"color": {"rgbColor": {"red": 0.12156863, "green": 0.12156863, "blue": 0.12156863}}}
LINK = {"color": {"rgbColor": {"red": 0.06666667, "green": 0.33333334, "blue": 0.8}}}
FONT = {"fontFamily": "Google Sans", "weight": 400}


def u16(s):
    return len(s.encode("utf-16-le")) // 2


def parse_inline(s):
    out, spans, pos = "", [], 0
    for m in INLINE.finditer(s):
        out += s[pos:m.start()]
        st = u16(out)
        if m.group(1) is not None:
            out += m.group(1)
            spans.append((st, u16(out), "bold"))
        elif m.group(4) is not None:
            out += m.group(4)
            spans.append((st, u16(out), "sup"))
        else:
            out += m.group(2)
            spans.append((st, u16(out), m.group(3)))
        pos = m.end()
    return out + s[pos:], spans


def paragraphs():
    res = []
    for b in B:
        if b[0] == "table":
            res.append(("ph", f"[[TABLA:{b[1]}]]", []))
        elif b[0] == "img":
            res.append(("ph", f"[[IMG:{b[1]}]]", []))
        else:
            t, sp = parse_inline(b[1])
            res.append((b[0], t, sp))
    return res


def full_text():
    return "\n".join(p[1] for p in paragraphs())


def load(doc_json):
    d = json.load(open(doc_json))
    d = d.get("content", d)
    tab = [t for t in d["tabs"] if t["tabProperties"]["tabId"] == TAB][0]
    return d["revisionId"], tab["documentTab"]["body"]["content"]


def rng(s, e):
    return {"startIndex": s, "endIndex": e, "tabId": TAB}


def styles(doc_json):
    rev, body = load(doc_json)
    dps = []
    for el in body:
        p = el.get("paragraph")
        if p is not None:
            txt = "".join(e.get("textRun", {}).get("content", "") for e in p["elements"])
            dps.append((el["startIndex"], el["endIndex"], txt.rstrip("\n")))
    paras = paragraphs()
    if len(dps) != len(paras):
        raise SystemExit(f"párrafos distintos: doc {len(dps)} / contenido {len(paras)}")
    for (s, e, t), (k, t2, _) in zip(dps, paras):
        if t != t2:
            raise SystemExit(f"texto distinto en {s}:\n doc: {t[:150]}\n esp: {t2[:150]}")
    start, end = dps[0][0], dps[-1][1]
    reqs = [
        {"deleteParagraphBullets": {"range": rng(start, end)}},
        {"updateParagraphStyle": {"range": rng(start, end), "paragraphStyle": {
            "namedStyleType": "NORMAL_TEXT", "spaceAbove": {"magnitude": 0, "unit": "PT"},
            "spaceBelow": {"magnitude": 12, "unit": "PT"}, "lineSpacing": 115,
            "indentStart": {"magnitude": 0, "unit": "PT"}, "indentFirstLine": {"magnitude": 0, "unit": "PT"},
            "alignment": "START", "keepWithNext": False},
            "fields": "namedStyleType,spaceAbove,spaceBelow,lineSpacing,indentStart,indentFirstLine,alignment,keepWithNext"}},
        {"updateTextStyle": {"range": rng(start, end - 1), "textStyle": {"weightedFontFamily": FONT, "foregroundColor": GRAY},
                             "fields": "weightedFontFamily,foregroundColor,fontSize,bold,italic,underline,link,"
                                       "strikethrough,baselineOffset,smallCaps,backgroundColor"}},
    ]
    groups = []
    for (s, e, _), (k, t, spans) in zip(dps, paras):
        if k in ("h1", "h2", "h3", "h4"):
            reqs.append({"updateParagraphStyle": {"range": rng(s, e), "paragraphStyle": {
                "namedStyleType": {"h1": "HEADING_1", "h2": "HEADING_2", "h3": "HEADING_3", "h4": "HEADING_4"}[k],
                "spaceBelow": {"magnitude": 6, "unit": "PT"}, "keepWithNext": True},
                "fields": "namedStyleType,spaceBelow,keepWithNext"}})
        elif k in ("bullet", "src"):
            reqs.append({"updateParagraphStyle": {"range": rng(s, e), "paragraphStyle": {
                "spaceBelow": {"magnitude": 6, "unit": "PT"}}, "fields": "spaceBelow"}})
            if groups and groups[-1][1] == s and groups[-1][2] == k:
                groups[-1][1] = e
            else:
                groups.append([s, e, k])
        elif k == "cap":
            reqs.append({"updateParagraphStyle": {"range": rng(s, e), "paragraphStyle": {
                "spaceAbove": {"magnitude": 12, "unit": "PT"}, "spaceBelow": {"magnitude": 12, "unit": "PT"}},
                "fields": "spaceAbove,spaceBelow"}})
            reqs.append({"updateTextStyle": {"range": rng(s, e - 1), "textStyle": {"italic": True}, "fields": "italic"}})
        if k == "src":
            reqs.append({"updateTextStyle": {"range": rng(s, e - 1), "textStyle": {"fontSize": {"magnitude": 12, "unit": "PT"}},
                                             "fields": "fontSize"}})
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
    for s, e, k in groups:
        reqs.append({"createParagraphBullets": {"range": rng(s, e), "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"}})
    return {"requests": reqs, "writeControl": {"requiredRevisionId": rev}}


def objects(doc_json):
    rev, body = load(doc_json)
    marks = []
    for el in body:
        p = el.get("paragraph")
        if not p:
            continue
        txt = "".join(e.get("textRun", {}).get("content", "") for e in p["elements"])
        m = re.match(r"\[\[(TABLA|IMG):([^\]]+)\]\]\n", txt)
        if m:
            marks.append((el["startIndex"], el["endIndex"], m.group(1), m.group(2)))
    tables = {b[1]: b[2] for b in B if b[0] == "table"}
    reqs = []
    for s, e, kind, name in sorted(marks, reverse=True):
        if kind == "IMG":
            reqs += [
                {"deleteContentRange": {"range": rng(s, e - 1)}},
                {"insertInlineImage": {"location": {"index": s, "tabId": TAB}, "uri": RAW + name,
                                       "objectSize": {"width": {"magnitude": 460, "unit": "PT"}}}},
                {"updateParagraphStyle": {"range": rng(s, s + 1), "paragraphStyle": {
                    "alignment": "CENTER", "spaceBelow": {"magnitude": 0, "unit": "PT"}}, "fields": "alignment,spaceBelow"}},
            ]
        else:
            path = f"{tempfile.gettempdir()}/t_{name}.json"
            json.dump(tables[name], open(path, "w"), ensure_ascii=False)
            reqs.append({"deleteContentRange": {"range": rng(s, e)}})
            out = subprocess.run([sys.executable, f"{SK}/docs_index.py", "new-table", "--at", str(s - 1), "--data", path,
                                  "--tab", TAB, "--bold-header"], capture_output=True, text=True, check=True).stdout
            reqs += json.loads(out)["requests"]
    return {"requests": reqs, "writeControl": {"requiredRevisionId": rev}}


SUP = re.compile(r"\^(\d+(?:\.\d+)?|[a-z])")


def md_inline(t):
    return SUP.sub(r"<sup>\1</sup>", t)


def markdown():
    out = []
    for b in B:
        k = b[0]
        if k in ("h1", "h2", "h3", "h4"):
            out.append("\n" + "#" * int(k[1]) + " " + b[1] + "\n")
        elif k == "p":
            out.append(md_inline(b[1]) + "\n")
        elif k in ("bullet", "src"):
            out.append("- " + md_inline(b[1]))
        elif k == "cap":
            out.append(f"\n*{md_inline(b[1])}*\n")
        elif k == "img":
            out.append(f"\n![{b[1]}](../results/figures/{b[1]})")
        elif k == "table":
            rows = b[2]
            out += ["", "| " + " | ".join(rows[0]) + " |", "|" + "---|" * len(rows[0])]
            out += ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return "\n".join(out).strip() + "\n"


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "text":
        sys.stdout.write(full_text())
    elif c == "styles":
        print(json.dumps(styles(sys.argv[2]), ensure_ascii=False))
    elif c == "objects":
        print(json.dumps(objects(sys.argv[2]), ensure_ascii=False))
    elif c == "md":
        sys.stdout.write(markdown())
