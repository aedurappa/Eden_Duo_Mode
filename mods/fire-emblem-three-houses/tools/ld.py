import struct, zlib
R='H:/EdenDuo/output/unpacked/010055D009F78000/romfs/'
D0=open(R+'DATA0.bin','rb').read()
def entry(i):
    off,pl,st,fl=struct.unpack_from('<4Q',D0,i*32)
    if pl==0: return b''
    with open(R+'DATA1.bin','rb') as f:
        f.seek(off); b=f.read(st)
    if not fl: return b
    cs,n,plain=struct.unpack_from('<III',b,0)
    sizes=struct.unpack_from('<%dI'%n,b,12)
    pos=(12+4*n+0x7f)&~0x7f
    out=bytearray()
    for k,s in enumerate(sizes):
        ch=b[pos:pos+s]
        if s==min(cs,plain-len(out)) and not (len(ch)>4 and False):
            # raw chunk heuristics: stored==plain size
            out+=ch
        else:
            zl=struct.unpack_from('<I',ch,0)[0]
            out+=zlib.decompress(ch[4:4+zl])
        pos=(pos+s+0x7f)&~0x7f
    return bytes(out)
