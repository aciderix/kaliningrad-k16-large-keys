l=$1
for g in wikipedia_2021 news_2020 wikipedia_2016 community_2017 web_2015 newscrawl_2016 wikipedia_2014 wikipedia_2010 mixed_2012 web_2012 news_2018 news_2010 newscrawl_2011; do
 for sz in 30K 10K; do
  u="https://downloads.wortschatz-leipzig.de/corpora/${l}_${g}_${sz}.tar.gz"
  if curl -sSf -o tgz/$l.tgz "$u" 2>/dev/null; then echo "$l ${g}_${sz}"; exit 0; fi
 done
done
echo "$l NONE"
