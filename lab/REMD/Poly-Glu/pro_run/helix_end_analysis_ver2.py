from subprocess import call 
import os


def input_analysis(path, input):
	R_list = []
	L_list = []
	R_L_list = []
	No_list = []	
	cnt = 0

	fr1 = open("%s/analysis/dssp_analysis/%s" % (path,input[0]), "r")
	fr2 = open("%s/analysis/end_to_end_analysis/%s" % (path, input[1]), "r")

	while True:
		line = fr1.readline()
		if "STEPS All_helix All_R 310_R alphaR" in line:break

	for line1, line2 in zip(fr1.readlines(), fr2.readlines()):
		R_num = int(line1.strip().split()[2])
		L_num = int(line1.strip().split()[6])

                if R_num >= 1 and L_num >= 1: # The both of right-handed helix and left-handed helix            
                        R_L_list.append(line1.strip() + " " + line2.strip().split()[1] + "\n")
			cnt += 1
		else:
			if R_num >= 1 and L_num == 0: # Only right-handed helix
				R_list.append(line1.strip() + " " + line2.strip().split()[1] + "\n")
				cnt += 1
			elif R_num == 0 and L_num >= 1: # Only left-handed helix
				L_list.append(line1.strip() + " " + line2.strip().split()[1] + "\n")
				cnt += 1
			else:
				No_list.append(line1.strip() + " " + line2.strip().split()[1] + "\n")
				cnt += 1
	fr1.close()
	fr2.close()
	
	return cnt, R_list, L_list, R_L_list, No_list

if __name__ == "__main__":

	path = os.getcwd() 	           # The "path" is "current directory".
	
	input = ["The_number_of_helix.txt","end_to_end_NC.txt"]
	out = ["R_helix_end.txt", "L_helix_end.txt", "R_L_helix_end.txt","No_helix_end.txt"]	

	swap_helix_end = list(input_analysis(path, input))
	cnt = swap_helix_end[0]
	helix_end = swap_helix_end[1:]
	os.chdir("%s/analysis" % path)
	call(["mkdir","-p","helix_end_analysis"])
	os.chdir("%s/" % path)

	for name,h_e in zip(out,helix_end):
		fw = open("%s" % name, "w")
		fw.write("#Ratio\n")	 
		fw.close()
		fw = open("%s" % name, "a")
		fw.write("%s\n" % str(len(h_e)/float(cnt)))
		fw.write("#Step All_helix All_R 310_R alphaR PaiR All_L 310_L alphaL PaiL end\n")
		for line in h_e:
			fw.write(line)
		fw.close()

		call(["mv","-f","%s/%s" % (path,name),"%s/analysis/helix_end_analysis/%s" % (path,name)]) 	
	

