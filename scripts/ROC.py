#!/Users/simonaramella/anaconda3/bin/python

#script for plots: ROC curve

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if len(sys.argv)!= 4: raise IndexError('the script take as input two file <__.results> and an <__.pdf> output file')

def roc_curve(input_file1, input_file2, output_file):

#file reading
    values1 = {}
    with open(input_file1, 'r') as f:
        for line in f:
            v=line.rstrip().split('\t')
            values1[float(v[0])]={'fpr':float(v[5]), 'tpr':float(v[3])}
    df1 = pd.DataFrame.from_dict(values1, orient='index')
    values2 = {}
    with open(input_file2, 'r') as f:
        for line in f:
            v=line.rstrip().split('\t')
            values2[float(v[0])]={'fpr':float(v[5]), 'tpr':float(v[3])}
    df2 = pd.DataFrame.from_dict(values2, orient='index')

    #df1["fpr_log"] = np.log10(df1['fpr'])
    #df2["fpr_log"] = np.log10(df2['fpr'])
    epsilon = 1e-7 
    df1['fpr_log'] = df1['fpr'].replace(0, epsilon)
    df2['fpr_log'] = df2['fpr'].replace(0, epsilon)


#graph creation
    fig, ax = plt.subplots()
    ax.plot(df1['fpr_log'], df1['tpr'], marker='o', color='#ffca41', linewidth=1.5, label='validation set 1')
    ax.plot(df2['fpr_log'], df2['tpr'], marker='o', color='#ff8a41', linewidth=1.5, label='validation set 2')
    ax.set_xscale('log')
    ax.set_xlim([epsilon / 2, max(df1['fpr'].max(),df2['fpr'].max()) * 2])
    ax.set_title('Semi Logaritmic ROC curve')
    ax.set_xlabel('False Positive Rate (FPR) - logaritmic scale')
    ax.set_ylabel('True Positive Rate (TPR) - linear scale')
    ax.grid(True, which="both", ls="--", alpha=0.5)
    ax.legend()
    plt.savefig(output_file, bbox_inches="tight")


if __name__=='__main__':
    input_file1=sys.argv[1]
    input_file2=sys.argv[2]
    output_file=sys.argv[3]
    roc_curve(input_file1, input_file2, output_file)

