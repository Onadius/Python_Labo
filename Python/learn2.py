# coding: UTF-8


# -----数値 - 整数、小数、複素数の扱いについて------
#演算子 + - * / // % **
# 整数と少数の演算 -> 小数の結果
# 整数同士の割り算 -> 切り捨ての整数


print 10 * 5
print 2 ** 3
print 10 / 5



# -----文字列について-----
# 日本語   u"こんにちは"
# + *（繰り返す）
# エスケープ \n \t \\

print u"イク！" * 10

# 3つの"""で囲むと便利
print """<html lang="ja">
<body>
</body>
</html>"""

# 文字数 len
# 検索 find
# 切り出し ｛｝
word = "shikoshikoonani"
print len(word)
print word.find("a")
print word[:5]
