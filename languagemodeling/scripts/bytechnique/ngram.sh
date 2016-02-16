#! /bin/bash

python scripts/train.py -n 1 -c B -o trained_models/brown/ngram_1_b
python scripts/train.py -n 2 -c B -o trained_models/brown/ngram_2_b
python scripts/train.py -n 3 -c B -o trained_models/brown/ngram_3_b
python scripts/train.py -n 4 -c B -o trained_models/brown/ngram_4_b


python scripts/train.py -n 1 -c G -o trained_models/gutenberg/ngram_1_g
python scripts/train.py -n 2 -c G -o trained_models/gutenberg/ngram_2_g
python scripts/train.py -n 3 -c G -o trained_models/gutenberg/ngram_3_g
python scripts/train.py -n 4 -c G -o trained_models/gutenberg/ngram_4_g


python scripts/train.py -n 1 -c S -o trained_models/shakespeare/ngram_1_s
python scripts/train.py -n 2 -c S -o trained_models/shakespeare/ngram_2_s
python scripts/train.py -n 3 -c S -o trained_models/shakespeare/ngram_3_s
python scripts/train.py -n 4 -c S -o trained_models/shakespeare/ngram_4_s
