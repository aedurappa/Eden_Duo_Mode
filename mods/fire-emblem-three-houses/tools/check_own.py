import sys
sys.path.insert(0, '.')
from ld import *
from own import *


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


lat, kor, jpn, twn, chn = table(77), table(80), table(76), table(78), table(79)
# the font a language gets: Latin, its own set, and Korean for what only Korean has
cover = {'en': lat, 'de': lat, 'fr': lat, 'es': lat, 'it': lat,
         'ja': lat | jpn | kor, 'ko': lat | kor, 'twn': lat | twn | kor, 'chn': lat | chn | kor}
bad = []
for lab, tr in OWN.items():
    assert len(tr) == 9, lab
    for col, t in zip(COLS, tr):
        for ch in t:
            if ch != ' ' and ch not in cover[col]:
                bad.append((lab, col, ch, hex(ord(ch))))
print('phrases:', len(OWN))
print('uncovered chars:', bad or 'none')
