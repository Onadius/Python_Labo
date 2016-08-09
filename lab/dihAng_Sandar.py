#coding: UTF-8
import subprocess
import os


#main function
if __name__ == "__main__":
	
    	for angle in  range(-180, 181):
    		
    		#define variable for command
		com1 = "sander -O -i Ene.in -c confamb%s.inpcrd -p confamb.prmtop -o " % str(angle)
		com2 = "dihAngle%s_ene.out -r dihAngle%s_ene.restrt -x dihAngle%s_ene.mdcrd" % (str(angle), str(angle), str(angle))
		COM = com1 + com2
		
		#print(COM)
		subprocess.check_call(COM.strip().split(" "))
			

	
