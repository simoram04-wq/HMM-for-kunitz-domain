#!/Users/simonaramella/anaconda3/bin/python

#script for false positive vs false negative where x is e-value trashold and y is units

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if len(sys.argv)!= 4: raise IndexError('the script take as input two file <__.results> and an <__.pdf> output file')

def tradeOFF(input_file1, input_file2, output_file):

#file reading
    values1 = {}
    with open(input_file1, 'r') as f:
        for line in f:
            v=line.rstrip().split('\t')
            values1[float(v[0])]={'th':float(v[0]), 'fp':float(v[10]), 'fn':float(v[11])}
    df1 = pd.DataFrame.from_dict(values1, orient='index')
    values2 = {}
    with open(input_file2, 'r') as f:
        for line in f:
            v=line.rstrip().split('\t')
            values2[float(v[0])]={'th':float(v[0]), 'fp':float(v[10]), 'fn':float(v[11])}
    df2 = pd.DataFrame.from_dict(values2, orient='index')

#graph construction
    fig, ax = plt.subplots()
    ax.plot(df1['th'], df1['fp'], marker='o', color='#ffca41', linewidth=1, label='FP - set 1')
    ax.plot(df1['th'], df1['fn'], marker="v", color='#ffca41',linestyle="--", linewidth=1, label='FN - set 1')
    ax.plot(df2['th'], df2['fp'], marker='o', color='#ff8a41', linewidth=1, label='FP - set 2')
    ax.plot(df2['th'], df2['fn'], marker="v", color='#ff8a41',linestyle="--", linewidth=1, label='FN - set 2')
    ax.set_xscale("log")
    ax.axvline(x=1e-5, color="green", linestyle="--", linewidth=1)
    ax.text(
    0.8e-5,
    30,                         # y-position: adjust for your graph
    "Chosen threshold\n1e-5",
    rotation=360,
    color="green",
    fontsize=6,
    verticalalignment="top",
    horizontalalignment="right"
)
    ax.set_title('Trade Off curve: False Positive vs False Negatives')
    ax.set_xlabel('Treashold value')
    ax.set_ylabel('Number of Errors')

    ax.grid(True, which="both", ls="--", alpha=0.35)
    ax.legend()
    plt.savefig(output_file, bbox_inches="tight")
    
    

if __name__=='__main__':
    input_file1=sys.argv[1]
    input_file2=sys.argv[2]
    output_file=sys.argv[3]
    tradeOFF(input_file1, input_file2, output_file)