#this code uses the results (ie, all the at_TDOS_Sss_Aaaaa.OUT files) produced by at_PDOS_to_at_TDOS.py for all the PDOS_Sss_Aaaaa.OUT files for this crystal.
#I didn't write a script to run at_PDOS_to_at_TDOS.py for all files at once. I will do it some other day. 


import sys

#function to count the number of digits in a number
def count_digits(num):
	return len(str(num))


nspecies = 2 #number of different types of elements aka species
natoms = [0, 12, 18] #no of atoms for each species; natoms[0] = 0 (always, for convenience)

wfilename = sys.argv[1] #input the name of the final cr_TDOS file that will be produced by this code
cr_TDOS_file = open(wfilename, "w")

array = []

#Initializing first column of array with E from first file.
first_rfilename = "at_TDOS_S01_A0001.OUT" #file produced after running at_PDOS_to_at_TDOS.py on a PDOS_S01_A0001.OUT file
atTDOS_file = open(first_rfilename, "r")
for line in atTDOS_file:
	first_space = line.find(" ")
	x = float(line[0:first_space])
	array.append([x, 0.0])


#Putting the DOS values in second column and summing over all at_TDOS files.
#starts with deciding the name of at_TDOS_Sss_Aaaaa.OUT file that needs to be opened. 
for species in range(1, nspecies+1): #deciding the species number
	print("species=", species)
	if count_digits(species) == 1:
		rfilename = "at_TDOS_S0" + str(species)+"_A"
	elif count_digits(species) == 2:
		rfilename = "at_TDOS_S" + str(species)+"_A"
	
	for atoms in range(1, natoms[species]+1): #deciding which atom of the current species; updating the filename
		print("atom = ", atoms)
		if count_digits(atoms) == 1:
			rfilename_upd = rfilename + "000" + str(atoms)+".OUT"
		elif count_digits(atoms) == 2:
			rfilename_upd = rfilename + "00" + str(atoms)+".OUT"
		elif count_digits(atoms) == 3:
			rfilename_upd = rfilename + "0" + str(atoms)+".OUT"
		elif count_digits(atoms) == 4:
			rfilename_upd = rfilename + str(atoms)+".OUT"

		#filename decided; opening the file for reading.
		at_TDOS_file = open(rfilename_upd, "r")

		line_num = 0
		for line in at_TDOS_file:
			first_space = line.find(" ") #ignoring the x-value of the file containing Energy value since that has already been fetched from the first at_TDOS file; it is same in all the at_TDOS file.
			y = ""
			#getting the value of y for this line
			for j in range(first_space, len(line)):
				if line[j] != " " and line[j] != "\n":
					y = y + line[j]

			y = float(y)

			array[line_num][1] += y  #adding the y-value to the previous y-value for this line
			line_num += 1  #appending line_num

		#closing the current file
		at_TDOS_file.close()


#Adding the second column from the interstitial DOS aka IDOS.OUT file to the second column of array
#There is just one IDOS.OUT file for the entire crystal
IDOS_rfilename = "IDOS.OUT"
IDOS_file = open(IDOS_rfilename, "r")
line_num = 0
for line in IDOS_file:
	if line != "     \n":
		l = list(line)
		if l[0] == " " and l[1] != " ":
			for i in range(1,len(l)):
				if l[i] == " ":
					break

			y = ""
			for j in range(i, len(l)):
				if l[j] != " " and l[j] != "\n":
					y = y + l[j]

			y = float(y)
			

		elif l[0] == " " and l[1] == " ":
			for i in range(2,len(l)):
				if l[i] == " ":
					break
			y = ""
			for j in range(i, len(l)):
				if l[j] != " " and l[j] != "\n":
					y = y + l[j]

			y = float(y)

		array[line_num][1] += y
		line_num += 1


#Writing the Crystal_TDOS to file
#Crystal_TDOS(E) = sum over at_TDOS(E) + IDOS(E)
cr_TDOS_file = open(wfilename, "w")
for i in range(0, len(array)):
	cr_TDOS_file.write(str(array[i][0]) + "  " + str(array[i][1]) + "\n")


#finally, the cr_TDOS file was plotted along with the TDOS.OUT file produced directly form Elk on the same graph.
#It matched exactly. Yay!