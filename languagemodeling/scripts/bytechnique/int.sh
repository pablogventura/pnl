#! /bin/bash

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
