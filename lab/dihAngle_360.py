#coding: UTF-8
import subprocess
import datetime
import os

#make textFile for tleap*360 function
def writeCommand(com2, com3, com4, com5_1, com5_2):

	fname = "doCommand.txt" #define a file_name
    	f = open(fname, "w")
    	
    	for angle in range(-180, 181): #(-180, 181)
    		#shaped command_str
		comAngle = com4 + str(angle) + " }}"
		comSave = com5_1 + com5_2 + str(angle) + ".inpcrd" 
		
		f.write(com2 + "\n" + com3 + "\n" + comAngle 
                       + "\n" + comSave + "\n")
                       
	return fname



#Execute command function
def doCommand(fname, year, month, day, sec, com1):
	
    	
    	#make new dir for resultInpcrd
    	new_dir = "results_"+ month + day + sec
    	cmd1 = "mkdir %s" % str(new_dir)
    	cmd2 = "cd %s" % str(new_dir)
    	
    	subprocess.check_call(cmd1.strip().split(" "))
    	
    	#Confirmation
    	subprocess.check_call("ls")	
    	if(os.path.exists(str(new_dir)) == True):
    		print("> %s is exists!" % str(new_dir))
    		#subprocess.check_call(cmd2.strip().split(" "), shell=True)
    		#subprocess.check_call(com1.strip().split(" "))


#main function
if __name__ == "__main__":
	
    	dirName = raw_input("What is the name of Dir? >") 
    	
	#variable for command
	com1 = "tleap -s -f leaprc.%s" % (dirName)
	com2 = "set default PBradii mbondi2"
	com3 = "test = sequence{ACE ASH NME}"
	com4 = "impose test {2} {{OE1 CG OE2 HE2 "
	com5_1 = "saveamberparm test" 
	com5_2 = " confamb.prmtop confamb"
	
	#get today_data
	d = datetime.datetime.today()
	year = str(d.year)
	month = str(d.month)
	day = str(d.day)
	sec = str(d.second)
	
	fname = writeCommand(com2, com3, com4, com5_1, com5_2) #makefile
	doCommand(fname, year, month, day, sec, com1) #Execute command
	

