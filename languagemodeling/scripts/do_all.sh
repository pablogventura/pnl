#! /bin/bash
echo ""
echo ""
echo "################################################################################################################"
echo "WARNING: This may take a while. About 2:30 hours in create all the models and about 30 minutes in evaluate them."
echo "################################################################################################################"
echo ""
echo ""
echo "Training Models..."
sh scripts/models_train.sh
echo ""
echo "Evaluating Models..."
sh scripts/models_eval.sh
