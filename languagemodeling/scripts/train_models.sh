#! /bin/bash
echo "Training Model 1-Gram"
python scripts/train.py -n 1 -o trained_models/m1g
echo "Training Model 2-Gram"
python scripts/train.py -n 2 -o trained_models/m2g
echo "Training Model 3-Gram"
python scripts/train.py -n 3 -o trained_models/m3g
echo "Training Model 4-Gram"
python scripts/train.py -n 4 -o trained_models/m4g
echo "Training Model 1-AddOneNGram"
python scripts/train.py -n 1 -o trained_models/m1aog -m addone
echo "Training Model 2-AddOneNGram"
python scripts/train.py -n 2 -o trained_models/m2aog -m addone
echo "Training Model 3-AddOneNGram"
python scripts/train.py -n 3 -o trained_models/m3aog -m addone
echo "Training Model 4-AddOneNGram"
python scripts/train.py -n 4 -o trained_models/m4aog -m addone
echo "Training Model 1-InterpolatedNGram"
python scripts/train.py -n 1 -o trained_models/m1ig -m interpolated -a 1
echo "Training Model 2-InterpolatedNGram"
python scripts/train.py -n 2 -o trained_models/m2ig -m interpolated -a 1
echo "Training Model 3-InterpolatedNGram"
python scripts/train.py -n 3 -o trained_models/m3ig -m interpolated -a 1
echo "Training Model 4-InterpolatedNGram"
python scripts/train.py -n 4 -o trained_models/m4ig -m interpolated -a 1
echo "Training Model 1-BackOffNGram"
python scripts/train.py -n 1 -o trained_models/m1bog -m backoff -a 1
echo "Training Model 2-BackOffNGram"
python scripts/train.py -n 2 -o trained_models/m2bog -m backoff -a 1
echo "Training Model 3-BackOffNGram"
python scripts/train.py -n 3 -o trained_models/m3bog -m backoff -a 1
echo "Training Model 4-BackOffNGram"
python scripts/train.py -n 4 -o trained_models/m4bog -m backoff -a 1
