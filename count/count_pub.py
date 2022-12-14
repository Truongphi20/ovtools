import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import argparse

def ReadCount(file_csv): # Doc file dem csv
    year = []
    count = []
    with open(file_csv) as t:
        next(t)
        next(t)
        for line in t:
            aline = line.rstrip().split(",")
            year.append(aline[0])
            count.append(int(aline[1]))
    #print(year)
    #print(count)
    return year[::-1], count[::-1]

# Initialize parser
parser = argparse.ArgumentParser()

parser.add_argument("-g", "--global_file")
parser.add_argument("-n", "--vn_file")
parser.add_argument("-v",'--version', action='version', version='%(prog)s 1.0',help = 'show version')

# Read arguments from command line
args = parser.parse_args()


year_global, count_global = ReadCount(args.global_file) # Doc du lieu file tong tat ca
#print(year_global)
#print(count_global)

step_min = min(count_global)
step_max = max(count_global) 

year_vn, count_vn = ReadCount(args.vn_file) # Doc du lieu file tong tat ca
#print(year_vn)
#print(count_vn)

## Tru so luong cac nam co vn de ve stack bar
indexs = [i for i in range(len(year_global)) if year_global[i] in year_vn] # index cac nam trung
#print(indexs)

count_global_pre = [] # Chinh sua count global
count_vn_pre = [] # Chinh sua count vn
for i in range(len(count_global)):
    if i not in indexs:
        count_global_pre.append(count_global[i])
        count_vn_pre.append(0)
    else:
        count_global_pre.append(count_global[i]-count_vn[indexs.index(i)])
        count_vn_pre.append(count_vn[indexs.index(i)])
#print(count_global_pre)
#print(count_vn_pre)

## Ve stackbar
data = pd.DataFrame(zip(year_global,count_global_pre,count_vn_pre),columns=["Năm","Quốc tế","Việt Nam"]) # Tao dataframe
#print(data)


# plot data in stack manner of bar type
data.plot(x='Năm', kind='bar', stacked=True, zorder = 3)

#plt.xticks(rotation = 45) # Rotates X-Axis Ticks by 45-degrees
plt.yticks(np.arange(step_min, step_max+1, 1))
plt.grid(zorder=0, axis="y")
plt.show()

