#! /bin/bash

echo "evaluating mlhmm models order n € {1,2,3,4} with addone"
#python scripts/eval.py -i models/m1a1
python scripts/eval.py -i models/m2a1
python scripts/eval.py -i models/m3a1
python scripts/eval.py -i models/m4a1

echo "evaluating mlhmm models order n € {1,2,3,4} without addone"
#python scripts/eval.py -i models/m1a0
python scripts/eval.py -i models/m2a0
python scripts/eval.py -i models/m3a0
python scripts/eval.py -i models/m4a0
