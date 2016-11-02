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

	
def dssp_analysis(line,dssp_R_list,dssp_L_list):     # This function count the dihedral angles included in the area of specific secondary structure. 
	# The reference of dihedral angle is ff99SB essay.
	# Secondary stracture = [phi angle_range,psi angle_range]
	# dih == dihedral angle 

	H_l_dih = [[30.0,130.0],[-50.0,100.0]]     # Hornak (right-handed alpha-helix) 
        G_l_dih = [[30.0,130.0],[-50.0,100.0]]        # left-handed 310-helix
        I_l_dih = [[30.0,130.0],[-50.0,100.0]]


	dih = []                           # The dihedral angles from original data
	dih.append(float(line[103:109]))   # The dihedral angle "phi"
	dih.append(float(line[109:115]))   # The dihedral angle "psi"

        if line[16] == "G":      # G = 3_10_helix
		if (G_l_dih[0][0] <= dih[0] <= G_l_dih[0][1]) and (G_l_dih[1][0] <= dih[1] <= G_l_dih[1][1]):
			dssp_L_list[1] += 1
		else:
			dssp_R_list[1] += 1
        elif line[16] == "H":    # H = alpha_helix
                if (H_l_dih[0][0] <= dih[0] <= H_l_dih[0][1]) and (H_l_dih[1][0] <= dih[1] <= H_l_dih[1][1]):
                        dssp_L_list[2] += 1
		else:
                        dssp_R_list[2] += 1
        elif line[16] == "I":    # I = pai_helix
                if (I_l_dih[0][0] <= dih[0] <= I_l_dih[0][1]) and (I_l_dih[1][0] <= dih[1] <= I_l_dih[1][1]):
                        dssp_L_list[3] += 1
		else:
                        dssp_R_list[3] += 1

	if 1 in dssp_R_list[1:]:
		dssp_R_list[0] += 1
	if 1 in dssp_L_list[1:]:
                dssp_L_list[0] += 1

	return list(dssp_R_list),list(dssp_L_list)

def calc_helix_len(struct_num,res,dssp_all):
        
        len_list_comp = []

        for dssp in dssp_all:
	        len_swap = []
  		flag = []
        	len_list = []

                for i in range(len(dssp[0])):
                        flag.append(0)
			len_swap.append(0) 
			len_list.append([])

                for i in range(res):
                        for j in range(len(dssp[0])):
                                if (dssp[i][j] == 1) and (flag[j] == 0):
                                        len_swap[j] += 1
					flag[j] = 1
				elif (dssp[i][j] == 1) and (flag[j] == 1):
					len_swap[j] += 1
                                elif (dssp[i][j] == 0) and (flag[j] == 1):
                                        flag[j] = 0
					len_list[j].append(int(len_swap[j]))
					len_swap[j] = 0

	        len_list_comp.append(list(len_list))
			
	return len_list_comp
	
def analysis_macro(frame,path,get_temp,res):                 # The role of this function is function call, the file loading and the file writing out.
	error_R = []
	error_L = []	
	dssp_R_all = []
	dssp_L_all = []
	bin = 20	
	struct_num = (int(frame[1])-int(frame[0]))/int(frame[2])+1
	s = ""
	
	# "dssp_(R/L)_all" are following as:
	#                  |----------The number of structure----------------|
        #                   |-------------Residue length----------------|
        # dssp_(R/L)_all = [[[All,310,alpha,pai],[All,310,alpha,pai],...],...]
	
        for i in range(int(frame[0]),int(frame[1])+1,int(frame[2])):                                   
                fr = open("dssp.%d" % i,"r")
                j =  0                                     # increasing the line of dssp_all           
		dssp_R_res = []    
		dssp_L_res = []              
                                                                  
                while True:       
                        if fr.readline()[2] == "#":break                                               
        
                for line in fr.readlines():
			dssp_R = [0]*4
			dssp_L = [0]*4			
			
                        dssp_R,dssp_L = dssp_analysis(line,dssp_R,dssp_L)       # The function call "dssp_analysis()" 
			dssp_R_res.append(list(dssp_R))
			dssp_L_res.append(list(dssp_L))
                        j += 1
			   
		dssp_R_all.append(list(dssp_R_res))
                dssp_L_all.append(list(dssp_L_res)) 

        R_data = calc_helix_len(struct_num,res,dssp_R_all)                                                                             
	L_data = calc_helix_len(struct_num,res,dssp_L_all)
	
	content_R = [[] for d in range(len(dssp_R_all[0][0]))]
        content_L = [[] for d in range(len(dssp_L_all[0][0]))]
	content_R_ave = []
	content_L_ave = []

	for data1,data2 in zip(dssp_R_all,dssp_L_all):
		for i in range(res):
			 for j in range(len(dssp_R_all[0][0])):
				content_R[j].append(data1[i][j])
				content_L[j].append(data2[i][j])

	data_len = struct_num*(res-2)

	for num1,num2 in zip(content_R,content_L):
		content_R_ave.append(sum(num1)/float(data_len))
		content_L_ave.append(sum(num2)/float(data_len))
		error_R.append(error_var(data_len,bin,num1))
		error_L.append(error_var(data_len,bin,num2))
	return R_data,L_data,content_R_ave,content_L_ave,error_R,error_L
	
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
        else:
                aci_stat = "GLH"
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
	
	mdcrd = "remd.%sK.mdcrd" % get_temp
	prmtop = "prmtop.rep1"
        frame = ["1000","%s" % get_last_frame(prmtop,mdcrd),"1"]     # The structure are 1-50000 frames (5000 sets).
	aci_stat,res = res_aci_stat(prmtop)
	dir = "helix_len_Nov"
	helix_name = ["All","310","alpha","pai"]
	dic_R = {}
	dic_L = {}
	
	##########################
	
        os.chdir("%s/split_dssp/"%path)
	files = os.listdir("%s/split_dssp/" % path ) 	
		
        R_data,L_data,content_R_ave,content_L_ave,error_R,error_L = analysis_macro(frame,path,get_temp,res)    # The function call "analysis_macro()"
	os.chdir("%s/analysis/" % path)
	cmd = "mkdir -p %s" % dir
	call(cmd,shell= True)
	os.chdir("%s/analysis/%s"%(path,dir))

	for name in helix_name:
		dic_R.update({"%s" % name:""})
		dic_L.update({"%s" % name:""})
		fw1 = open("R_len_data_%s.txt" % (name),"w")
		fw1.write("#\n%s,%s\n" % (str(content_R_ave.pop(0)),str(error_R.pop(0))))
		fw1.close()
		fw2 = open("L_len_data_%s.txt" % (name),"w")
		fw2.write("#\n%s,%s\n" % (str(content_L_ave.pop(0)),str(error_L.pop(0))))
		fw2.close()
		
	for data1,data2 in zip(R_data,L_data):
		for name,d1,d2 in zip(helix_name,data1,data2):
			if len(d1) == 0:  
				d1 = [0]
			if len(d2) == 0:
				d2 = [0]
			
			dic_R[name] += (",".join(map(str,d1)) + "\n")
			dic_L[name] += (",".join(map(str,d2)) + "\n")

	for name in helix_name:
		fw1 = open("R_len_data_%s.txt" % (name),"a")
                fw2 = open("L_len_data_%s.txt" % (name),"a")
		fw1.write("%s\n" % dic_R[name])
		fw2.write("%s\n" % dic_L[name])
		fw1.close()
		fw2.close()


