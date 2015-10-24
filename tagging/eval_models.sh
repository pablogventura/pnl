#! /bin/bash

echo "evaluating mlhmm models order n € {1,2,3,4} with addone"
python scripts/eval.py -i models/m1a1
python scripts/eval.py -i models/m2a1
python scripts/eval.py -i models/m3a1
python scripts/eval.py -i models/m4a1

echo "evaluating mlhmm models order n € {1,2,3,4} without addone"
python scripts/eval.py -i models/m1a0
python scripts/eval.py -i models/m2a0
python scripts/eval.py -i models/m3a0
python scripts/eval.py -i models/m4a0

echo "evaluating memm models order n € {1,2,3,4} with Logistic Regression Classifier"
python scripts/eval.py -i models/m1clr
python scripts/eval.py -i models/m2clr
python scripts/eval.py -i models/m3clr
python scripts/eval.py -i models/m4clr

echo "evaluating memm models order n € {1,2,3,4} with Multinomial NB Classifier"
python scripts/eval.py -i models/m1mnb
python scripts/eval.py -i models/m2mnb
python scripts/eval.py -i models/m3mnb
python scripts/eval.py -i models/m4mnb

echo "evaluating memm models order n € {1,2,3,4} with Linear SVC Classifier"
python scripts/eval.py -i models/m1lsvc
python scripts/eval.py -i models/m2lsvc
python scripts/eval.py -i models/m3lsvc
python scripts/eval.py -i models/m4lsvc
