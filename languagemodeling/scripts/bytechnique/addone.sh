#! /bin/bash

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
