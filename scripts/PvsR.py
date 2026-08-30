#!/Users/simonaramella/anaconda3/bin/python

#script for Precision vs Recall curve

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if len(sys.argv)!= 4: raise IndexError('the script take as input two file <__.results> and an <__.pdf> output file')

def PvsR(input_file1, input_file2, output_file):

#file reading
    values1 = {}
    with open(input_file1, 'r') as f:
        for line in f:
            v=line.rstrip().split('\t')
            values1[float(v[0])]={'th':float(v[0]), 'recall':float(v[3]), 'precision':float(v[6])}
    df1 = pd.DataFrame.from_dict(values1, orient='index')
    values2 = {}
    with open(input_file2, 'r') as f:
        for line in f:
            v=line.rstrip().split('\t')
            values2[float(v[0])]={'th':float(v[0]), 'recall':float(v[3]), 'precision':float(v[6])}
    df2 = pd.DataFrame.from_dict(values2, orient='index')

#graph construction
    fig, ax = plt.subplots()
    ax.plot(df1['recall'], df1['precision'], marker='o', color='#ffca41', linewidth=2, label='set 1')
    ax.plot(df2['recall'], df2['precision'], marker='o', color='#ff8a41', linewidth=2, label='set 2')
    ax.set_ylim(0.86, 1.02)
    ax.set_title('Precision vs Recall')
    ax.set_xlabel('Recall')
    ax.set_ylabel('Precision')
    ax.grid(True, which="both", ls="--", alpha=0.5)
    ax.legend()
    plt.savefig(output_file, bbox_inches="tight")
    
    

if __name__=='__main__':
    input_file1=sys.argv[1]
    input_file2=sys.argv[2]
    output_file=sys.argv[3]
    PvsR(input_file1, input_file2, output_file)