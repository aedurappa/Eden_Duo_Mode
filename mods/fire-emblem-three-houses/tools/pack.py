"""Installs the freshly built modules into the 1.1.0 package, refreshes their hashes, zips it."""
import hashlib
import json
import os
import shutil
import zipfile

ROOT = 'H:/EdenDuo'
P = ROOT + '/010055D009F78000-FireEmblemThreeHousesDS-1.1.1-multilang.dsmod'
DIST = ROOT + '/work/cache/dist'
LIB = '010055D009F78000.so'

pkg = open(P + '/package.json', encoding='utf-8').read()
man = open(P + '/dualscreen/manifest.json', encoding='utf-8').read()
libs = json.loads(pkg)['module']['libraries']
for plat, info in libs.items():
    src = f'{DIST}/{plat}/{LIB}'
    dst = f'{P}/dualscreen/{info["path"]}'
    new = hashlib.sha256(open(src, 'rb').read()).hexdigest()
    old = info['sha256']
    old_man = json.loads(man)['module']['libraries'][plat]['sha256']  # the manifest may lag behind
    assert pkg.count(old) == 1 and man.count(old_man) == 1, plat
    shutil.copyfile(src, dst)
    pkg, man = pkg.replace(old, new), man.replace(old_man, new)
    print(plat, old[:12], '->', new[:12])
open(P + '/package.json', 'w', encoding='utf-8', newline='').write(pkg)
open(P + '/dualscreen/manifest.json', 'w', encoding='utf-8', newline='').write(man)

out = ROOT + '/010055D009F78000-FireEmblemThreeHousesDS-1.1.1-multilang.dsmod.zip'
if os.path.exists(out):
    os.remove(out)
members = ['package.json', 'dualscreen/fe3h_font.txt', 'dualscreen/manifest.json'] + \
          ['dualscreen/' + i['path'] for i in libs.values()]
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for rel in members:
        z.write(f'{P}/{rel}', rel)
z = zipfile.ZipFile(out)
assert z.testzip() is None
m = json.loads(z.read('package.json'))
for plat, v in m['module']['libraries'].items():
    assert hashlib.sha256(z.read('dualscreen/' + v['path'])).hexdigest() == v['sha256'], plat
mj = json.loads(z.read('dualscreen/manifest.json'))
assert mj['module']['libraries'] == m['module']['libraries']
print('zip ok', os.path.getsize(out), 'bytes;', len(members), 'files')
