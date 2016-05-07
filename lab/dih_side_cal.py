#coding: UTF-8
# -----syn, antiの割合の平均値を出す-----

#Syn計算
def calculateSyn(fName):


#Anti計算
def calculateAnti(fName):




#main関数
print "What's a reading File?\n"
fileName = raw_input() #ファイル名直接入力

ave_syn = calculateSyn(fileName)
ave_anti = calculateAnti(fileName)

print "Ave_syn = %f\n" % (ave_syn)
print "Ave_anti = %f\n" % (ave_anti)
