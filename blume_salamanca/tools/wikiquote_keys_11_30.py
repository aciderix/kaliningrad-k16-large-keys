import sys, re, unicodedata
src, out_f, lo, hi = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
seen = set(); out = open(out_f, 'w')
for line in open(src, encoding='utf-8'):
    t = unicodedata.normalize('NFKD', line.lower().replace('ß', 'ss')).encode('ascii', 'ignore').decode()
    words = [w for w in (re.sub('[^a-z]', '', x) for x in t.split()) if w]
    acc = ''
    for w in words:                                  # débuts de phrase en mots entiers
        acc += w
        if len(acc) > hi: break
        if len(acc) >= lo and acc not in seen: seen.add(acc); out.write(acc + '\n')
    s = ''.join(words)                               # et coupés à toute longueur lo..hi
    for k in range(lo, min(hi, len(s)) + 1):
        c = s[:k]
        if c not in seen: seen.add(c); out.write(c + '\n')
print(len(seen), file=sys.stderr)
