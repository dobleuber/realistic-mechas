"""Comprueba que el Google Doc (salida de documents.get) coincide con content.py: texto, tablas,
imágenes y superíndices.

  python verify.py DOC.json
"""
import json, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from build import B, parse_inline
d = json.load(open(sys.argv[1]))['content']
body = d['tabs'][0]['documentTab']['body']['content']
def ptext(p): return ''.join(e.get('textRun', {}).get('content', '') for e in p['elements']).rstrip('\n')
doc = []
for el in body:
    if 'table' in el:
        rows = [[''.join(ptext(ce['paragraph']) + '\n' for ce in c['content']).rstrip('\n') for c in r['tableCells']] for r in el['table']['tableRows']]
        doc.append(('table', rows, el['startIndex'], el['endIndex']))
    elif 'paragraph' in el:
        p = el['paragraph']
        if any('inlineObjectElement' in e for e in p['elements']):
            doc.append(('img', None, el['startIndex'], el['endIndex']))
        else:
            sups = [(e['startIndex'] - el['startIndex'], e['endIndex'] - el['startIndex']) for e in p['elements']
                    if e.get('textRun', {}).get('textStyle', {}).get('baselineOffset') == 'SUPERSCRIPT']
            doc.append(('p', ptext(p), el['startIndex'], el['endIndex'], sups, p['paragraphStyle'].get('namedStyleType')))
exp = []
for b in B:
    if b[0] == 'table': exp.append(('table', b[2]))
    elif b[0] == 'img': exp.append(('img', None))
    else:
        t, sp = parse_inline(b[1]); exp.append(('p', t, [(a, c) for a, c, w in sp if w == 'sup'], b[0]))
print('doc', len(doc), 'exp', len(exp))
i = j = 0; bad = 0; extra = []
while i < len(doc) and j < len(exp):
    a, e = doc[i], exp[j]
    if a[0] == 'p' and a[1] == '' and e[0] != 'p':
        extra.append(a[2]); i += 1; continue
    if a[0] == 'p' and a[1] == '' and e[0] == 'p' and e[1] != '':
        extra.append(a[2]); i += 1; continue
    if a[0] != e[0] or a[1] != e[1]:
        print('MISMATCH', a[:2] if a[0] != 'table' else a[0], '\n   vs', e[:2]); bad += 1
    elif a[0] == 'p':
        # superíndices: el doc agrupa runs; comprobar que cubren lo esperado
        cover = set(k for s, t in a[4] for k in range(s, t))
        want = set(k for s, t in e[2] for k in range(s, t))
        if cover != want: print('SUP mismatch', a[1][:60], sorted(cover), sorted(want)); bad += 1
    i += 1; j += 1
print('leftover doc', doc[i:], 'leftover exp', exp[j:])
print('empty paragraphs not in content at', extra)
print('bad', bad, 'rev', d['revisionId'])
