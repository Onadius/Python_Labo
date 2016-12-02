#coding: UTF-8
import subprocess
import datetime
import os


#Execute command function and make setting file
def doCommand(file1, file2, file3):

    	#make txtfile for setting v1 and v2
    	fileName = "settings_V1andV2.txt"
    	f = open(fileName, "w")

    	ans1 = raw_input("Which is Model ?>")
    	ans2 = raw_input("Which is basis function ?>")
    	ans3 = raw_input("Which is 1-4EFL ?>")
    	ans4 = raw_input("V1 = ")
    	ans5 = raw_input("V2 = ")
    	txt = "Model : " + str(ans1) + "\n" + "BasisFunction : " + str(ans2) + "\n" + "1-4EFl : " + str(ans3) + "\n" + "V1 = " + str(ans4) + "\n" + "V2 = " + str(ans5)
    	f.write(txt)

    	#make new dir for resultInpcrd
    	new_dir = "results_{model}_{function}".format(model = str(ans1), function = str(ans2))
    	cmd1 = "mkdir %s" % str(new_dir)
    	subprocess.check_call(cmd1.strip().split(" "))

    	#move files to dir
    	cmd2 = "mv settings_V1andV2.txt {0} {1} {2} ./{3}/".format(file1, file2, file3, new_dir)
    	subprocess.check_call(cmd2.strip().split(" "))

    	#Confirmation
    	subprocess.check_call("ls")
    	if(os.path.exists(str(new_dir)) == True):
    		print("> %s is exists!" % str(new_dir))
    		#subprocess.check_call(cmd2.strip().split(" "), shell=True)
    		#subprocess.check_call(com1.strip().split(" "))

def createFile1(com2):

	fname1 = "strfile.txt"
	f = open(fname1,"w")
	a = -180
	for i in range(0,361):
		f.write(str(com2) + "\n")
		f.write("str" + str(i) + " = sequence{ACE GLH NME}" + "\n")
		f.write("impose str" + str(i) + " {2} {{\"OE1\" \"CD\" \"OE2\" \"HE2\" " + str(a+i) + "}}" + "\n")
		f.write("saveAmberParm str" + str(i) + "  confamb.prmtop confamb" + str(i) + ".inpcrd" + "\n")

	return fname1

def createFile2():
	fname2 = "groupfile.sh"
	f = open(fname2,"w")
	f.write("#!/bin/sh"+ "\n")
	for i in range(0,361):
		f.write("sander -O -i ener.in -c confamb" + str(i) + ".inpcrd -p confamb.prmtop -o dih_ener" + str(i) + ".out -r dih_ener"+ str(i) + ".restrt -x dih_ener"+ str(i) + ".mdcrd" + "\n")

	return fname2

def createFile3():

	fname3 = "grep.sh"
	f = open(fname3,"w")
	f.write("#!/bin/sh"+ "\n")
	f.write("grep -A4 -m1 NSTEP dih_ener0.out > allout.txt" + "\n")
	for i in range(1,361):
		f.write("grep -A4 -m1 NSTEP dih_ener" + str(i) + ".out >> allout.txt" + "\n")

	return fname3

#main function
if __name__ == "__main__":


	#igb=5 --> mbondi2, igb=8 --> mbondi3, igb=6(in vacuo)
	type = raw_input("What is the type of igb? >")

	if(type == "8"):
	    mbon = 3
	    com2 = "set default PBradii mbondi%s" % str(mbon)

	elif(type == "6"):
		com2 = ""

	elif (type == "5"):
	    mbon = 2
	    com2 = "set default PBradii mbondi%s" % str(mbon)

	file1 = createFile1(com2)
	file2 = createFile2()
	file3 = createFile3()
	doCommand(file1, file2, file3) #Execute command
