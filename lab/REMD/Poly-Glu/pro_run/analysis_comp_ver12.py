import math
import os
import shutil
from subprocess import call

def get_last_frame(prmtop,mdcrd):
	fr = open("%s" % prmtop,"r")
	flag = 0
        
        for line in fr.readlines():
        	if "%FORMAT(10I8)" in line:
        		flag = 1
        	elif flag == 1:
        		atom_num = int(line.strip().split()[0])
        		break
	
        fr.close()
        fr = open("%s" % mdcrd,"r")
        count = 0
        last_frame = 0
        
        while True:
        	line = fr.readline()
        	if "trajectory" in line:
        		continue
        	if not line:
        		break
        	else:
        		count += len(line.strip().split())
        	if count == (atom_num*3):
        		last_frame += 1
        		count = 0
        fr.close()
	return last_frame	
	
def get_mdcrd(get_temp,prmtop,mdcrd):                      # This function makes only 300K trajectry file.
        fw = open("extract_%sK_traj.csh" % get_temp,"w")
        fw.write("#!/bin/csh\n")
        fw.close()

        fw = open("extract_%sK_traj.csh" % get_temp,"a")
        fw.write("ptraj %s  << EOF\n" % prmtop)
        fw.write("trajin mdcrd.001 remdtraj remdtrajtemp %s.00\n" % get_temp)
        fw.write("trajout %s nobox\n" % mdcrd)
        fw.close()

        call(["csh","extract_%sK_traj.csh" % get_temp])

def convert_pdb(frame,prmtop,mdcrd):                    # This function converts trajectory file to pdb file for dssp analysis and dihedral analysis.
        fw = open("convert_pdb.csh","w")
        fw.write("#!/bin/csh\n")
        fw.close()

        fw = open("convert_pdb.csh","a")
        fw.write("ptraj %s  << EOF\n" % prmtop)
        fw.write("trajin %s %s %s %s\n" % (mdcrd,frame[0],frame[1],frame[2]))
        fw.write("trajout split.pdb pdb\n")
        fw.close()

        call(["csh","convert_pdb.csh"])


def dssp(frame):                           # The DSSP analysis is done here. 
        for i in range(int(frame[0]),int(frame[1])+1,int(frame[2])):
                call(["/home/biostr1/bin/dssp","split.pdb.%d" % i,"dssp.%d" % i])


def dssp_analysis(line,dssp_list):    # The three helices are counted here.
	if line[16] == "H" or line[16] == "I" or line[16] == "G":
		dssp_list[0] += 1
		if line[16] == "G":      # G = 3_10_helix
			dssp_list[1] += 1
		
		elif line[16] == "H":    # H = alpha_helix
			dssp_list[2] += 1
		
		elif line[16] == "I":    # I = pai_helix
			dssp_list[3] +=1

	elif line[16] == "T":
		dssp_list[4] += 1
	elif line[16] == "E":
                dssp_list[5] += 1

	return list(dssp_list)
 	
def dihedral_analysis(line,dihedral_list):     # This function count the dihedral angles included in the area of specific secondary structure. 
	# The reference of dihedral angle is ff99SB essay.
	# Secondary stracture = [phi range,psi range]
	# dih == dihedral angle 
	H_r_dih = [[-90,-30],[-75,-15]]     # Hornak 
	#S_r_dih = [[-90,-30],[-77,-17]]    # Sorin ,Pande (and Garcia)
	l_dih = [[30,130],[-50,100]]        # Novotny 2005 
	pp2_dih = [[-100,-40],[120,180]]
	b_dih =[[-180,-120],[120,180]]

	dih = []                           # The dihedral angles from original data
	dih.append(float(line[103:109]))   # The dihedral angle "phi"
	dih.append(float(line[109:115]))   # The dihedral angle "psi"
	
	if (H_r_dih[0][0]<= dih[0] <= H_r_dih[0][1]) and (H_r_dih[1][0] <= dih[1] <= H_r_dih[1][1]):
		dihedral_list[0] += 1
	
	if (l_dih[0][0] <= dih[0] <= l_dih[0][1]) and (l_dih[1][0] <= dih[1]<= l_dih[1][1]):
		dihedral_list[1] += 1
	
	if (pp2_dih[0][0]<= dih[0] <= pp2_dih[0][1]) and (pp2_dih[1][0] <= dih[1] <= pp2_dih[1][1]):
	 	dihedral_list[2] += 1

	if (b_dih[0][0]<= dih[0] <= b_dih[0][1]) and (b_dih[1][0] <= dih[1] <= b_dih[1][1]):
		dihedral_list[3] += 1

	return list(dihedral_list)

def all_dihedral_angles(line,s):               # All dihedral anglesis stored on "s" here. 
	dih = []
	dih.append(float(line[103:109]))
	dih.append(float(line[109:115]))
	if (-180 <= dih[0] <= 180) and (-180 <= dih[1] <= 180):                                
		s += ",".join(map(str,dih)) + "\n"                                                                                                                 
	return s

def end_to_end(frame,prmtop,mdcrd,name,edge):                 # End to end analysis is done here.
	fw = open("end_to_end.csh","w")
	fw.write("#!/bin/csh\n")
	fw.close()

	fw = open("end_to_end.csh","a")
        fw.write("ptraj %s << EOF\n" % prmtop)
        fw.write("trajin %s %s %s %s\n" % (mdcrd,frame[0],frame[1],frame[2]))
        fw.write("distance end_to_end %s %s out %s\n" % (edge[0],edge[1],name))     # It is necessaly to add 1 to variant "res" because the first "CA" is in "Ace".
        fw.close()
	call(["csh","end_to_end.csh"])


def dih_side(frame,prmtop,mdcrd,res):
	for i in range(2,res+2):
		fw = open("dih_side.csh","w")
                fw.write("#!/bin/csh\n")
                fw.close()
        
                fw = open("dih_side.csh","a")
                fw.write("ptraj %s << EOF\n" % prmtop)
                fw.write("trajin %s %s %s %s\n" % (mdcrd,frame[0],frame[1],frame[2]))
                fw.write("dihedral d1 :{0}@OE1 :{0}@CD :{0}@OE2 :{0}@HE2 out dih_side{1}.txt\n".format(str(i),str(i-1)))
                fw.close()
                call(["csh","dih_side.csh"])


def error_var(data_len,bin,data):
        data_swap = []
        ave_list = []

        for d in data:
                data_swap.append(d)
                if len(data_swap) == (len(data)/bin):
                        ave_list.append(sum(data_swap)/float(data_len/bin))
			data_swap = []

        error_swap = map(lambda x:(x-sum(ave_list)/float(bin))**2,ave_list)
        return math.sqrt((sum(error_swap)/float(bin-1))/float(bin))
	
def content_out(name,struct_num,res,bin,all_data):	
	content = [[] for d in range(len(all_data[0][0]))]
	error_list = []

	if name == "dssp_content.txt":
		fw = open("%s" % name,"w")
		fw.write("#The_helices_analized_by_DSSP_analysis\n" +\
		"#The_first_row_are_corresponding_to_All_helix,3_10,Alpha,Pai,Turn and Extend.\n" +\
		"#The_second_row_is_corresponding_to_error_value.\n")
		fw.close()

	elif name == "dihedral_content.txt":
		fw = open("%s" % name,"w")
		fw.write("#The_dihedral_angles_included_in_the_area_of_specific_secondary_structure\n"+\
		"#The_first_row_is_corresponding_to_Hornak's_Right-handed_alpha_helix,Sorin's_Right-handed_alpha_helix,"+\
		"Left-handed_alpha_helix,Poly_proline_II_and_Extended_be-ta_strand.\n" +\
		"#The_second_row_is_corresponding_to_error_value.\n")
		fw.close()

	elif name == "dihedral_side_content.txt":
		fw = open("%s" % name,"w")
                fw.write("#The_dihedral_angles_included_the_calboxyl_group_of side_chain\n"+\
                "#The_each_row_syn_error_anti_error.\n")
                fw.close()

	for data in all_data:
		for i in range(res):
			for j in range(len(all_data[0][0])):
				content[j].append(data[i][j])
	
	fw = open("%s" % name,"a")

	if (name == "dssp_content.txt") or (name == "dihedral_content.txt"):		
		data_len = struct_num*(res-2)
	else:
		data_len = struct_num*res

	for num in content:
		error = error_var(data_len,bin,num)
		fw.write("%s %s\n" % (str(sum(num)/float(data_len)),str(error)))
	fw.close()			
	
	
def all_out(name,frame,struct_num,res,all_data):
	con_all = []	

        if name == "all_dssp.txt":
                fw = open("%s" % name,"w")
                fw.write("#The_helices_analized_by_DSSP_analysis\n" +\
                "#The_each_data_are_corresponding_to_NSTEP,All_helix,3_10,Alpha,Pai,Turn and Extend\n")
                fw.close()

        elif name == "all_dihedral.txt":
                fw = open("%s" % name,"w")
                fw.write("#The_dihedral_angles_included_in_the_area_of_specific_secondary_structure\n"+\
                "#The_each_data_are_corresponding_to_NSTEP,Hornak's_Right-handed_alpha_helix,Sorin's_Right-handed_alpha_helix,"+\
                "Left-handed_alpha_helix,Poly_proline_II_and_Extended_be-ta_strand\n")
                fw.close()

        for num in range(struct_num):
		con_swap = [0.0 for d in range(len(all_data[0][0]))]
                for i in range(res):
			for j in range(len(all_data[0][0])):
                                con_swap[j] += all_data[num][i][j]

		con_all.append(list(con_swap))


        fw = open("%s" % name,"a")
        for step,con in zip(range(int(frame[0])/int(frame[2]),int(frame[1])/int(frame[2])+1),con_all):
		con = map(lambda x:x/float(res-2), con)
		fw.write("%s %s\n" % (str(step)," ".join(map(str,con))))
        fw.close()
		
def per_res_out(name,struct_num,res,all_data,bin):
        con_per = [[[] for d in range(len(all_data[0][0]))] for r in range(res)]

        if name == "dssp_per_res.txt":
                fw = open("%s" % name,"w")
                fw.write("#The_helices_analized_by_DSSP_analysis\n" +\
                "#The_each_data_are_corresponding_to_,All_helix,3_10,Alpha,Pai_and_Turn\n")
                fw.close()

        elif name == "dihedral_per_res.txt":
                fw = open("%s" % name,"w")
                fw.write("#The_dihedral_angles_included_in_the_area_of_specific_secondary_structure\n"+\
                "#The_each_data_corresponding_to_Hornak's_Right-handed_alpha_helix,Sorin's_Right-handed_alpha_helix,"+\
                "Left-handed_alpha_helix,Poly_proline_II_and_Extended_be-ta_strand\n")
                fw.close()

	elif name == "dihedral_side_content.txt":
                fw = open("%s" % name,"w")
                fw.write("#The_dihedral_angles_included_the_calboxyl_group_of side_chain\n"+\
                "#The_each_row_syn_error_anti_error.\n")
                fw.close()

        for data in all_data:
                for i in range(res):
                        for j in range(len(all_data[0][0])):
                                con_per[i][j].append(data[i][j])	
	
	fw = open("%s" % name,"a")
        for i,con in enumerate(con_per):
                fw.write("%s %s\n" % (str(i)," ".join(map(str,map(lambda x:sum(x)/float(struct_num),con)))))
	fw.write("\n")
	for i,con in enumerate(con_per):
		fw.write("%s %s\n" % (str(i)," ".join(map(str,map(lambda x:error_var(struct_num,bin,x),con)))))
		
        fw.close()

def calc_helix(name,frame,struct_num,res,bin,dssp_all,dihedral_all):
        right_list = []       # The list including the numbers of all helix, 3_10-helix,alpha-helix,pai-helix
        left_list = []
        right_flag = []
        left_flag = []
        all_helix = []
        calc_list = []
	error_list = []
	
        for helix,dih in zip(dssp_all,dihedral_all):
	
                for i in range(len(dssp_all[0][0])-2): # except "Extended be-ta" and "Turn"
                        right_list.append(0)
                        left_list.append(0)
                        right_flag.append(0)
                        left_flag.append(0)
			all_helix = 0
        		all_flag = 0

                for i in range(res):
                        for j in range(len(helix[i])-2):
				if (j == 0) and (helix[i][j] == 1) and (all_flag == 0):
					all_helix += 1
					all_flag = 1
				elif (j == 0) and (helix[i][j] == 0) and (all_flag == 1):
                                        all_flag = 0
                                if (helix[i][j] == 1) and (right_flag[j] == 0) and (dih[i][1] != 1):
                                        right_list[j] += 1
                                        right_flag[j] = 1
                                elif (helix[i][j] == 0) and (right_flag[j] == 1):
                                        right_flag[j] = 0
                                if (helix[i][j] == 1) and (left_flag[j] == 0) and (dih[i][1] ==1):
                                        left_list[j] += 1
                                        left_flag[j] = 1
                                elif (helix[i][j] == 0) and (left_flag[j] == 1):
                                        left_flag[j] = 0
                calc_list.append(list([all_helix] + right_list + left_list))
                right_list = []
                left_list = []
	
	fw = open("%s" % name,"w")
	fw.write("#The_helices_analized_by_DSSP_analysis\n" +\
                "#The_each_data_are_corresponding_to_average_value,error_value,NSTEP,The_numbe_of_helix\n")
		
	fw.close()
			
	fw = open("%s" % name, "a")
	
	for i in range(len(calc_list[0])):
		swap_data = []
		for j in range(len(calc_list)):
			swap_data.append(calc_list[j][i])
		error = error_var(len(swap_data),bin,swap_data)
		fw.write("%s %s " % (str(sum(swap_data)/float(len(swap_data))),str(error)))
	fw.write("\nSTEPS All_helix All_R 310_R alphaR PaiR All_L 310_L alphaL PaiL\n")

	for step,num in zip(range(int(frame[0])/int(frame[2]),int(frame[1])/int(frame[2])+1),calc_list):
                fw.write("%s %s\n" % (str(step)," ".join(map(str,num))))
        fw.close()


def dihedral_out(name,s):
	fw = open("%s" % name,"w")
	fw.write("%s" % s)
	fw.close()
	
def end_to_end_ave(output,input,bin,struct_num):
	data = []
	fr = open("%s" % input,"r")
	for line in fr.readlines():
		data.append(float(line.strip().split()[1]))
	fr.close()
	
	error = error_var(len(data),bin,data)	
	
	fw = open("%s" % output,"w")
	fw.write("The_end_to_end_average\n%s %s\n" % (str(sum(data)/float(struct_num)),error))
	fw.close()
		
def dih_side_analysis(line2):
	torsion = [0,0]      # [syn,anti]
	data = float((line2.strip().split()[1]))	
	
	if -90.0 <= data <= 90.0: #The "syn" state 
		torsion[0] = 1
	elif (-180.0 <= data < -90.0) or (90 < data <=180): #The "anti" state
		torsion[1] = 1
	
	return list(torsion)

def analysis_macro(frame,path,get_temp,prmtop,mdcrd,res,out5,aci_stat):                 # The role of this function is function call, the file loading and the file writing out.
	
	dssp_all = []
	dihedral_all = []
	struct_num = (int(frame[1])-int(frame[0]))/int(frame[2])+1
	s = ""
	dihedral_side_all = [[] for d in range(struct_num)] 
	
	convert_pdb(frame,prmtop,mdcrd)        # The function call "convert_pdb()"
	
	dssp(frame)                        # The function call "dssp()"
	if aci_stat == "GLH":        
		dih_side(frame,prmtop,mdcrd,res)

        for i in range(int(frame[0]),int(frame[1])+1,int(frame[2])):                                   
                fr = open("dssp.%d" % i,"r")
                j =  0                                     # increasing the line of dssp_all           
		dssp_res = []                  
                dihedral_res = []
                                                                  
                while True:       
                        if fr.readline()[2] == "#":break                                               
        
                for line in fr.readlines():
			dssp_list = [0]*6
			dihedral_list = [0]*4			
			
                        dssp_res.append(dssp_analysis(line,dssp_list))       # The function call "dssp_analysis()"                                                                                        
                        dihedral_res.append(dihedral_analysis(line,dihedral_list))   # The function call "dihedral_analysis()"    
                        s = all_dihedral_angles(line,s)                        # The function call "all_dihedral_angles()"                                                                                                           
                        j += 1    
		dssp_all.append(list(dssp_res))
                dihedral_all.append(list(dihedral_res))                                                                                      
                fr.close() 
   
	if aci_stat == "GLH":
		for i in range(1,res+1):
			fr2 = open("dih_side%s.txt" % str(i),"r")
			dihedral_side_swap = []
			j = 0
			for line2 in fr2.readlines():
				dihedral_side_all[j].append(dih_side_analysis(line2))                       # The "dihedral_side_swap" is the list containing "[syn,anti]" on each residue.
				j += 1
			fr2.close()									  # For example, if there is 20 residues, 20 lists are contained within the "dihedral_side_all". 

	for name in out5:
		if name == "end_to_end.txt":
			edge = [":2@CA",":%s@CA" % str(res+1)]
		
		elif name == "end_to_end_NC.txt":
			edge = [":1@CH3",":%s@CH3" % str(res+2)]
		
		elif name == "end_to_end_half1.txt":
                	edge = [":2@CA",":%s@CA" % str(int(((res+1)+2)/2))]
		
		elif name == "end_to_end_half2.txt":
                	edge = [":%s@CA" % str(int(((res+1)+2)/2)+1),":%s@CA" % str(res+1)]
		
		elif name == "end_to_end_half1_NC.txt":
                	edge = [":1@CH3",":%s@CA" % str(int(((res+1)+2)/2))]
                
		elif name == "end_to_end_half2_NC.txt":
                	edge = [":%s@CA" % str(int(((res+1)+2)/2)+1),":%s@CH3" % str(res+2)]
		
		end_to_end(frame,prmtop,mdcrd,name,edge)

	return [dssp_all,dihedral_all,dihedral_side_all,s,struct_num]
	
def output_macro(result_data,frame,res,bin,out1,out2,out3,out4,out6,aci_stat):
	dssp_all = list(result_data[0])
	dihedral_all = list(result_data[1])
	dihedral_side_all = list(result_data[2])
	s = result_data[3]
	struct_num = result_data[4]
	
	flag = 0
	for name in out1:
		if flag == 0:
                	content_out(name,struct_num,res,bin,dssp_all)
			flag = 1
		
		elif flag == 1:
			all_out(name,frame,struct_num,res,dssp_all)
			flag = 2
		
		elif flag == 2:
			per_res_out(name,struct_num,res,dssp_all,bin)
			flag = 3

		elif flag == 3:
			calc_helix(name,frame,struct_num,res,bin,dssp_all,dihedral_all)
	
	flag = 0
        for name in out2:
                if flag == 0:
                        content_out(name,struct_num,res,bin,dihedral_all)
                        flag = 1

                elif flag == 1:
                        all_out(name,frame,struct_num,res,dihedral_all)
                        flag = 2

                elif flag == 2:
                        per_res_out(name,struct_num,res,dihedral_all,bin)	

	dihedral_out(out3,s)

	for name in out4:
		if name == "end_to_end_ave.txt":
			name2 = "end_to_end.txt"
		elif name == "end_to_end_NC_ave.txt":
			name2 = "end_to_end_NC.txt"
		end_to_end_ave(name,name2,bin,struct_num)
	if aci_stat == "GLH":
		for name in out6:
			if name == "dihedral_side_content.txt":
				content_out(name,struct_num,res,bin,dihedral_side_all)
			elif name == "dihedral_side_per_res.txt":
				per_res_out(name,struct_num,res,dihedral_side_all,bin)			

def res_aci_stat(prmtop):
	flag = 0
        PGA = []
        fr = open("%s" % prmtop,"r")
        for line in fr.readlines():
                if "%FLAG RESIDUE_LABEL" in line:
                        flag = 1
                        continue
                if "%FORMAT(20a4)" in line and flag ==1:
                        flag += 1
                        continue
                if flag == 2 and "%FLAG RESIDUE_POINTER" not in line:
                        PGA += line.strip().split()

                elif "%FLAG RESIDUE_POINTER" in line:
                        break

        if "GLU" in PGA:
                aci_stat = "GLU"
                res = len(PGA)-2
	elif "GLU" not in PGA and "GLH" not in PGA: 
		aci_stat = "GLU"
		res = len(PGA)-2
        else:
                aci_stat = "GLH"                    # When concluding "GLH", aci_stat analysis are implimented.
                res = len(PGA)-2
        fr.close()

	return aci_stat,res


if __name__ == "__main__":

	##########################
	#    variable derived    #
	##########################

	path = os.getcwd() 	          # The "path" is "current directory".
	input_name = "md.mdin"

	fr = open("%s" % input_name, "r") # The system temperature is derived from "md.mdin" file.
        for line in fr.readlines():
                if "temp0" in line:
                        for s in line.strip().split(","):
                                if  "temp0" in s:
                                        get_temp = s.strip().split("=")[1].strip()[0:3]
	
	mdcrd = "remd.%sK.mdcrd" % get_temp # Replica exchange MD 
	#mdcrd = "after-md.mdcrd"           # Conventional MD
	prmtop = "prmtop.rep1"
	get_mdcrd(get_temp,prmtop,mdcrd)                # The function call "#get_mdcrd()"
        frame = ["1000","%s" % get_last_frame(prmtop,mdcrd),"1"]     # The structure are 1-50000 frames (5000 sets).
	bin = 20
	aci_stat,res = res_aci_stat(prmtop)
	
	###########################
	#     Output file names   #
	###########################

	out1 = ["dssp_content.txt","all_dssp.txt","dssp_per_res.txt","The_number_of_helix.txt"]
        out2 = ["dihedral_content.txt","all_dihedral.txt","dihedral_per_res.txt"]
	out3 = "dihedral_angle.txt"
        out4 = ["end_to_end_ave.txt","end_to_end_NC_ave.txt"]
	out5 = ["end_to_end.txt","end_to_end_NC.txt","end_to_end_half1.txt","end_to_end_half2.txt","end_to_end_half1_NC.txt","end_to_end_half2_NC.txt"]
	out6 = ["dihedral_side_content.txt","dihedral_side_per_res.txt"]	

	###########################

        if os.path.exists(path+"/split_dssp"):
                call(["rm","-r","-f","./split_dssp"])
        if os.path.exists(path+"/split_pdb"):
                call(["rm","-r","-f","./split_pdb"])
        if os.path.exists(path+"/analysis"):
                call(["rm","-r","-f","./analysis"])
	if os.path.exists(path+"./dih_side_all") and aci_stat == "GLH":
                call(["rm","-r","-f","./dih_side_all"])	

        call(["mkdir","-p","split_dssp"])
        call(["mkdir","-p","split_pdb"])
	if aci_stat == "GLH":
        	call(["mkdir","-p","dih_side_all"])
	
        result_data = analysis_macro(frame,path,get_temp,prmtop,mdcrd,res,out5,aci_stat)    # The function call "analysis_macro()"
	output_macro(result_data,frame,res,bin,out1,out2,out3,out4,out6,aci_stat)
	
	for i in range(int(frame[0]),int(frame[1])+1,int(frame[2])):
		call(["mv","-f","%s/split.pdb.%d" % (path,i),"%s/split_pdb/" % path])
        	call(["mv","-f","%s/dssp.%d" % (path,i),"%s/split_dssp/" % path])
	if aci_stat == "GLH":
		cmd = "mv -f {0}/dih_side*.txt {0}/dih_side_all/".format(path)
		call(cmd, shell = True)

        os.chdir("%s" % path)
        call(["mkdir","-p","analysis"])                
	os.chdir("%s/analysis" % path)
	call(["mkdir","-p","dssp_analysis"])
	call(["mkdir","-p","dihedral_analysis"])
	call(["mkdir","-p","end_to_end_analysis"])
        call(["mkdir","-p","rad_gyr_analysis"])
	if aci_stat == "GLH":
		call(["mkdir","-p","dihedral_side_analysis"])	

	for out in out1:
		call(["mv","-f","%s/%s" % (path,out),"%s/analysis/dssp_analysis/%s" % (path,out)])
	for out in out2:
		call(["mv","-f","%s/%s" % (path,out),"%s/analysis/dihedral_analysis/%s" % (path,out)])
	
	call(["mv","-f","%s/%s" % (path,out3),"%s/analysis/dihedral_analysis/%s" % (path,out3)])	
	
	for out in (out4+out5):
		call(["mv","-f","%s/%s" % (path,out),"%s/analysis/end_to_end_analysis/%s" % (path,out)])
	if aci_stat == "GLH":
		for out in (out6):
                	call(["mv","-f","%s/%s" % (path,out),"%s/analysis/dihedral_side_analysis/%s" % (path,out)])











