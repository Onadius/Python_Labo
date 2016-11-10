#coding: UTF-8
import subprocess
import os


#main function
if __name__ == "__main__":
	
	
	fname3 = "grep.sh"
	f = open(fname3,"w")
	f.write("#!/bin/sh"+ "\n")
	f.write("grep -A4 -m1 NSTEP dihAngle-180_ene.out > allout.txt" + "\n")
	for angle in range(-180, 181):
		f.write("grep -A4 -m1 NSTEP dihAngle" + str(angle) + "_ene.out >> allout.txt" + "\n")
