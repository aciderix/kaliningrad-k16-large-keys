import urllib.request, re, html, time, os, sys, hashlib, ssl
from concurrent.futures import ThreadPoolExecutor
os.makedirs('songs',exist_ok=True)
urls=[u.strip() for u in open('posts.txt') if u.strip()]
ctx=ssl.create_default_context(cafile=os.environ.get('SSL_CERT_FILE') or None)
def get(u):
    fn='songs/'+u.rstrip('/').split('/')[-1][:120]+'.txt'
    if os.path.exists(fn): return 0
    for t in range(3):
        try:
            req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (research; bottle-cipher study)'})
            s=urllib.request.urlopen(req,timeout=40).read().decode('utf-8','ignore')
            i=s.find('entry-content')
            if i<0: return 0
            seg=s[i:i+60000]
            j=seg.find('Liederthema:')
            if j>0: seg=seg[:j]
            t2=re.sub(r'<script.*?</script>|<style.*?</style>','',seg,flags=re.S); t2=re.sub(r'<br\s*/?>','\n',t2); t2=re.sub(r'<[^>]+>','',t2); t2=html.unescape(t2)
            open(fn,'w').write(t2[t2.find('>')+1:])
            time.sleep(0.4); return 1
        except Exception as e:
            time.sleep(3*(t+1))
    return 0
with ThreadPoolExecutor(2) as ex:
    n=0
    for r in ex.map(get,urls):
        n+=r
        if n%500==0 and r: print(n,flush=True)
print('done',n)
