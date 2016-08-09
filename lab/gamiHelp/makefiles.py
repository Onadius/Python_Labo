fname1 = "strfile.txt"
f = open(fname1,"w")
a = -180
for i in range(0,361):
	f.write("set default PBradii mbondi2" + "\n")
	f.write("str" + str(i) + " = sequence{ACE GLH NME}" + "\n")
	f.write("impose str" + str(i) + " {2} {{\"OE1\" \"CD\" \"OE2\" \"HE2\" " + str(a+i) + "}}" + "\n")
	f.write("saveAmberParm str" + str(i) + "  confamb.prmtop confamb" + str(i) + ".inpcrd" + "\n")

fname2 = "groupfile.sh"
f = open(fname2,"w")
f.write("#!/bin/sh"+ "\n")
for i in range(0,361):
	f.write("sander -O -i ener.in -c confamb" + str(i) + ".inpcrd -p confamb.prmtop -o dih_ener" + str(i) + ".out -r dih_ener"+ str(i) + ".restrt -x dih_ener"+ str(i) + ".mdcrd" + "\n")

fname3 = "grep.sh"
f = open(fname3,"w")
f.write("#!/bin/sh"+ "\n")
f.write("grep -A4 -m1 NSTEP dih_ener0.out > allout.txt" + "\n")
for i in range(1,361):
	f.write("grep -A4 -m1 NSTEP dih_ener" + str(i) + ".out >> allout.txt" + "\n")
