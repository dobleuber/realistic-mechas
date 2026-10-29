"""Construye las peticiones de la API de Docs y una copia en Markdown del contenido.

    python build.py text  TAB_ID REVISION  > batch_text.json
    python build.py md                      > version_revisada.md
    python build.py objects TAB_ID REVISION DOC.json > batch_objects.json   (tablas e imágenes)
"""
import json
import re
import subprocess
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from content import B, RAW  # noqa: E402

SK = "/root/.claude/skills/synced/bbc03e69-a18b-4fc5-965c-3a1d28d9c489_e05548c1-1a7e-4e03-90f5-a72175d66a4c/google-workspace/scripts"
INLINE = re.compile(r"\*\*(.+?)\*\*|\[([^\]]+)\]\(([^)]+)\)")


def u16(s):
    return len(s.encode("utf-16-le")) // 2


def parse_inline(s):
    """Devuelve (texto plano, [(ini, fin, 'bold'|url)]) con offsets UTF-16."""
    out, spans, pos = "", [], 0
    for m in INLINE.finditer(s):
        out += s[pos:m.start()]
        start = u16(out)
        if m.group(1) is not None:
            out += m.group(1)
            spans.append((start, u16(out), "bold"))
        else:
            out += m.group(2)
            spans.append((start, u16(out), m.group(3)))
        pos = m.end()
    out += s[pos:]
    return out, spans


def paragraphs():
    """Lista de (tipo, texto plano, spans, extra) incluyendo marcadores de tablas e imágenes."""
    res = []
    for b in B:
        kind = b[0]
        if kind == "table":
            res.append(("ph", f"[[TABLA:{b[1]}]]", [], b[2]))
        elif kind == "img":
            res.append(("ph", f"[[IMG:{b[1]}]]", [], b[1]))
        else:
            t, sp = parse_inline(b[1])
            res.append((kind, t, sp, None))
    return res


def text_batch(tab, rev):
    paras = paragraphs()
    full = "\n".join(p[1] for p in paras)
    reqs = [{"insertText": {"location": {"index": 1, "tabId": tab}, "text": full}}]
    idx = 1
    styles, texts, bullets = [], [], []
    for kind, t, spans, _ in paras:
        s, e = idx, idx + u16(t) + 1
        named = {"title": "TITLE", "h1": "HEADING_1", "h2": "HEADING_2"}.get(kind, "NORMAL_TEXT")
        ps = {"namedStyleType": named}
        fields = "namedStyleType"
        if kind in ("h1", "h2", "title"):
            ps["keepWithNext"] = True
            fields += ",keepWithNext"
        if named != "NORMAL_TEXT":  # el texto insertado ya es NORMAL_TEXT
            styles.append({"updateParagraphStyle": {"range": {"startIndex": s, "endIndex": e, "tabId": tab},
                                                    "paragraphStyle": ps, "fields": fields}})
        for a, b_, what in spans:
            rng = {"startIndex": s + a, "endIndex": s + b_, "tabId": tab}
            if what == "bold":
                texts.append({"updateTextStyle": {"range": rng, "textStyle": {"bold": True}, "fields": "bold"}})
            else:
                texts.append({"updateTextStyle": {"range": rng, "textStyle": {"link": {"url": what}}, "fields": "link"}})
        if kind == "bullet":
            if bullets and bullets[-1][1] == s:
                bullets[-1][1] = e
            else:
                bullets.append([s, e])
        idx = e
    for s, e in bullets:
        reqs_b = {"createParagraphBullets": {"range": {"startIndex": s, "endIndex": e, "tabId": tab},
                                             "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"}}
        texts.append(reqs_b)
    return {"requests": reqs + styles + texts, "writeControl": {"requiredRevisionId": rev}}


def markdown():
    lines = []
    for b in B:
        k = b[0]
        if k == "title":
            lines.append(f"# {b[1]}\n")
        elif k == "h1":
            lines.append(f"\n## {b[1]}\n")
        elif k == "h2":
            lines.append(f"\n### {b[1]}\n")
        elif k == "p":
            lines.append(b[1] + "\n")
        elif k == "bullet":
            lines.append(f"- {b[1]}")
        elif k == "img":
            lines.append(f"\n![{b[1]}](../results/figures/{b[1]})\n")
        elif k == "table":
            rows = b[2]
            lines.append("")
            lines.append("| " + " | ".join(rows[0]) + " |")
            lines.append("|" + "---|" * len(rows[0]))
            for r in rows[1:]:
                lines.append("| " + " | ".join(r) + " |")
            lines.append("")
    return "\n".join(lines) + "\n"


def objects_batch(tab, rev, doc_json):
    """Sustituye cada marcador por su tabla o imagen, de abajo arriba."""
    doc = json.load(open(doc_json))
    content = doc.get("content", doc)

    def find_tab(tabs):
        for t in tabs:
            if t["tabProperties"]["tabId"] == tab:
                return t
            r = find_tab(t.get("childTabs", []))
            if r:
                return r
    body = find_tab(content["tabs"])["documentTab"]["body"]["content"]
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
                {"deleteContentRange": {"range": {"startIndex": s, "endIndex": e - 1, "tabId": tab}}},
                {"insertInlineImage": {"location": {"index": s, "tabId": tab}, "uri": RAW + name,
                                       "objectSize": {"width": {"magnitude": 460, "unit": "PT"}}}},
                {"updateParagraphStyle": {"range": {"startIndex": s, "endIndex": s + 1, "tabId": tab},
                                          "paragraphStyle": {"alignment": "CENTER"}, "fields": "alignment"}},
            ]
        else:
            path = f"/tmp/claude-0/-home-user-pipboy-otto/8254ed8a-d5dd-5050-8dac-90ae90b806a2/scratchpad/gdoc/t_{name}.json"
            json.dump(tables[name], open(path, "w"), ensure_ascii=False)
            reqs.append({"deleteContentRange": {"range": {"startIndex": s, "endIndex": e, "tabId": tab}}})
            out = subprocess.run([sys.executable, f"{SK}/docs_index.py", "new-table", "--at", str(s - 1),
                                  "--data", path, "--tab", tab, "--bold-header"],
                                 capture_output=True, text=True, check=True).stdout
            reqs += json.loads(out)["requests"]
    return {"requests": reqs, "writeControl": {"requiredRevisionId": rev}}


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "text":
        print(json.dumps(text_batch(sys.argv[2], sys.argv[3]), ensure_ascii=False))
    elif cmd == "md":
        print(markdown())
    elif cmd == "objects":
        print(json.dumps(objects_batch(sys.argv[2], sys.argv[3], sys.argv[4]), ensure_ascii=False))


def doc_paragraphs(doc_json, tab):
    doc = json.load(open(doc_json))
    content = doc.get("content", doc)
    for t in content["tabs"]:
        if t["tabProperties"]["tabId"] == tab:
            body = t["documentTab"]["body"]["content"]
    out = []
    for el in body:
        p = el.get("paragraph")
        if p is None:
            continue
        txt = "".join(e.get("textRun", {}).get("content", "") for e in p["elements"])
        out.append((el["startIndex"], el["endIndex"], txt.rstrip("\n")))
    return content["revisionId"], out


def styles_batch(tab, doc_json):
    rev, dps = doc_paragraphs(doc_json, tab)
    paras = paragraphs()
    if len(dps) != len(paras):
        raise SystemExit(f"número de párrafos distinto: doc {len(dps)} vs contenido {len(paras)}")
    reqs, bullets = [], []
    for (s, e, txt), (kind, t, spans, _) in zip(dps, paras):
        if txt != t:
            raise SystemExit(f"texto distinto en {s}:\n doc: {txt[:120]}\n esp: {t[:120]}")
        named = {"title": "TITLE", "h1": "HEADING_1", "h2": "HEADING_2"}.get(kind)
        if named:
            reqs.append({"updateParagraphStyle": {"range": {"startIndex": s, "endIndex": e, "tabId": tab},
                         "paragraphStyle": {"namedStyleType": named, "keepWithNext": True},
                         "fields": "namedStyleType,keepWithNext"}})
        for a, b_, what in spans:
            rng = {"startIndex": s + a, "endIndex": s + b_, "tabId": tab}
            ts = {"bold": True} if what == "bold" else {"link": {"url": what}}
            reqs.append({"updateTextStyle": {"range": rng, "textStyle": ts, "fields": "bold" if what == "bold" else "link"}})
        if kind == "bullet":
            if bullets and bullets[-1][1] == s:
                bullets[-1][1] = e
            else:
                bullets.append([s, e])
    for s, e in bullets:
        reqs.append({"createParagraphBullets": {"range": {"startIndex": s, "endIndex": e, "tabId": tab},
                                                "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"}})
    return {"requests": reqs, "writeControl": {"requiredRevisionId": rev}}


if __name__ == "__main__" and sys.argv[1] == "styles":
    print(json.dumps(styles_batch(sys.argv[2], sys.argv[3]), ensure_ascii=False))
