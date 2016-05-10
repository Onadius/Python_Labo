#coding: UTF-8

# ------辞書------
# key value (json配列)
voc = {"miku":39, "rin":14}
print voc["miku"]

voc["rin"] = 16
print voc

# in
print "miku" in voc # -> True

# keyの一覧を取得
print voc.keys()
print voc.values()

# データ組み込み

a = 3939
b = 3.939
c = "ruka"

print "age: %d" % (a)
print "hatyune %f" % b
print "hatyune %.2f" % b
print "name: %s" % c

#辞書型に
print "level: %(rin)d" % (voc)
