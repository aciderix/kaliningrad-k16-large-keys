# Noyau Kaggle (GPU) — B07 : dictionnaires de phrases-clés pour BLUME sur GPU (tools/bdt_gpu.cu), deux numérotations.
# 1) contrôle planté ; 2) Bibles de/es + 33 œuvres (troncatures + mots) ; 3) Wikiquote de/es (débuts + fenêtres) ;
# 4) tous les livres Gutenberg allemands et espagnols (mots seulement). Sorties dans /kaggle/working.
import subprocess, os, sys, time
def sh(c, check=True):
    print('$', c, flush=True); return subprocess.run(c, shell=True, check=check)
W = '/kaggle/working'
sh('nvidia-smi || true')
sh('git clone -q --depth 1 -b claude/trusting-cerf-i26igv https://github.com/aciderix/kaliningrad-k16-large-keys.git repo')
os.chdir('repo/blume_salamanca')
sh('nvcc -O3 -gencode arch=compute_60,code=sm_60 -gencode arch=compute_75,code=sm_75 -o bdt_gpu tools/bdt_gpu.cu')
SCAN = './bdt_gpu data/models/qg_es.bin data/telegram1_615.txt data/telegram2_160.txt {keys} 11 30 11 30 2 4.5 60'
sh('./bdt_gpu data/models/qg_es.bin data/controls/pc1.txt data/controls/pc2.txt data/controls/ctl_keys_20k.txt 11 30 11 30 2 4.5 3 | tee ' + W + '/controle.txt')
os.makedirs('src', exist_ok=True)
def get(url, out):
    for i in range(3):
        if subprocess.run(f'curl -sSL --retry 2 -m 180 -o "{out}" "{url}"', shell=True).returncode == 0 and os.path.getsize(out) > 0: return True
        time.sleep(5)
    return False
# 2) Bibles + 33 œuvres (comme B02)
ids = '12108 19460 21000 2229 22367 2403 2407 24288 24571 31284 34811 35312 38780 40739 50285 5323 56156 6343 6498 65661 7205 15532 16625 17073 2000 25317 29506 36805 39647 46201 49836 55514 58221'.split()
os.makedirs('src/b02', exist_ok=True)
for i in ids: get(f'https://gutenberg.pglaf.org/cache/epub/{i}/pg{i}.txt', f'src/b02/pg{i}.txt')
for b in ['GerBoLut', 'GerElb1905', 'SpaRV', 'SpaRV1865']:
    get(f'https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/txt/{b}.txt', f'src/b02/{b}.txt')
sh('python3 tools/keys_texts.py 11 30 keys_b02.txt src/b02/*')
sh(SCAN.format(keys='keys_b02.txt') + ' | tee ' + W + '/b07_bibles_oeuvres.txt')
# 3) Wikiquote de/es
for l in ['de', 'es']:
    get(f'https://dumps.wikimedia.org/{l}wikiquote/latest/{l}wikiquote-latest-pages-articles.xml.bz2', f'src/{l}wq.xml.bz2')
    sh(f'python3 ../common/phrasekeys.py src/{l}wq.xml.bz2 11 30 prefix,trunc,windows 0 1 keys_wq_{l}.txt')
sh('cat keys_wq_de.txt keys_wq_es.txt > keys_wq.txt')
sh(SCAN.format(keys='keys_wq.txt') + ' | tee ' + W + '/b07_wikiquote.txt')
# 4) Gutenberg complet de/es (mots entiers)
os.makedirs('src/pg', exist_ok=True)
books = [l.strip() for l in open('data/pg_ids_de_es.txt') if l.strip()]
t0 = time.time()
for k, i in enumerate(books):
    get(f'https://gutenberg.pglaf.org/cache/epub/{i}/pg{i}.txt', f'src/pg/pg{i}.txt')
    if k % 200 == 0: print(k, 'livres', int(time.time() - t0), 's', flush=True)
sh('KEYS_TRUNC=0 KEYS_DEDUP=file python3 tools/keys_texts.py 11 30 keys_pg.txt src/pg/*')
sh(SCAN.format(keys='keys_pg.txt') + ' | tee ' + W + '/b07_gutenberg_complet.txt')
print('FIN', flush=True)
