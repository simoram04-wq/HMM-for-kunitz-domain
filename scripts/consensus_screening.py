### F*Y*GC****N*F*****C
#ACDEFGHIKLMNQRSTVWYP

import pandas as pd
from sys import argv
from re import *

if len(argv)!= 2:
    raise IndexError('Correct imput line: python <script-name.py> <imput-file-name.csv> \nThe output of the script will be a file named output.txt')

imput_file=argv[1]

#read file
raw_table= pd.read_csv(imput_file)
#set columns names and drop the first row
raw_table.columns=raw_table.iloc[0]
raw_table = raw_table[1:].copy()
#raw_table= raw_table.drop(raw_table.index[0])

#drop na values and empty strings in the "Sequence" column 
# filter sequences with length between 40 and 80
raw_table = raw_table[raw_table["Sequence"].notna()]
raw_table = raw_table[raw_table["Sequence"].astype(str).str.strip() != ""]
raw_table = raw_table[raw_table["Sequence"].astype(str).str.len().between(40, 80)]
#drop na values in the "Entry ID" column
final_table = raw_table.dropna(subset=["Entry ID"])
final_table = final_table.reset_index(drop=True)
print(final_table['Sequence'].iloc[1])

df = pd.DataFrame(columns=['Entry ID', 'Sequence', 'Auth Asym ID', 'Entity ID', 'nan'])
pattern='F.Y.GC.{4}N.F.{5}C'
#filter out sequence without the pattern
for i in range(final_table.shape[0]):
    print(i)
    seq=final_table['Sequence'].iloc[i]
    match = search(pattern, seq)
    if match:
        row=final_table.iloc[i]
        df.loc[len(df)] = row

with open('output_consensus.txt', 'w') as file:
        for i in range(df.shape[0]):
            file.write('>'+df['Entry ID'].iloc[i]+':'+df['Auth Asym ID'].iloc[i]+'\n'+df['Sequence'].iloc[i]+'\n')


print(df.shape)
print(df)



