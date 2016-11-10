#coding: UTF-8
import subprocess
import datetime
import os

#make textFile for tleap*360 function
def writeCommand(type, com2, com3, com4, com5_1, com5_2):

	fname = "doCommand_igb%s.txt" % str(type) #define a file_name
    	f = open(fname, "w")
    	
    	for angle in range(-180, 181): #(-180, 181)
    		#shaped command_str
		comAngle = com4 + str(angle) + " }}"
		comSave = com5_1 + com5_2 + str(angle) + ".inpcrd" 
		
		f.write(com2 + "\n" + com3 + "\n" + comAngle 
                       + "\n" + comSave + "\n")
                       
	return fname



#Execute command function
def doCommand(fname, type, year, month, day, sec):
	
    	
    	#make new dir for resultInpcrd
    	new_dir = "results_igb%s_" % str(type) + month + day 
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
    	
    	
	#variable for command
	#com1 = "tleap -s -f leaprc.%s" % (dirName)
	com3 = "test = sequence{ACE ASH NME}"
	com4 = "impose test {2} {{OD1 CG OD2 HD2 "
	com5_1 = "saveamberparm test" 
	com5_2 = " confamb.prmtop confamb"
	
	#get today_data
	d = datetime.datetime.today()
	year = str(d.year)
	month = str(d.month)
	day = str(d.day)
	sec = str(d.second)
	
	fname = writeCommand(type, com2, com3, com4, com5_1, com5_2) #makefile
	doCommand(fname, type, year, month, day, sec) #Execute command
	

