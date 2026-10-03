#!/bin/sh
# K27 — contrôles plantés : allemand réservé + 99 nuls f/w/n, deux clés tirées du dictionnaire réduit.
# Usage : sh tools/k27/controles.sh <binaire dictdt> <clés réduites (keys.py ... 2000 2000)>
D=$1; K=$2; T=${TMPDIR:-/tmp}/k27ctrl.$$
for s in 1 2 3; do echo "== graine $s, texte entier, 4 variantes de base"; python3 tools/k27/ctrl.py $K $s $T | tail -1
  $D data/models/qg_de.bin $T $K $K whole 120 -12.8 2 51 2>&1 | grep -E "^ *-[0-9]+\.[0-9]{4}|au-dessus"; done
for s in 4 5; do echo "== graine $s, par bloc, 4 variantes de base"; python3 tools/k27/ctrl.py $K $s $T blocks | tail -1
  $D data/models/qg_de.bin $T $K $K blocks 120 -12.8 2 51 2>&1 | grep -E "^ *-[0-9]+\.[0-9]{4}|au-dessus"; done
for s in 11 12 13; do echo "== graine $s, texte entier, 16 variantes"; python3 tools/k27/ctrl.py $K $s $T whole 99 toutes | tail -1
  $D data/models/qg_de.bin $T $K $K whole 120 -12.8 2 65535 2>&1 | grep -E "^ *-[0-9]+\.[0-9]{4}|au-dessus"; done
for s in 14 15; do echo "== graine $s, par bloc, 16 variantes"; python3 tools/k27/ctrl.py $K $s $T blocks 99 toutes | tail -1
  $D data/models/qg_de.bin $T $K $K blocks 120 -12.8 2 65535 2>&1 | grep -E "^ *-[0-9]+\.[0-9]{4}|au-dessus"; done
rm -f $T
