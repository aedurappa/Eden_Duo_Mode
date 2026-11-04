"""Generates companions/native/modules/fe3h_labels_data.inc and the localized manifest.

Every `label` widget of the manifest with a fixed English `text` that is localizable becomes a
`bind_text` on "ui.l.<slug>"; the module publishes the text of the game's language under that key.
Game terms are read from the game's own msgdata at run time (refs.py: label -> part, index);
the phrases the game has no word for are the translations of own.py.
"""
import json
import re
import sys

sys.path.insert(0, '.')
from own import COLS, OWN, REFS_EXTRA
from refs import REFS
from layout_fix import fix_turn_overlap

MODULES = 'H:/EdenDuo/companions/native/modules'
MANIFEST = sys.argv[1]  # the manifest to read and rewrite

with open(MANIFEST, encoding='utf-8') as f:
    manifest = json.load(f)

# the label widgets whose fixed text becomes a key
static = {'Waiting for the game', 'The Companion Module Did Not Start',
          'Supported Game VERSION: 1.2.0', 'Dual Screen Companion', '\u2013', '\u2192', '-'}
refs = {k: v for k, v in REFS.items() if v}
refs.update(REFS_EXTRA)


def slug(text):
    return re.sub(r'[^a-z0-9]+', '_', text.lower()).strip('_')


used = []


def walk(o):
    if isinstance(o, dict):
        if o.get('type') == 'label' and isinstance(o.get('text'), str) and 'bind_text' not in o:
            t = o['text']
            if t not in static and (t in refs or t in OWN):
                if t not in used:
                    used.append(t)
                # keep the widget's key order: text -> bind_text in place
                items = [('bind_text', 'ui.l.' + slug(t)) if k == 'text' else (k, v) for k, v in o.items()]
                o.clear()
                o.update(items)
        for v in list(o.values()):
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)


print('turn overlap fix:', fix_turn_overlap(manifest), 'widgets')
walk(manifest['pages'])
keys = [slug(t) for t in used]
assert len(set(keys)) == len(keys), 'slug collision'
missing = [t for t in refs if t not in used and t != 'Personal']
print(len(used), 'localized labels;', len(refs) - sum(1 for t in refs if t in used), 'refs not used by a label')


def lit(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


rows = []
for t in sorted(used):
    en = t
    if t in refs:
        part, index = refs[t]
        own = [en] + ['nullptr'] * (len(COLS) - 1)
        own = [lit(en)] + ['nullptr'] * (len(COLS) - 1)
    else:
        part, index = -1, 0
        own = [lit(x) for x in OWN[t]]
        own[0] = lit(en)
    rows.append('    {%s, %d, %d, {%s}},' % (lit(slug(t)), part, index, ', '.join(own)))

with open(MODULES + '/fe3h_labels_data.inc', 'w', encoding='utf-8', newline='\n') as f:
    f.write('// SPDX-FileCopyrightText: Copyright 2026 Eden_Duo_Mode contributors\n')
    f.write('// SPDX-License-Identifier: GPL-3.0-or-later\n')
    f.write('// Generated (gen_labels.py): the localizable labels of the manifest. {key, game text part,\n')
    f.write('// game text index (part < 0: none), own text per column: en ja de fr es it ko twn chn}.\n')
    f.write('// A game text entry reads its word from the game\'s own msgdata in the game\'s language; its\n')
    f.write('// English text is the fallback. The other entries are this companion\'s own wording.\n')
    f.write('\n'.join(rows) + '\n')

# a small gray line at the bottom of every page: the language the module found (set DBG=0 to omit)
import os
if os.environ.get('DBG', '1') != '0':
    for page in manifest['pages']:
        page['widgets'].append({'type': 'label', 'rect': [8, 1064, 0, 0], 'bind_text': 'fe.dbg',
                                'text_scale': 3, 'color': '#FF8A84A6'})
    print('debug line added to', len(manifest['pages']), 'pages')

with open(MANIFEST, 'w', encoding='utf-8', newline='') as f:
    json.dump(manifest, f, ensure_ascii=False, separators=(',', ':'))
    f.write('\n')
print('wrote', len(rows), 'entries')
