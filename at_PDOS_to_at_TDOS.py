#each PDOS_Sss_Aaaaa.OUT (partial DOS) file is for a single symmetrically unique atom of species ss and atom aaaa. 
#in PDOS, each symmetrised (l, m)-projection is written consecutively (in a block) and separated by blank lines. So, each block corresponds to a unique (l, m) [in increasing order of (l, m)].
#takes PDOS_Sss_Aaaaa.OUT file and adds the PDOS for all (l,m) projection to give atomic total_DOS for this particular atom.
#the 1st column is identical for all blocks.

import sys

rfilename = sys.argv[1] #PDOS_Sss_Aaaaa.OUT
at_PDOS_file = open(rfilename, "r")
array = []


#collecting just the first block of PDOS_Sss_Aaaaa.OUT file in a 2-column array with columns being: E  \t  DOS.
#the 2nd column is fetched from the subsequent blocks and are added to the DOS column of the above array. 

for line in at_PDOS_file:
	
	#if not a linebreak
	if line != "     \n":
		l = list(line)

		#getting x value for this line for E < 0
		if l[0] == " " and l[1] != " ":
			x = ""
			for i in range(1,len(l)):
				if l[i] != " ":
					x = x + l[i]
				else:
					break
			x = float(x)
			y = ""

			#getting y value for this line
			for j in range(i, len(l)):
				if l[j] != " " and l[j] != "\n":
					y = y + l[j]

			y = float(y)
			
		#getting x value for this line E >= 0
		elif l[0] == " " and l[1] == " ":
			x = ""
			for i in range(2,len(l)):
				if l[i] != " ":
					x = x + l[i]
				else:
					break
			x = float(x)
			y = ""

			#getting y value for this line
			for j in range(i, len(l)):
				if l[j] != " " and l[j] != "\n":
					y = y + l[j]

			y = float(y)

		#putting x, y values of this line into array
		array.append([x,y])

	#if a linebreak
	else:
		break


line_num = 0


#taking the subsequent blocks and adding up all the DOS for each block to the 2nd column of the main array for each value of E.

for line in at_PDOS_file:
	
	#if a linebreak, don't append line_num
	if line == "     \n":
		line_num = 0
		continue

	#if not a linebreak, keep fetching	
	else:
		
		l = list(line)
		#going over the region of x value for this line for E < 0 (note: we do not need this value since it was already fetched from the first block)
		if l[0] == " " and l[1] != " ":
			for i in range(1,len(l)):
				if l[i] == " ":
					break

			y = ""
			#getting y value for this line
			for j in range(i, len(l)):
				if l[j] != " " and l[j] != "\n":
					y = y + l[j]

			y = float(y)
			
		#going over the region of x value for this line for E >= 0 (note: we do not need this value since it was already fetched from the first block)
		elif l[0] == " " and l[1] == " ":
			for i in range(2,len(l)):
				if l[i] == " ":
					break
			y = ""
			#getting y value for this line
			for j in range(i, len(l)):
				if l[j] != " " and l[j] != "\n":
					y = y + l[j]

			y = float(y)

		#adding the value of y for this particular line to the previous array element
		array[line_num][1] = array[line_num][1] + y
		line_num = line_num + 1  


#wfilename = "at_TDOS_Sss_Aaaaa.OUT" w/o quotation marks.
#rfilename = "PDOS_Sss_Aaaaa.OUT" w/o quotation marks.
wfilename = "at_T"+rfilename[1:len(rfilename)]
at_TDOS_file = open(wfilename, "w")

#writing array to file
for i in range(0, len(array)):
	at_TDOS_file.write(str(array[i][0])+"  " + str(array[i][1]) + "\n")


#in output file, the array looks like:
#E1 \t sum over all (l,m) for E1
#E2 \t sum over all (l,m) for E2
#E3 \t sum over all (l,m) for E3
#E4 \t sum over all (l,m) for E4
#....
#En \t sum over all (l,m) for En