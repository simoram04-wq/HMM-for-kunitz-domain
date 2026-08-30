#!/Users/simonaramella/anaconda3/bin/python

'''
This script is for the optimization
This script evaluates binary classification performance for a given E-value threshold.
Usage: python preformance.py <predictions_file> <threshold> 

Input file format:
protein_id    evalue    true_label
Where true_label is 1 for positive and 0 for negative.
'''

import sys
import numpy as np

def get_predictions(fname):
    '''Reads the the given file and returns a list of tuples (id, score)'''    
    preds = []
    fh = open(fname)
    for line in fh:
        v = line.strip().split()
        if len(v) != 3:
            continue
        preds.append((v[0], v[1], v[2]))
    return preds  

def get_confusion_matrix(preds, th=0.001):
    '''Returns the confusion matrix for the given predictions and threshold'''    
    confusion_matrix = np.zeros((2, 2), dtype=int)
    for k in range(len(preds)):
        j = 0
        i= int(preds[k][2])
        if float(preds[k][1]) <= th:
            j = 1
        confusion_matrix[i][j] += 1
    return confusion_matrix

def get_accuracy(confusion_matrix):
    '''Returns the accuracy for the given confusion matrix.'''
    return (confusion_matrix[0][0] + confusion_matrix[1][1]) / np.sum(confusion_matrix)

def get_mcc(confusion_matrix):
    '''Returns the Matthews correlation coefficient for the given confusion matrix.'''
    tp = confusion_matrix[1][1]
    tn = confusion_matrix[0][0]
    fp = confusion_matrix[0][1]
    fn = confusion_matrix[1][0]
    n = tp * tn - fp * fn
    d = np.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    return n / d if d != 0 else 0            

def get_metrics(confusion_matrix):
    '''Returns TP, FP, FN, TN  the accuracy and MCC for the given confusion matrix.'''
    tp = confusion_matrix[1][1]
    tn = confusion_matrix[0][0]
    fp = confusion_matrix[0][1]
    fn = confusion_matrix[1][0] 

    Sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    Specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    f1_score = 2 * (precision * Sensitivity) / (precision + Sensitivity) if (precision + Sensitivity) > 0 else 0

    return  Sensitivity, Specificity, fpr, precision, f1_score

if __name__ == "__main__":
    fname = sys.argv[1]
    threshold = float(sys.argv[2])
    results_file=sys.argv[3]
    preds = get_predictions(fname)
    confusion_matrix = get_confusion_matrix(preds, threshold)
    accuracy = get_accuracy(confusion_matrix)
    mcc = get_mcc(confusion_matrix)
    sensitivity, specificity, fpr, precision, f1_score = get_metrics(confusion_matrix)

    #informations are saved on txt file
    with open(results_file, 'a') as file:
        file.write(str(threshold)+'\t'+str(accuracy)+'\t'+str(mcc)+'\t'+str(sensitivity)+'\t'+str(specificity)+'\t'+str(fpr)+'\t'+str(precision)+'\t'+str(f1_score)+'\t'+str(confusion_matrix[1][1])+'\t'+str(confusion_matrix[0][0])+'\t'+str(confusion_matrix[0][1])+'\t'+str(confusion_matrix[1][0])+'\n')

    #same information are printed on screen for fast evaluation
    print(f"Threshold: {threshold}, Accuracy: {accuracy:}, MCC: {mcc:}")
    print(f"Sensitivity: {sensitivity:}, Specificity: {specificity:}, FPR: {fpr:}, Precision: {precision:}, F1 Score: {f1_score:}")
    print(f"Confusion Matrix:\n{confusion_matrix}")
