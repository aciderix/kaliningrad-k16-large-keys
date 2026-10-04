#!/bin/sh
# Corpus de référence de K18 (non versé au dépôt). Usage : sh tools/k18/fetch_corpus.sh [dossier] ; puis K18_CORPUS=dossier.
D=${1:-corpus}; mkdir -p "$D"
for id in 2229 35312 50285 2407 6498 22367 5323 21000 2403 24288 38780 19460 6343 12108 24571 7205 34811 65661 56156 31284 40739; do
  curl -sSL -A "Mozilla/5.0" -o "$D/g$id.txt" "https://www.gutenberg.org/cache/epub/$id/pg$id.txt"; done
for id in 11024 1012 2000 218 11940 31536 3333 17489 7000 25343 1661 20203 26073 8800 10805; do
  curl -sSL -A "Mozilla/5.0" -o "$D/x_$id.txt" "https://www.gutenberg.org/cache/epub/$id/pg$id.txt"; done
curl -sSL -o "$D/en_1342.txt" https://www.gutenberg.org/cache/epub/1342/pg1342.txt
curl -sSL -o "$D/en_2701.txt" https://www.gutenberg.org/cache/epub/2701/pg2701.txt
curl -sSL -o "$D/fr_18143.txt" https://www.gutenberg.org/cache/epub/18143/pg18143.txt
# Bible synodale russe (1876), pour tester l'affirmation de « Frank » (Cipherbrain, 2021)
curl -sSL -o "$D/ru_synodal.json" https://raw.githubusercontent.com/maatheusgois/bible/main/versions/ru/synodal.json
# K19 : poésie, chants, comptines, bas-allemand, allemand de Pennsylvanie, Bible Schlachter 1951
for id in 3498 57915 51467 44784 70178; do
  curl -sSL -A "Mozilla/5.0" -o "$D/p_$id.txt" "https://www.gutenberg.org/cache/epub/$id/pg$id.txt"; done
curl -sSL -o "$D/de_schlachter.json" https://raw.githubusercontent.com/maatheusgois/bible/main/versions/de/schlachter.json
