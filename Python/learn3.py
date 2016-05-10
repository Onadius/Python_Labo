# coding: UTF-8

# 数値 <> 文字列
# 文字列 -> 数字 int float
#数値 -> 文字列 str

print 39 + int("1")
print 39 + float("1")

# データの型を意識する必要がある
age = 20
print "I am " + str(age) + " years old."


# --------リスト（配列）-------
vocaloid = [39, 3939, 3.9, 393]
print len(vocaloid)
print vocaloid[2]

vocaloid[2] = "len"
print vocaloid[2]

# in
print 3939 in vocaloid #true

#range
print range(39, 49, 2) #[39, 41, 43, 45, 47]

# sort/reverse
vocaloid.sort()
print vocaloid

# 文字列とリスト
date = "2016/5/5"
print date.split("/") #文字列をリストに変換

vo = ["miku", "rin", "ruka"]
print "-".join(vo) #リストを文字列に変換した
