"Computing perplexity for:"
echo "1-Gram"
python scripts/eval.py -i trained_models/m1g
echo "2-Gram"
python scripts/eval.py -i trained_models/m2g
echo "3-Gram"
python scripts/eval.py -i trained_models/m3g
echo "4-Gram"
python scripts/eval.py -i trained_models/m4g
echo "AddOne 1-Gram"
python scripts/eval.py -i trained_models/m1aog
echo "AddOne 2-Gram"
python scripts/eval.py -i trained_models/m2aog
echo "AddOne 3-Gram"
python scripts/eval.py -i trained_models/m3aog
echo "AddOne 4-Gram"
python scripts/eval.py -i trained_models/m4aog
echo "Interpolated 1-Gram"
#python scripts/eval.py -i trained_models/m1ig
echo "Interpolated 2-Gram"
#python scripts/eval.py -i trained_models/m2ig
echo "Interpolated 3-Gram"
#python scripts/eval.py -i trained_models/m3ig
echo "Interpolated 4-Gram"
#python scripts/eval.py -i trained_models/m4ig
echo "BackOff (with discounting) 1-Gram"
#python scripts/eval.py -i trained_models/m1bog
echo "BackOff (with discounting) 2-Gram"
#python scripts/eval.py -i trained_models/m2bog
echo "BackOff (with discounting) 3-Gram"
#python scripts/eval.py -i trained_models/m3bog
echo "BackOff (with discounting) 4-Gram"
#python scripts/eval.py -i trained_models/m4bog
