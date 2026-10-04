import sys, re
mode = sys.argv[1]; lo, hi = 20, 27
seen = set(); out = open('keys_%s.txt' % mode, 'w'); n = 0
for line in open('wq_sentences.txt', encoding='utf-8'):
    words = [re.sub('[^a-z]', '', w) for w in line.lower().split()]
    words = [w for w in words if w]
    if not words: continue
    cands = []
    if mode == 'prefix':                       # débuts de phrase en mots entiers
        L = 0
        for w in words:
            L += len(w)
            if lo <= L <= hi: cands.append(''.join(words[:words.index(w) + 1]) if False else None)
        acc = ''; 
        for w in words:
            acc += w
            if lo <= len(acc) <= hi: cands.append(acc)
            if len(acc) > hi: break
        cands = [c for c in cands if c]
    elif mode == 'windows':                    # toute suite de mots entiers
        for i in range(len(words)):
            acc = ''
            for w in words[i:]:
                acc += w
                if len(acc) > hi: break
                if len(acc) >= lo: cands.append(acc)
    elif mode == 'trunc':                      # premières lettres de la phrase, coupées à 20..27
        s = ''.join(words)
        cands = [s[:k] for k in range(lo, min(hi, len(s)) + 1)]
    for c in cands:
        if c not in seen: seen.add(c); out.write(c + '\n'); n += 1
print(mode, n, file=sys.stderr)
