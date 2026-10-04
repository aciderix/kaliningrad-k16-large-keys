import bz2, re, sys
out = open('wq_sentences.txt', 'w')
n_pages = n_sent = 0; intext = False; buf = []
TAG = re.compile(r'<[^>]+>'); TEMPL = re.compile(r'\{\{[^{}]*\}\}'); LINK = re.compile(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]')
EXT = re.compile(r'\[https?://\S+\s*([^\]]*)\]'); QUOTE = re.compile(r"'{2,}")
def clean(s):
    for _ in range(3): s = TEMPL.sub('', s)
    s = LINK.sub(r'\1', s); s = EXT.sub(r'\1', s); s = QUOTE.sub('', s); s = TAG.sub('', s)
    s = s.replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&nbsp;', ' ')
    return s
with bz2.open('enwikiquote.xml.bz2', 'rt', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if '<text' in line: intext = True
        if intext:
            s = line
            if s.lstrip().startswith(('*', ':')) or (s.strip() and not s.lstrip().startswith(('{', '|', '!', '=', '[[Category', '<'))):
                t = clean(s.lstrip('*: \t#')).strip()
                if len(t) > 15 and not t.startswith(('http', 'File:', 'Image:')):
                    for sent in re.split(r'(?<=[.!?;:])\s+', t):
                        sent = sent.strip(' "“”‘’\'()-—–')
                        if sum(c.isalpha() for c in sent) >= 12:
                            out.write(sent + '\n'); n_sent += 1
        if '</text>' in line: intext = False; n_pages += 1
print(n_pages, 'pages', n_sent, 'phrases', file=sys.stderr)
