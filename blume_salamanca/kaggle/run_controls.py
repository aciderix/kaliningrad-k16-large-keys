# Noyau Kaggle (GPU) : compile bdt_gpu.cu et le vérifie sur les contrôles plantés de BLUME.
import subprocess, os
def sh(c):
    print('$', c, flush=True); subprocess.run(c, shell=True, check=True)
sh('nvidia-smi || true')
sh('git clone -q --depth 1 -b claude/trusting-cerf-i26igv https://github.com/aciderix/kaliningrad-k16-large-keys.git repo')
os.chdir('repo/blume_salamanca')
sh('nvcc -O3 -gencode arch=compute_60,code=sm_60 -gencode arch=compute_75,code=sm_75 -o bdt_gpu tools/bdt_gpu.cu')
for c in ['pc', 'pt', 'ps']:
    sh(f'./bdt_gpu data/models/qg_es.bin data/controls/{c}1.txt data/controls/{c}2.txt data/controls/ctl_keys_20k.txt 11 30 11 30 2 4.5 4 | tee /kaggle/working/ctl_{c}.txt')
