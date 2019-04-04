file1 = open("IF.txt","r")
file2 = open("inputs.txt","r")
open('processed_data.txt', 'w').close()				#to erase all the contents in that file
file3 = open('processed_data.txt',"a")


data1=file1.readlines()
data2=file2.readlines()

n1=len(data1)
n2=len(data2)

for i in range(1,n2):
	temp2=list(map(str,data2[i].split(";")))
	comp2=temp2[2].replace(" ","")									#to remove white spaces
	comp2=comp2.replace("-","")										#to remove -
	comp2=comp2.replace("/","")										#to remove /
	comp2=comp2.replace(",","")										#to remove ,
	comp2=(comp2.replace(":","")).lower()							#to remove "-" characters
	comp2=comp2[1:-1]

	for j in range(0,n1):
		temp1=list(map(str,data1[j].split(";")))
		comp1=temp1[1].replace(" ","")					#to remove white spaces
		comp1=comp1.replace(":","")										#to remove -
		comp1=comp1.replace("/","")										#to remove /
		comp1=comp1.replace(",","")										#to remove ,
		comp1=(comp1.replace("-","")).lower()						#to remove "-" characters
		if(comp1==comp2):
			s=temp1[1] + " ; " + temp2[5].replace(",","")+ " ; " + temp2[7].replace(",","") + " ; " + temp2[9].replace(",","")+ " ; " + temp2[10].replace(",","")+ " ; " + temp2[11].replace(",","")+ " ; " + temp2[12].replace(",","")+ " ; " + temp2[13].replace(",","")+ " ; " + temp2[14].replace(",","")+ " ; " + temp1[2].replace(",","") 
			file3.write(s)
			break;
