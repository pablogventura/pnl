#! /bin/bash
mkdir -p trained_models
mkdir -p trained_models/brown
mkdir -p trained_models/gutenberg
mkdir -p trained_models/shakespeare
mkdir -p trained_models/shakespeare/ngram
mkdir -p trained_models/shakespeare/interpolated
mkdir -p trained_models/shakespeare/kneserney
mkdir -p trained_models/shakespeare/addone
mkdir -p trained_models/shakespeare/backoff
mkdir -p trained_models/gutenberg/ngram
mkdir -p trained_models/gutenberg/interpolated
mkdir -p trained_models/gutenberg/kneserney
mkdir -p trained_models/gutenberg/addone
mkdir -p trained_models/gutenberg/backoff
mkdir -p trained_models/brown/ngram
mkdir -p trained_models/brown/interpolated
mkdir -p trained_models/brown/kneserney
mkdir -p trained_models/brown/addone
mkdir -p trained_models/brown/backoff

python scripts/train.py -n 1 -c B -o trained_models/brown/kneserney/kneserney_1_b -m kn -D 1
python scripts/train.py -n 2 -c B -o trained_models/brown/kneserney/kneserney_2_b -m kn -D 1
python scripts/train.py -n 3 -c B -o trained_models/brown/kneserney/kneserney_3_b -m kn -D 1
python scripts/train.py -n 4 -c B -o trained_models/brown/kneserney/kneserney_4_b -m kn -D 1
python scripts/train.py -n 1 -c G -o trained_models/gutenberg/kneserney/kneserney_1_g -m kn -D 1
python scripts/train.py -n 2 -c G -o trained_models/gutenberg/kneserney/kneserney_2_g -m kn -D 1
python scripts/train.py -n 3 -c G -o trained_models/gutenberg/kneserney/kneserney_3_g -m kn -D 1
python scripts/train.py -n 4 -c G -o trained_models/gutenberg/kneserney/kneserney_4_g -m kn -D 1
python scripts/train.py -n 1 -c S -o trained_models/shakespeare/kneserney/kneserney_1_s -m kn -D 1
python scripts/train.py -n 2 -c S -o trained_models/shakespeare/kneserney/kneserney_2_s -m kn -D 1
python scripts/train.py -n 3 -c S -o trained_models/shakespeare/kneserney/kneserney_3_s -m kn -D 1
python scripts/train.py -n 4 -c S -o trained_models/shakespeare/kneserney/kneserney_4_s -m kn -D 1
#############
python scripts/train.py -n 1 -c B -o trained_models/brown/interpolated/interpolated_1_b -m in
python scripts/train.py -n 2 -c B -o trained_models/brown/interpolated/interpolated_2_b -m in
python scripts/train.py -n 3 -c B -o trained_models/brown/interpolated/interpolated_3_b -m in
python scripts/train.py -n 4 -c B -o trained_models/brown/interpolated/interpolated_4_b -m in
python scripts/train.py -n 1 -c G -o trained_models/gutenberg/interpolated/interpolated_1_g -m in
python scripts/train.py -n 2 -c G -o trained_models/gutenberg/interpolated/interpolated_2_g -m in
python scripts/train.py -n 3 -c G -o trained_models/gutenberg/interpolated/interpolated_3_g -m in
python scripts/train.py -n 4 -c G -o trained_models/gutenberg/interpolated/interpolated_4_g -m in
python scripts/train.py -n 1 -c S -o trained_models/shakespeare/interpolated/interpolated_1_s -m in
python scripts/train.py -n 2 -c S -o trained_models/shakespeare/interpolated/interpolated_2_s -m in
python scripts/train.py -n 3 -c S -o trained_models/shakespeare/interpolated/interpolated_3_s -m in
python scripts/train.py -n 4 -c S -o trained_models/shakespeare/interpolated/interpolated_4_s -m in
####################
python scripts/train.py -n 1 -c B -o trained_models/brown/ngram/ngram_1_b
python scripts/train.py -n 2 -c B -o trained_models/brown/ngram/ngram_2_b
python scripts/train.py -n 3 -c B -o trained_models/brown/ngram/ngram_3_b
python scripts/train.py -n 4 -c B -o trained_models/brown/ngram/ngram_4_b
python scripts/train.py -n 1 -c G -o trained_models/gutenberg/ngram/ngram_1_g
python scripts/train.py -n 2 -c G -o trained_models/gutenberg/ngram/ngram_2_g
python scripts/train.py -n 3 -c G -o trained_models/gutenberg/ngram/ngram_3_g
python scripts/train.py -n 4 -c G -o trained_models/gutenberg/ngram/ngram_4_g
python scripts/train.py -n 1 -c S -o trained_models/shakespeare/ngram/ngram_1_s
python scripts/train.py -n 2 -c S -o trained_models/shakespeare/ngram/ngram_2_s
python scripts/train.py -n 3 -c S -o trained_models/shakespeare/ngram/ngram_3_s
python scripts/train.py -n 4 -c S -o trained_models/shakespeare/ngram/ngram_4_s
#############
python scripts/train.py -n 1 -c B -o trained_models/brown/backoff/backoff_1_b -m kz
python scripts/train.py -n 2 -c B -o trained_models/brown/backoff/backoff_2_b -m kz
python scripts/train.py -n 3 -c B -o trained_models/brown/backoff/backoff_3_b -m kz
python scripts/train.py -n 4 -c B -o trained_models/brown/backoff/backoff_4_b -m kz
python scripts/train.py -n 1 -c G -o trained_models/gutenberg/backoff/backoff_1_g -m kz
python scripts/train.py -n 2 -c G -o trained_models/gutenberg/backoff/backoff_2_g -m kz
python scripts/train.py -n 3 -c G -o trained_models/gutenberg/backoff/backoff_3_g -m kz
python scripts/train.py -n 4 -c G -o trained_models/gutenberg/backoff/backoff_4_g -m kz
python scripts/train.py -n 1 -c S -o trained_models/shakespeare/backoff/backoff_1_s -m kz
python scripts/train.py -n 2 -c S -o trained_models/shakespeare/backoff/backoff_2_s -m kz
python scripts/train.py -n 3 -c S -o trained_models/shakespeare/backoff/backoff_3_s -m kz
python scripts/train.py -n 4 -c S -o trained_models/shakespeare/backoff/backoff_4_s -m kz
##########
python scripts/train.py -n 1 -c B -o trained_models/brown/addone/addone_1_b -m ao
python scripts/train.py -n 2 -c B -o trained_models/brown/addone/addone_2_b -m ao
python scripts/train.py -n 3 -c B -o trained_models/brown/addone/addone_3_b -m ao
python scripts/train.py -n 4 -c B -o trained_models/brown/addone/addone_4_b -m ao
python scripts/train.py -n 1 -c G -o trained_models/gutenberg/addone/addone_1_g -m ao
python scripts/train.py -n 2 -c G -o trained_models/gutenberg/addone/addone_2_g -m ao
python scripts/train.py -n 3 -c G -o trained_models/gutenberg/addone/addone_3_g -m ao
python scripts/train.py -n 4 -c G -o trained_models/gutenberg/addone/addone_4_g -m ao
python scripts/train.py -n 1 -c S -o trained_models/shakespeare/addone/addone_1_s -m ao
python scripts/train.py -n 2 -c S -o trained_models/shakespeare/addone/addone_2_s -m ao
python scripts/train.py -n 3 -c S -o trained_models/shakespeare/addone/addone_3_s -m ao
python scripts/train.py -n 4 -c S -o trained_models/shakespeare/addone/addone_4_s -m ao
