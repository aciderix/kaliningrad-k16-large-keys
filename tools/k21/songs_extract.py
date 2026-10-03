import json, glob, re, html, os
os.makedirs('vla/apisongs',exist_ok=True); n=0; tot=0
for f in sorted(glob.glob('vla/api/p*.json')):
    for post in json.load(open(f)):
        c=post['content']['rendered']
        j=c.find('Text und Musik')
        body=c if j<0 else c[:j]
        t=re.sub(r'<br\s*/?>','\n',body); t=re.sub(r'<[^>]+>','',t); t=html.unescape(t)
        if len(t)<80: continue
        open('vla/apisongs/'+post['slug'][:120]+'.txt','w').write(t); n+=1; tot+=len(t)
print('songs',n,'chars',tot)
