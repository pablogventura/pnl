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

echo "training memm models order n € {1,2,3,4} and Logistic Regression classifier"
python scripts/train.py -m memm -n 1 -c lr -o models/m1clr
python scripts/train.py -m memm -n 2 -c lr -o models/m2clr
python scripts/train.py -m memm -n 3 -c lr -o models/m3clr
python scripts/train.py -m memm -n 4 -c lr -o models/m4clr

echo "training memm models order n € {1,2,3,4} and MultinomialNB classifier"
python scripts/train.py -m memm -n 1 -c mnb -o models/m1mnb
python scripts/train.py -m memm -n 2 -c mnb -o models/m2mnb
python scripts/train.py -m memm -n 3 -c mnb -o models/m3mnb
python scripts/train.py -m memm -n 4 -c mnb -o models/m4mnb

echo "training memm models order n € {1,2,3,4} and Linear SVC classifier"
python scripts/train.py -m memm -n 1 -c lsvc -o models/m1lsvc
python scripts/train.py -m memm -n 2 -c lsvc -o models/m2lsvc
python scripts/train.py -m memm -n 3 -c lsvc -o models/m3lsvc
python scripts/train.py -m memm -n 4 -c lsvc -o models/m4lsvc
