import sys
sys.path.insert(0, '.')
from msg import lang

idx = [257, 259, 598, 283, 284]
with open('probe_texts.tsv', 'w', encoding='utf-8', newline='\n') as f:
    for l in range(12):
        part = lang(l)[1]
        for i in idx:
            assert '\t' not in part[i] and '\n' not in part[i]
            f.write(f'{l}\t{i}\t{part[i]}\n')
print('ok')
