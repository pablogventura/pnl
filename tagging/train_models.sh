#! /bin/bash
echo "training mlhmm models order n € {1,2,3,4} with addone (output model name struct: m-order-addone<1|0>)"
python scripts/train.py -m mlhmm -n 1 -a 1 -o models/m1a1
python scripts/train.py -m mlhmm -n 2 -a 1 -o models/m2a1
python scripts/train.py -m mlhmm -n 3 -a 1 -o models/m3a1
python scripts/train.py -m mlhmm -n 4 -a 1 -o models/m4a1

echo "training mlhmm models order n € {1,2,3,4} without addone (output model name struct: m-order-addone<1|0>)"
python scripts/train.py -m mlhmm -n 1 -a 0 -o models/m1a0
python scripts/train.py -m mlhmm -n 2 -a 0 -o models/m2a0
python scripts/train.py -m mlhmm -n 3 -a 0 -o models/m3a0
python scripts/train.py -m mlhmm -n 4 -a 0 -o models/m4a0
