echo "Training models"

time python scripts/train.py -o models/flat
echo "\n"
time python scripts/train.py -m rbranch -o models/rbranch
echo "\n"
time python scripts/train.py -m lbranch -o models/lbranch

time python scripts/train.py -m upcfg -o models/upcfg

time python scripts/train.py -m upcfg -H 0 -o models/upcfg0

time python scripts/train.py -m upcfg -H 1 -o models/upcfg1

time python scripts/train.py -m upcfg -H 2 -o models/upcfg2

time python scripts/train.py -m upcfg -H 3 -o models/upcfg3

time python scripts/train.py -m upcfg -H 4 -o models/upcfg4
