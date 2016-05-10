#coding: UTF-8

# -----------関数処理-------------
#引数
def hello(name):
    print "hello " + name
    print "%s, I like you.\n" % (name)

def sex(name, num):
    return "%s, let's play SEX %d times!\n" % (name, num) * num

hello("Miku")
s = sex("Miku", 3)
print s
