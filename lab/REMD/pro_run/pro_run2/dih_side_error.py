import math
def error(n):
    dx = 0.0
    for i in range(20):
        dx += n[i]
    dx = dx / 20.0
    sum = 0.0
    for i in range(20):
        sum += ((n[i] - dx) ** 2)

    dif = sum / 19.0
    return math.sqrt(dif)

sum_syn = 0
sum_anti = 0
sam_syn = 0
sam_anti = 0
n = 20
x = n*[0]
y = n*[0]
i = 0
j = 0
fname = "dih_side.txt"
for f in open(fname,"r"):
    data = f.split()
    dih = float(data[1])
    if -90.0 < dih < 90.0:
        sum_syn += 1
        sam_syn += 1
    else:
        sum_anti += 1
        sam_anti += 1
    i += 1
    if i == 500:
        x[j] = sam_syn / 500.0
        y[j] = sam_anti / 500.0
        j += 1
        sam_syn = 0
        sam_anti = 0
        i = 0
#for i in range(20):
#    print "x[%d] = %lf y[%d] = %lf" % (i,x[i],i,y[i])

ave_syn = sum_syn / 10000.0
ave_anti = sum_anti / 10000.0

print "ave_syn = %lf  +-%lf" % (ave_syn,error(x))
print "ave_anti= %lf  +-%lf" % (ave_anti,error(y))
