#!/usr/bin/env bash
######################################################################################

#Pipline for the construction and validation of the HMM starting from a MSA fasta file

#necessary files:
# For construction:
#- MSA fasta file: './output/alignment_consensus.fasta'
# For the validation:
#- Fasta file with sequences containing kunitz domain: './input_val/positive.fasta'
#- Fasta file with sequencing not containing kunitz domain: './input_val/negative.fasta'
#- python file for metrics evaluations: './scripts/performance.py'
# For the plots:
#- Roc curve: ./scripts/ROC.py 
#- Trade Off curve FP vs FN: ./scripts/FPvsFN.py 
#- Precision vs Recall curve: ./scripts/PvsR.py
#- Normalized heatmap for specific trashold: ./scripts/heatmap.py

#necessary softwers
#- HMMER must be installed 

#######################################################################################

#1. HMM CONSTRUCTION
#start from the correct directory
cd Desktop/Unibo_projects/lab1/

#build the HMM from the alignment file
hmmbuild ./output/model_consensus.hmm  ./output/alignment_consensus.fasta


#2. VALIDATION DATASETS CONSTRUCTION
# The model is applied on the positive and negative datasets  
hmmsearch --max --noali --tblout ./output_val/positive_kunitz.tbl -Z 1000 ./output/model_consensus.hmm ./input_val/Positive.fasta
hmmsearch --max --noali --tblout ./output_val/negative_kunitz.tbl -Z 1000 ./output/model_consensus.hmm ./input_val/Negative.fasta


# from the previosly created files we save the reported HMMER hits:
# Files Format: protein_id    evalue    true_label
# true_label = 1 for known Kunitz positives
# true_label = 0 for known negatives
grep -v '^#' ./output_val/positive_kunitz.tbl | awk '{print $1"\t"$8"\t1"}' |sort -R > ./output_val/positive_kunitz.match
grep -v '^#' ./output_val/negative_kunitz.tbl | awk '{print $1"\t"$8"\t0"}' > ./output_val/negative_kunitz.match


# We extract and sort all negative IDs from the original negative FASTA file and save them in a new file
grep '^>' ./input_val/negative.fasta | awk '{print $1}' | tr -d '>' | sort > ./output_val/negative_kunitz.ids

# We extract negative IDs that had HMMER hits and save them in a new file
awk '{print $1}' ./output_val/negative_kunitz.match | sort > ./output_val/negative_kunitz_match.ids

# We create file of negative proteins with no HMMER hit
# These are assigned an artificial bad E-value of 100 and true label 0
comm -23 <(sort ./output_val/negative_kunitz.ids) <(sort ./output_val/negative_kunitz_match.ids) \
| awk '{print $1"\t100\t0"}' > ./output_val/negative_kunitz.nonmatch

# We combine matched and nonmatched negatives, then shuffle
cat ./output_val/negative_kunitz.match ./output_val/negative_kunitz.nonmatch | sort -R > ./output_val/negative_kunitz.tot.match

# We check dataset counts
echo "Original FASTA counts:"
grep -c '^>' ./input_val/positive.fasta
grep -c '^>' ./input_val/negative.fasta

echo "Evaluation file counts:"
wc -l ./output_val/positive_kunitz.match
wc -l ./output_val/negative_kunitz.match
wc -l ./output_val/negative_kunitz.nonmatch
wc -l ./output_val/negative_kunitz.tot.match

# Positives are split into two validation sets
head -n 199 ./output_val/positive_kunitz.match > ./val_sets/kunitz_set_1.txt
tail -n 199 ./output_val/positive_kunitz.match > ./val_sets/kunitz_set_2.txt

# Negatives are added to the two validation sets
head -n 287115 ./output_val/negative_kunitz.tot.match >> ./val_sets/kunitz_set_1.txt
tail -n 287115 ./output_val/negative_kunitz.tot.match >> ./val_sets/kunitz_set_2.txt

# We check the validation set sizes and label distributions
echo "Validation set sizes:"
wc -l ./val_sets/kunitz_set_1.txt
wc -l ./val_sets/kunitz_set_2.txt

echo "Validation set 1 labels:"
awk '{print $3}' ./val_sets/kunitz_set_1.txt | sort | uniq -c

echo "Validation set 2 labels:"
awk '{print $3}' ./val_sets/kunitz_set_2.txt | sort | uniq -c

# 3. PERFORMANCE EVALUATION

touch ./val_sets/kunitz_set_1.results
for i in $(seq 1 15); do
    python3 ./scripts/performance.py ./val_sets/kunitz_set_1.txt 1e-$i ./val_sets/kunitz_set_1.results
done 

touch ./val_sets/kunitz_set_2.results
for i in $(seq 1 15); do
    python3 ./scripts/performance.py ./val_sets/kunitz_set_2.txt 1e-$i ./val_sets/kunitz_set_2.results
done 

# inspection of the results
echo "Performance results for validation set 1:"
cat ./val_sets/kunitz_set_1.results

echo "Performance results for validation set 2:"
cat ./val_sets/kunitz_set_2.results

# 4. PLOTS

#ROC curve
python ./scripts/ROC.py ./val_sets/kunitz_set_1.results ./val_sets/kunitz_set_2.results ./images/ROC.pdf

#Precision Recall graph
python ./scripts/PvsR.py ./val_sets/kunitz_set_1.results ./val_sets/kunitz_set_2.results ./images/PvsR.pdf

#False Negative vs False positive graph
python ./scripts/FPvsFN.py ./val_sets/kunitz_set_1.results ./val_sets/kunitz_set_2.results ./images/TradeOFF.pdf

#heatmap for th
python ./scripts/heatmap.py ./val_sets/kunitz_set_1.results ./val_sets/kunitz_set_2.results ./images/heatmap.pdf 1e-5


# We make it execyutable and run it
#chmod +x ./scripts/kunitz.sh
#./scripts/kunitz.sh






