#coding: UTF-8
# -----syn, antiの標本平均より誤差算出-----

import math



#Syn計算
"""
def calculateSyn(fName):
    sum_syn = 0
    for file in open(fName,"r"):
        data = file.split()
        value = float(data[1])

        if -90.0 < value <90.0:
            sum_syn += 1

    ave_syn = sum_syn / 10000.0
    return ave_syn


#Anti計算
def calculateAnti(fName):
    sum_anti = 0
    for file in open(fName,"r"):#"r" -> 読み出し
        data = file.split()
        value = float(data[1])

        if value < -90.0 or value > 90.0:
            sum_anti += 1

    ave_anti = sum_anti / 10000.0
    return ave_anti
"""


#main関数
def main():

    print "Which is a reading File?\n"
    fileName = raw_input() #ファイル名直接入力

    samAve = calcAve_syn(fileName)

    print samAve

    """
    ave_syn = calculateSyn(fileName)
    ave_anti = calculateAnti(fileName)

    print "\nError_syn = %f" % (ave_syn)
    print "Error_anti = %f\n" % (ave_anti)
    """

#(scriptファイルとして実行すると、trueでif文以下実行)
if __name__ == '__main__':
    main()
