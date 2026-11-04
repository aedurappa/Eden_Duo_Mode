"""Korean-only package: the manifest's fixed English words replaced by fixed Korean ones.

No per-language labels: the game terms are the game's own Korean (from msgdata, as in refs.py),
the companion's own phrases are the Korean column of own.py, a few extra words are below.
"""
import hashlib
import json
import os
import shutil
import sys
import zipfile

sys.path.insert(0, '.')
from ld import entry
from msg import lang
from own import OWN, REFS_EXTRA
from refs import REFS
from layout_fix import fix_turn_overlap

ROOT = 'H:/EdenDuo'
SRC = ROOT + '/010055D009F78000-FireEmblemThreeHousesDS-1.1.1-multilang.dsmod'   # current build (hashes)
DST = ROOT + '/010055D009F78000-FireEmblemThreeHousesDS-1.1.1-ko.dsmod'
ZIP = DST + '.zip'

KO_STATIC = {
    'Dual Screen Companion': '듀얼 스크린 컴패니언',
    'Waiting for the game': '게임을 기다리는 중',
    'The Companion Module Did Not Start': '컴패니언 모듈이 시작되지 않았습니다',
    'Supported Game VERSION: 1.2.0': '지원 게임 버전: 1.2.0',
}
GAME_EXTRA = {'Total': (1, 398)}

ko = lang(9)
refs = {k: v for k, v in REFS.items() if v}
refs.update(REFS_EXTRA)
refs.update(GAME_EXTRA)


def table(i):
    t = entry(i)
    r = set()
    for k in range(0, len(t), 4):
        v = int.from_bytes(t[k:k + 4], 'little')
        try:
            r.add(v.to_bytes(4, 'big').lstrip(b'\0').decode('utf-8'))
        except Exception:
            pass
    return r


covered = table(77) | table(80)
used = {}


def korean(text):
    core = text.strip()
    pad_l, pad_r = text[:len(text) - len(text.lstrip())], text[len(text.rstrip()):]
    if core in KO_STATIC:
        out = KO_STATIC[core]
    elif core in refs:
        part, index = refs[core]
        out = ''.join(c for c in ko[part][index] if ord(c) >= 0x20)
        out = out.replace('・', '·')  # the Korean font has no katakana middle dot
    elif core in OWN:
        out = OWN[core][6]
    else:
        return text
    used[text] = pad_l + out + pad_r
    return used[text]


manifest = json.load(open(ROOT + '/work/manifest_pre_labels.json', encoding='utf-8'))


def walk(o):
    if isinstance(o, dict):
        if isinstance(o.get('text'), str) and o.get('type') in ('label', 'value'):
            o['text'] = korean(o['text'])
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)


print('turn overlap fix:', fix_turn_overlap(manifest), 'widgets')
walk(manifest['pages'])
bad = sorted({c for t in used.values() for c in t if c != ' ' and c not in covered})
print('translated', len(used), 'distinct texts; chars missing from the Korean font:', bad or 'none')
assert not bad

# hashes of the modules in the package
cur = json.load(open(SRC + '/package.json', encoding='utf-8'))['module']['libraries']
old = manifest['module']['libraries']
text = json.dumps(manifest, ensure_ascii=False, separators=(',', ':')) + '\n'
for plat in cur:
    assert text.count(old[plat]['sha256']) == 1
    text = text.replace(old[plat]['sha256'], cur[plat]['sha256'])

if os.path.exists(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)
open(DST + '/dualscreen/manifest.json', 'w', encoding='utf-8', newline='').write(text)
assert json.loads(text)['module']['libraries'] == cur

members = ['package.json', 'dualscreen/fe3h_font.txt', 'dualscreen/manifest.json'] + \
          ['dualscreen/' + i['path'] for i in cur.values()]
if os.path.exists(ZIP):
    os.remove(ZIP)
with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
    for rel in members:
        z.write(f'{DST}/{rel}', rel)
z = zipfile.ZipFile(ZIP)
assert z.testzip() is None
pk = json.loads(z.read('package.json'))
for plat, v in pk['module']['libraries'].items():
    assert hashlib.sha256(z.read('dualscreen/' + v['path'])).hexdigest() == v['sha256'], plat
print('zip ok', os.path.getsize(ZIP), 'bytes')
for k, v in list(used.items())[:6]:
    print(repr(k), '->', v)
