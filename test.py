import numpy

a=[1,2,3,45,1,3,54,0,1]
b=[]
#y=[a.pop(i) for i in range(len(a)) if a[i]>10]
for one in a:
    if one<=10:
        b.append(one)
a=b
print a