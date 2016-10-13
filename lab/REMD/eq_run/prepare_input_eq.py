import os
import random
from subprocess import call

def make_input(rem_switch,rep_num,chag_name,chag_val):
	
	f_r = open("md.mdin","r")
        f_w = open("con_md.mdin","w")
 	f_w.close()
	f_w = open("con_md.mdin","a")	

	for line in  f_r:
		for n,v in zip(chag_name,chag_val):
                	if n in line:
				s = line.split(",")
				for i,j in enumerate(s):	
					if n in j:
						t = j.split("=")
						t[1] = str(v)
						s[i] = "=".join(t).rstrip()
				line = ",".join(s)
                f_w.write(line)
				
        f_r.close()
        f_w.close()
        os.remove("md.mdin")
        os.rename("con_md.mdin","md.mdin")	

	if rem_switch == 0:
        	for i in range(1,rep_num+1,1):
               		cmd = "\cp -f md.mdin mdin.rep%d" % i
                	call(cmd,shell = True)
                	cmd = "\cp -f confamb.inpcrd confamb.inpcrd.rep%d" % i
                	call(cmd,shell = True)
                	cmd = "\cp -f confamb.prmtop prmtop.rep%d" % i
                	call(cmd,shell = True)
                return "The input file for equilibrium has been made !" + "\n"

	elif rem_switch == 1:
                for i in range(1,rep_num+1,1):
                        cmd = "\cp -f md.mdin mdin.rep%d" % i
                        call(cmd,shell = True)
                        cmd = "\cp -f confamb.prmtop prmtop.rep%d" % i
                        call(cmd,shell = True)
 	       	return "The input file for production run has been made !" + "\n"


def get_group(rem_switch,rep_num):
	f_w = open("groupfile.txt","w")
	f_w.write("# The group file for REMD simulation\n")
	f_w.close()

	f_w = open("groupfile.txt","a")

	for i in range(1,rep_num+1):
		element = [rem_switch]
		for j in range(7):
			element.append(i)
		element = tuple(element)

		if rem_switch == 0:
			if i < 10:
				f_w.write("-O -rem %s -i mdin.rep%d -o mdout.rep%d -c confamb.inpcrd.rep%d "\
				"-r after-eq.rst.rep%d -x mdcrd.00%d -inf mdinfo.00%d -p prmtop.rep%d" % (element) + "\n")
			elif i >= 10:
       	        		f_w.write("-O -rem %s -i mdin.rep%d -o mdout.rep%d -c confamb.inpcrd.rep%d "\
				"-r after-eq.rst.rep%d -x mdcrd.0%d -inf mdinfo.0%d -p prmtop.rep%d" % (element) + "\n")
	
		elif rem_switch == 1:
			if i < 10:
        			f_w.write("-O -rem %s -i mdin.rep%d -o mdout.rep%d -c after-eq.rst.rep%d "\
				"-r after-remd.rst.rep%d -x mdcrd.00%d -inf mdinfo.00%d -p prmtop.rep%d" % (element) + "\n")
        		elif i >= 10:
               	        	f_w.write("-O -rem %s -i mdin.rep%d -o mdout.rep%d -c after-eq.rst.rep%d "\
				"-r after-remd.rst.rep%d -x mdcrd.0%d -inf mdinfo.0%d -p prmtop.rep%d" % (element) + "\n")
	f_w.close()

	if rem_switch == 0:
		return "The group file for equilibrium has been made !" + "\n"
	elif rem_switch == 1:
		return "The group file for production run has been made !" + "\n"

def geometric_num(temp_num,first_temp,last_temp):
	temp_list = []
	start = first_temp
	end = last_temp
	r = (end/float(start))**(1/(float(temp_num)-1.0))
	for i in range(temp_num):
		if i == 0:
			temp_list.append(start)
		elif i == (temp_num -1):
			temp_list.append(end)
		else:
			temp_list.append(round(temp_list[i-1]*r,3))
	return temp_list

def get_temp(rem_switch,rep_num,first_temp,last_temp):
	temp_list = geometric_num(rep_num,first_temp,last_temp)
	
	for temp,num in zip(temp_list,range(rep_num)):
		num = num + 1
		f_r = open("mdin.rep%d" % num,"r")
		f_w = open("con_mdin.rep%d" % num,"w")
		for line in  f_r:
			if " tempi" in line:
				line = line.replace("tempi=%d" % first_temp,"tempi=%.2f"%temp)
				f_w.write(line)
			elif "temp0" in line:
				line = line.replace("temp0=%d" % first_temp,"temp0=%.2f"%temp)
				f_w.write(line)
			else:
				f_w.write(line)
		f_r.close()
		f_w.close()
		os.remove("mdin.rep%d"%num)
		os.rename("con_mdin.rep%d" % num,"mdin.rep%d" % num)

	if rem_switch == 0:
		return "%s temperatures for production run have modified !" % rep_num + "\n"
	elif rem_switch == 1:
		return "%s temperatures for production run have modified !" % rep_num + "\n"


if __name__ == "__main__":

	rep_num = 6
	first_temp = 300
	last_temp = 900
	rem_switch = 0        #rem = 1 :REMD , rem = 0 :not REMD 
	chag_name = ["irest","ntx","nstlim","numexchg"]
	chag_val = [0,1,100000,1]
	
	print("%s" % make_input(rem_switch,rep_num,chag_name,chag_val))
	print("%s" % get_group(rem_switch,rep_num))
	print("%s" % get_temp(rem_switch,rep_num,first_temp,last_temp))
	


	



