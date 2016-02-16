#! /bin/bash

for a in $(ls ./trained_models)
do
    for b in $(ls ./trained_models/$a)
    do 
	for c in $(ls ./trained_models/$a/$b)
	do python scripts/eval.py -i trained_models/$a/$b/$c >> reports/"REPORT_"$c".txt"
	done
    done
done

cd reports

cat REPORT_add*_b* > addone_brown.txt
cat REPORT_add*_s* > addone_shakespeare.txt
cat REPORT_add*_g* > addone_gutenberg.txt

cat REPORT_kn*_b* > kneserney_brown.txt
cat REPORT_kn*_s* > kneserney_shakespeare.txt
cat REPORT_kn*_g* > kneserney_gutenberg.txt

cat REPORT_ng*_b* > ngram_brown.txt
cat REPORT_ng*_s* > ngram_shakespeare.txt
cat REPORT_ng*_g* > ngram_gutenberg.txt

cat REPORT_int*_b* > interpolated_brown.txt
cat REPORT_int*_s* > interpolated_shakespeare.txt
cat REPORT_int*_g* > interpolated_gutenberg.txt

cat REPORT_ba*_b* > backoff_brown.txt
cat REPORT_ba*_s* > backoff_shakespeare.txt
cat REPORT_ba*_g* > backoff_gutenberg.txt

rm R*
