#!/bin/bash
id=$1
[ -s t_$id.txt ] && exit 0
for t in 1 2 3; do
  curl -sS -m 90 -A "Mozilla/5.0" -o t_$id.txt "https://www.gutenberg.org/cache/epub/$id/pg$id.txt" && [ $(wc -c < t_$id.txt) -gt 2000 ] && exit 0
  sleep $((t*3))
done
rm -f t_$id.txt
