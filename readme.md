1. parse html docs, find main text, split to shingles, get int32 hash from shingle
2. hashing docs buckets with location sensitive hashing
3. find similarity with min-hash

all in map-reduce (with bottleneck in 2->3 step, storing all docs in 1 server, see main.py)

pip install beautifulsoup4

pip install scipy


running:

python main.py

./stupid_worker.sh (as many as you wish, but change news.py to right server if many servers)


lsh and min-hash exploration: http://users.soe.ucsc.edu/~niejiazhong/slides/kumar.pdf

lsh in map-reduce exploration: http://architects.dzone.com/articles/location-sensitive-hashing

simple python map-reduce framework: https://github.com/michaelfairley/mincemeatpy

lecture in russian: http://compscicenter.ru/program/lecture/7329

only russian in text parsing grammar, tests, and most of examples code :)
