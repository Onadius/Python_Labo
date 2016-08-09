fname = "allout.txt"
fname1 = "Etot.txt"
fname2 = "EPtot.txt"
fname3 = "BOND.txt"
fname4 = "ANGLE.txt"
fname5 = "DIHED.txt"
fname6 = "1-4NB.txt"
fname7 = "1-4EEL.txt"
fname8 = "VDWAALS.txt"
fname9 = "EELEC.txt"
fname10 = "EGB.txt"
f1 = open(fname1,"w")
f2 = open(fname2,"w")
f3 = open(fname3,"w")
f4 = open(fname4,"w")
f5 = open(fname5,"w")
f6 = open(fname6,"w")
f7 = open(fname7,"w")
f8 = open(fname8,"w")
f9 = open(fname9,"w")
f10 = open(fname10,"w")

ang = [-180]*10
for f in open(fname,"r"):
    x = f.split()
    for i in range(len(x)):
        if x[i] == "Etot":
            f1.write(str(ang[0]) + " " + str(x[i+2]) + "\n")
            ang[0] += 1
        elif x[i] == "EPtot":
            f2.write(str(ang[1]) + " " + str(x[i+2]) + "\n")
            ang[1] += 1
        elif x[i] == "BOND":
            f3.write(str(ang[2]) + " " + str(x[i+2]) + "\n")
            ang[2] += 1
        elif x[i] == "ANGLE":
            f4.write(str(ang[3]) + " " + str(x[i+2]) + "\n")
            ang[3] += 1
        elif x[i] == "DIHED":
            f5.write(str(ang[4]) + " " + str(x[i+2]) + "\n")
            ang[4] += 1
        elif x[i] == "NB":
            f6.write(str(ang[5]) + " " + str(x[i+2]) + "\n")
            ang[5] += 1
        elif x[i] == "EEL":
            f7.write(str(ang[6]) + " " + str(x[i+2]) + "\n")
            ang[6] += 1
        elif x[i] == "VDWAALS":
            f8.write(str(ang[7]) + " " + str(x[i+2]) + "\n")
            ang[7] += 1
        elif x[i] == "EELEC":
            f9.write(str(ang[8]) + " " + str(x[i+2]) + "\n")
            ang[8] += 1
        elif x[i] == "EGB":
            f10.write(str(ang[9]) + " " + str(x[i+2]) + "\n")
            ang[9] += 1

f1.close()
f2.close()
f3.close()
f4.close()
f5.close()
f6.close()
f7.close()
f8.close()
f9.close()
f10.close()

Etot = []
EPtot = []
BOND = []
ANGLE = []
DIHED = []
NB = []
EEL = []
VDWAALS = []
EELEC = []
EGB = []

for f in open(fname1,"r"):
    x = f.split()
    Etot.append(x[1])
for f in open(fname2,"r"):
    x = f.split()
    EPtot.append(x[1])
for f in open(fname3,"r"):
    x = f.split()
    BOND.append(x[1])
for f in open(fname4,"r"):
    x = f.split()
    ANGLE.append(x[1])
for f in open(fname5,"r"):
    x = f.split()
    DIHED.append(x[1])
for f in open(fname6,"r"):
    x = f.split()
    NB.append(x[1])
for f in open(fname7,"r"):
    x = f.split()
    EEL.append(x[1])
for f in open(fname8,"r"):
    x = f.split()
    VDWAALS.append(x[1])
for f in open(fname9,"r"):
    x = f.split()
    EELEC.append(x[1])
for f in open(fname10,"r"):
    x = f.split()
    EGB.append(x[1])

a = -180
fname11 = "all_result.txt"
f = open(fname11,"w")
f.write("dih  Etot    EPtot   BOND   ANGLE  DIHED   1-4NB  1-4EEL  VDWAALS  EELEC EGB\n")
for i in range(0,361):
    f.write(str(a) + " " + str(Etot[i]) + " " + str(EPtot[i]) + " " + str(BOND[i]) + " " + str(ANGLE[i]) + " " + str(DIHED[i]) + " " + str(NB[i]) + " " + str(EEL[i]) + " " + str(VDWAALS[i]) + " " + str(EELEC[i]) + " " + str(EGB[i]) + "\n")
    a += 1
f.close()

fname12 = "EP_res.txt"
f = open(fname12,"w")
a = -180
n = float(EPtot[0])
for i in range(0,361):
    f.write(str(a) + " " + str(float(EPtot[i]) - n) + "\n")
    a += 1
f.close()
