#! /bin/bash
echo "Training Model 1-Gram"
python scripts/train.py -n 1 -o m1g
echo "Training Model 2-Gram"
python scripts/train.py -n 2 -o m2g
echo "Training Model 3-Gram"
python scripts/train.py -n 3 -o m3g
echo "Training Model 4-Gram"
python scripts/train.py -n 4 -o m4g
echo "Training Model 1-AddOneNGram"
python scripts/train.py -n 1 -o m1aog -m addone
echo "Training Model 2-AddOneNGram"
python scripts/train.py -n 2 -o m2aog -m addone
echo "Training Model 3-AddOneNGram"
python scripts/train.py -n 3 -o m3aog -m addone
echo "Training Model 4-AddOneNGram"
python scripts/train.py -n 4 -o m4aog -m addone
#echo "Trainig Interpolated model with order 1"
#python scripts/train.py -n 3 -o tr3aogr -m addone

echo "Trainig Interpolated model with order 2"
#python scripts/train.py -n 3 -o tr3aogr -m addone

echo "Trainig Interpolated model with order 3"
#python scripts/train.py -n 3 -o tr3aogr -m addone



echo "Computing perplexity now..."
python scripts/eval.py -i m1g
python scripts/eval.py -i m2g
python scripts/eval.py -i m3g
python scripts/eval.py -i m4g

python scripts/eval.py -i m1aog
python scripts/eval.py -i m2aog
python scripts/eval.py -i m3aog
python scripts/eval.py -i m4aog
