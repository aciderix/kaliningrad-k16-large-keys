#!/bin/bash
p=$1; f=api/p$(printf %03d $p).json
[ -s $f ] && exit 0
for t in 1 2 3 4; do
  curl -sS -m 300 -A 'Mozilla/5.0 (research; bottle-cipher study)' -o $f.tmp "https://www.volksliederarchiv.de/wp-json/wp/v2/posts?per_page=100&page=$p&_fields=slug,content" && python3 -c "import json;json.load(open('$f.tmp'))" 2>/dev/null && mv $f.tmp $f && exit 0
  sleep $((t*10))
done
