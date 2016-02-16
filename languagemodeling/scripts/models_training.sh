#! /bin/bash

python scripts/train.py -n 1 -c B -o trained_models/brown/kneserney_1_b -m kn -D 1
python scripts/train.py -n 2 -c B -o trained_models/brown/kneserney_2_b -m kn -D 1
python scripts/train.py -n 3 -c B -o trained_models/brown/kneserney_3_b -m kn -D 1
python scripts/train.py -n 4 -c B -o trained_models/brown/kneserney_4_b -m kn -D 1
python scripts/train.py -n 1 -c G -o trained_models/gutenberg/kneserney_1_g -m kn -D 1
python scripts/train.py -n 2 -c G -o trained_models/gutenberg/kneserney_2_g -m kn -D 1
python scripts/train.py -n 3 -c G -o trained_models/gutenberg/kneserney_3_g -m kn -D 1
python scripts/train.py -n 4 -c G -o trained_models/gutenberg/kneserney_4_g -m kn -D 1
python scripts/train.py -n 1 -c S -o trained_models/shakespeare/kneserney_1_s -m kn -D 1
python scripts/train.py -n 2 -c S -o trained_models/shakespeare/kneserney_2_s -m kn -D 1
python scripts/train.py -n 3 -c S -o trained_models/shakespeare/kneserney_3_s -m kn -D 1
python scripts/train.py -n 4 -c S -o trained_models/shakespeare/kneserney_4_s -m kn -D 1
#############
python scripts/train.py -n 1 -c B -o trained_models/brown/interpolated_1_b -m in
python scripts/train.py -n 2 -c B -o trained_models/brown/interpolated_2_b -m in
python scripts/train.py -n 3 -c B -o trained_models/brown/interpolated_3_b -m in
python scripts/train.py -n 4 -c B -o trained_models/brown/interpolated_4_b -m in
python scripts/train.py -n 1 -c G -o trained_models/gutenberg/interpolated_1_g -m in
python scripts/train.py -n 2 -c G -o trained_models/gutenberg/interpolated_2_g -m in
python scripts/train.py -n 3 -c G -o trained_models/gutenberg/interpolated_3_g -m in
python scripts/train.py -n 4 -c G -o trained_models/gutenberg/interpolated_4_g -m in
python scripts/train.py -n 1 -c S -o trained_models/shakespeare/interpolated_1_s -m in
python scripts/train.py -n 2 -c S -o trained_models/shakespeare/interpolated_2_s -m in
python scripts/train.py -n 3 -c S -o trained_models/shakespeare/interpolated_3_s -m in
python scripts/train.py -n 4 -c S -o trained_models/shakespeare/interpolated_4_s -m in
####################
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
#############
python scripts/train.py -n 1 -c B -o trained_models/brown/backoff_1_b -m kz
python scripts/train.py -n 2 -c B -o trained_models/brown/backoff_2_b -m kz
python scripts/train.py -n 3 -c B -o trained_models/brown/backoff_3_b -m kz
python scripts/train.py -n 4 -c B -o trained_models/brown/backoff_4_b -m kz
python scripts/train.py -n 1 -c G -o trained_models/gutenberg/backoff_1_g -m kz
python scripts/train.py -n 2 -c G -o trained_models/gutenberg/backoff_2_g -m kz
python scripts/train.py -n 3 -c G -o trained_models/gutenberg/backoff_3_g -m kz
python scripts/train.py -n 4 -c G -o trained_models/gutenberg/backoff_4_g -m kz
python scripts/train.py -n 1 -c S -o trained_models/shakespeare/backoff_1_s -m kz
python scripts/train.py -n 2 -c S -o trained_models/shakespeare/backoff_2_s -m kz
python scripts/train.py -n 3 -c S -o trained_models/shakespeare/backoff_3_s -m kz
python scripts/train.py -n 4 -c S -o trained_models/shakespeare/backoff_4_s -m kz
##########
python scripts/train.py -n 1 -c B -o trained_models/brown/addone_1_b -m ao
python scripts/train.py -n 2 -c B -o trained_models/brown/addone_2_b -m ao
python scripts/train.py -n 3 -c B -o trained_models/brown/addone_3_b -m ao
python scripts/train.py -n 4 -c B -o trained_models/brown/addone_4_b -m ao
python scripts/train.py -n 1 -c G -o trained_models/gutenberg/addone_1_g -m ao
python scripts/train.py -n 2 -c G -o trained_models/gutenberg/addone_2_g -m ao
python scripts/train.py -n 3 -c G -o trained_models/gutenberg/addone_3_g -m ao
python scripts/train.py -n 4 -c G -o trained_models/gutenberg/addone_4_g -m ao
python scripts/train.py -n 1 -c S -o trained_models/shakespeare/addone_1_s -m ao
python scripts/train.py -n 2 -c S -o trained_models/shakespeare/addone_2_s -m ao
python scripts/train.py -n 3 -c S -o trained_models/shakespeare/addone_3_s -m ao
python scripts/train.py -n 4 -c S -o trained_models/shakespeare/addone_4_s -m ao
