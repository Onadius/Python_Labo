#coding: UTF-8
import subprocess
import datetime

#make textFile for tleap*360 function
def writeCommand(dirName, com1, com2, com3, com4, com5_1, com5_2, com6):

	fname = "doCommand.txt" #define a file_name
    	f = open(fname, "w")
    	
    	for angle in range(-180, -179): #(-180, 181)
    		#shaped command_str
		comAngle = com4 + str(angle) + " }}"
		comSave = com5_1 + com5_2 + str(angle) + ".inpcrd" 
		
		f.write(com1 + "\n" + com2 + "\n" + com3 + "\n" + comAngle 
                       + "\n" + comSave + "\n" + com6 + "\n")
                       
	return fname



#Execute command function
def doCommand(fname, year, month, day):
	
	#Confirmation of txtFile
    	subprocess.check_call("ls")
    	subprocess.check_call(["cat", fname])
    	
    	#subprocess.check_call(["", ""])



#main function
if __name__ == "__main__":
	
    	dirName = raw_input("What is the name of Dir? >") #

	#variable for command
	com1 = "tleap -s -f leaprc." + dirName
	com2 = "set default PBradii mbondi2"
	com3 = "test = sequence{ACE ASH NME}"
	com4 = "impose test {2} {{OE1 CG OE2 HE2 "
	com5_1 = "saveamberparm test" 
	com5_2 = " confamb.prmtop confamb"
	com6 = "quit"
	
	#get today_data
	d = datetime.datetime.today()
	year = str(d.year)
	month = str(d.month)
	day = str(d.day)
	
	fname = writeCommand(dirName, com1, com2, com3, com4, com5_1, com5_2, com6) #makefile
	doCommand(fname, year, month, day) #Execute command
	

