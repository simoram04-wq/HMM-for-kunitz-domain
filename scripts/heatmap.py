#!/Users/simonaramella/anaconda3/bin/python

#hetamap for the selected treshold

import seaborn as sns
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if len(sys.argv)!= 5: raise IndexError('the script take as input two file <__.results> and an <__.pdf> output file and a th of interest, in this order')

def heatmap(input_file1, input_file2, output_file, th):

#file reading
    values1=[]
    with open(input_file1, 'r') as f:
        for line in f:
            v=line.rstrip().split('\t')
            if float(v[0])==float(th):
                values1.append([[int(v[9]),int(v[10])],[int(v[11]),int(v[8])]])
    cm1=np.array(values1[0])

    values2=[]
    with open(input_file2, 'r') as f:
        for line in f:
            v=line.rstrip().split('\t')
            if float(v[0])==float(th):
                values2.append([[int(v[9]),int(v[10])],[int(v[11]),int(v[8])]])
    cm2=np.array(values2[0])

# heatmap construction
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    sns.heatmap(cm1, annot=True, fmt="d", cmap="Blues", ax=axes[0], cbar=False,
                xticklabels=["Pred Neg", "Pred Pos"],
                yticklabels=["True Neg", "True Pos"])
    axes[0].set_title(f"Heatmap th: {th} - Validation set 1")
    axes[0].set_xlabel("Predicted label")
    axes[0].set_ylabel("True label")

    sns.heatmap(cm2, annot=True, fmt="d", cmap="Greens", ax=axes[1], cbar=False,
                xticklabels=["Pred Neg", "Pred Pos"],
                yticklabels=["True Neg", "True Pos"])
    axes[1].set_title(f"Heatmap th: {th} - Validation set 2")
    axes[1].set_xlabel("Predicted label")
    axes[1].set_ylabel("True label")

    plt.tight_layout()
    #plt.savefig("confusion_matrices.pdf")
    plt.savefig(output_file, dpi=300)

if __name__=='__main__':
    input_file1=sys.argv[1]
    input_file2=sys.argv[2]
    output_file=sys.argv[3]
    th=sys.argv[4]
    heatmap(input_file1, input_file2, output_file,th)
    
    
 