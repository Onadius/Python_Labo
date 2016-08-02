#coding: UTF-8
import subprocess


#make textFile for tleap*360
def writeCommand(dirName, com1, com2, com3, com4, com5, com6):

    	f = open("doCommand.txt", "w")
    	for angle in range(-180, 181):
		comAngle = com4 + str(angle) + " }}"
		f.write(com1 + "\n" + com2 + "\n" + com3 + "\n" + comAngle 
                       + "\n" + com5 + "\n" + com6 + "\n")
	


#main function
if __name__ == "__main__":
	
    	dirName = raw_input("What is the name of Dir? >") #

	#variable for command
	com1 = "tleap -s -f leaprc." + dirName
	com2 = "set default PBradii mbondi2"
	com3 = "test = sequence{ACE ASH NME}"
	com4 = "impose test {2} {{OE1 CG OE2 HE2 "
	com5 = "saveamberparm test confamb.prmtop confamb.inpcrd"
	com6 = "quit"

	writeCommand(dirName, com1, com2, com3, com4, com5, com6) #create File

 	#Confirmation of txtFile
    	subprocess.check_call("ls")
    	subprocess.check_call(["cat", "doCommand.txt"])
