#coding: UTF-8

# -------forループ-------
nums = [12, 13, 1423, 123]
sum = 0
for num in nums:
    sum += num
else: #forが終わったらelse以下を一回だけ行う
    ave = sum/4
    print ave


# -----continue break-----
for n in range(6):
    if n == 3:
        continue #この条件の時は、無視してループ処理
    print n


# 辞書型データでループ処理
voc = {"miku":39, "rin":16, "ruka":300}
for key, value in voc.iteritems():
    print "key: %s value: %d\n" % (key, value)

# keyだけとってくる
for key in voc.iterkeys():
    print key
    print "key: %s\n" % (key)


# ------while文処理-------

a = 0
while a < 10:
    if a == 3 or a == 7:
        a += 1
        continue
    print a
    a +=1
else:
    print "end\n"
