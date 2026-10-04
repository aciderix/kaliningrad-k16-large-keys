import sys, re, numpy as np, glob
files = sys.argv[2:]; out = sys.argv[1]
txt = []
for f in files:
    s = open(f, encoding='utf-8', errors='ignore').read()
    a, b = s.find('*** START'), s.find('*** END')
    if 0 < a < b: s = s[a + 200:b]
    txt.append(re.sub('[^a-z]', '', s.lower()))
t = np.frombuffer(''.join(txt).encode(), dtype=np.uint8).astype(np.int64) - 97
idx = ((t[:-3] * 26 + t[1:-2]) * 26 + t[2:-1]) * 26 + t[3:]
c = np.bincount(idx, minlength=456976).astype(np.float64); N = c.sum()
q = np.where(c > 0, np.log(np.maximum(c, 1) / N), np.log(0.01 / N)).astype('<f4')
q.tofile(out); print(len(t), 'lettres ->', out)
