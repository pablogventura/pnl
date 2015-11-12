echo "Evaluating models"
echo "\n"
echo "Flat model"

time python scripts/eval.py -i models/flat -m 20
echo "\n"
echo "RBranch model"

time python scripts/eval.py -i models/rbranch -m 20
echo "\n"
echo "LBranch model"
time python scripts/eval.py -i models/lbranch -m 20
echo "\n"
echo "UPCFG model"
time python scripts/eval.py -i models/upcfg -m 20
echo "\n"
echo "UPCFG model with horizontal Markovization of order 0"
time python scripts/eval.py -i models/upcfg0 -m 20
echo "\n"
echo "UPCFG model with horizontal Markovization of order 1"
time python scripts/eval.py -i models/upcfg1 -m 20
echo "\n"
echo "UPCFG model with horizontal Markovization of order 2"
time python scripts/eval.py -i models/upcfg2 -m 20
echo "\n"
echo "UPCFG model with horizontal Markovization of order 3"
time python scripts/eval.py -i models/upcfg3 -m 20
echo "\n"
echo "UPCFG model with horizontal Markovization of order 4"
time python scripts/eval.py -i models/upcfg4 -m 20
