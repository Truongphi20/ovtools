from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

def CheckSec(word1,word2): # Check tu thu 2 cua 2 chu
    ans = False
    if word1.split(" ")[1] == word2.split(" ")[1]:
        ans = True
    return ans
#print(CheckSec('Enterococcus faecium', 'E. faecium'))

def Locten(lis):# Loc ten duy nhat trong list
    ten_sec = []
    ten_fir = []
    for t in lis:
        if t.split(" ")[1] in ten_sec:
            if len(t.split(" ")[0]) > len(ten_fir[ten_sec.index(t.split(" ")[1])]):
                ten_fir[ten_sec.index(t.split(" ")[1])] = t.split(" ")[0]
        else:
            ten_fir.append(t.split(" ")[0])
            ten_sec.append(t.split(" ")[1])
    #print(ten_fir)
    #print(ten_sec)

    name_sort = [ten_fir[i] + " " + ten_sec[i] for i in range(len(ten_fir))]
    #print(name_sort)
    return name_sort
#print(Locten(lis))

def Sort_2_list(list1,list2):

    index = list(range(len(list1)))
    #print(index)

    index.sort(key = list1.__getitem__)
    #print(index)

    list1[:] = [list1[i] for i in index]
    list2[:] = [list2[i] for i in index]

    #print(list1)
    #print(list2)
    return list1, list2

## Doc du lieu
daa = []
with open("useful_org.txt") as file:
    for line in file:
        tem = line.rstrip().split(", ")
        for i in range(len(tem)):
            if len(tem[i]) > 0 and tem[i][-1] == ".":
                tem[i] = tem[i][:-1]
        daa.append(tem)
#print(daa)

lib = {}
for lis in daa:
    if len(lis) > 1:
        name = Locten(lis) # Ten duy nhat cua vi khuan
        #print(name)
        for ten in name:
            if ten not in lib:
                lib[ten] = 1
            else:
                lib[ten] += 1
        #print(lib)
#print(lib)

## Vẽ biểu đồ histogram
name_bac = [key for key in lib] # Ten vi khuan probiotic
#print(name_bac)
name_hist = [name.split(" ")[0][0] + ". " + name.split(" ")[1] for name in name_bac]
#print(name_hist)

mount = [lib[i] for i in name_bac] # So luong bai bao nghien cuu
#print(mount)
mounta, name_hista = Sort_2_list(mount, name_hist)
#print(mounta)
#print(name_hista)

# Figure Size

data = pd.DataFrame(zip(mounta, name_hista),columns=["Sl","name"]) # Tao dataframe
# Horizontal Bar Plot
data.plot(x='name', kind='bar', zorder = 3)
plt.xticks(rotation = 45, ha='right') # Rotates X-Axis Ticks by 45-degrees
plt.yticks(np.arange(min(mounta), max(mounta)+1, 1))
plt.xlabel("")
plt.legend('')
plt.grid(zorder=0, axis="y")
# Show Plot
plt.show()
