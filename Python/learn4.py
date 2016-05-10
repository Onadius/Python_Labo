#coding: UTF-8


# -------タプル---------
# 要素の中身を変更できない

a = (2, 5, 8)
print len(a)

# タプル <> リスト

b = list(a)
print b

c = tuple(b)
print c

# --------セット--------
# セット（集合型）　重複を許さない
num1 = set([1, 2, 3, 4])
print num1

num2 = set([3, 4, 5])
print num1 - num2
print num1 | num2 #または
print num1 & num2 #且つ
print num1 ^ num2
