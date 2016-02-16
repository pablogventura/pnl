#! /bin/bash

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
