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
