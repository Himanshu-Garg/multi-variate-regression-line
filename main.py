import math

"""

Here, data is in the form (journal_name;SJR;H-Index;Total docs(3 yrs);total refs;total cites;citable docs;cites/docs;ref/doc;Impact_factor)
i.e. each is seperated by a semi-colon (;)

We have to obtain the regression line

"""

#----------------------------------------------------------------------------------
import numpy as np
def matrixmultiply (A, B):
	a=np.array(A)
	b=np.array(B)
	return np.matmul(a,b)

def returnPowerSet(set,set_size): 
      
    # set_size of power set of a set 
    # with set_size n is (2**n -1) 
    pow_set_size = (int) (math.pow(2, set_size)); 
    counter = 0; 
    j = 0; 
    ans=[]
      
    # Run from counter 000..0 to 111..1 
    for counter in range(0, pow_set_size):
        s=""
        for j in range(0, set_size): 
              
            # Check if jth bit in the  
            # counter is set If set then  
            # print jth element from set  
            if((counter & (1 << j)) > 0): 
                #print(set[j], end = ";");
                s=s+str(set[j])+" "
                #ans.append(str(set[j])+" ") 
        #print("");
        ans.append(s[:-1])
    #print(ans[1:])
    return ans[1:] 


def transposeMatrix(m):
    return list(zip(*m))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    a=np.array(m)
    return float(np.linalg.det(a))

    

def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors


#print(  getMatrixInverse([[8,2],[7,3]])  )

#--------------------------------------------------------------------------------------
# class to store each combination and it's mean square error and absolute error
class combo(object):											
    """__init__() functions as the class constructor"""
    def __init__(self, combination=None, abs_error=None, mean_square_error=None):
        self.combination = combination
        self.abs_error = abs_error
        self.mean_square_error=mean_square_error


#--------------------------------------------------------------------------------------
file_from = open("merging data/processed_data.txt","r")
open('output.txt', 'w').close()				#to erase all the contents in that file
file_to = open("output.txt","a")

data=file_from.readlines()
n=len(data)							# n = no. of journals 

combo_list=[]

set=[1,2,3,4,5,6,7,8]			#set contains all the inputs
power_set = returnPowerSet(set,8)				#power_set contains all the possible combinations
#print(type(power_set))
to_choose=int(80/100*n) 					# equivalent to 8-% of n

for input_combination in power_set:
	#print(type(input_combination))
	inn=list(map(int,input_combination.split(" ")))
	absolute_error_final=10000000
	square_error_final=100000000

	#print(inn)
	for i in range(0,n - to_choose + 1):
		matrix_X=[]							# input matrix of all columns
		matrix_Y=[]							# output matrix (IF)
		for j in range(i,i+to_choose-1):
			temp_data=list(map(str,data[j].split(";")))
			jrow=[1]
			for k in inn:
				#print(";" + (temp_data[k]) + ";")
				jrow.append(float(temp_data[k][1:-1]))
			matrix_X.append(jrow)
			matrix_Y.append([float(temp_data[9])])

		
		X_transpose=transposeMatrix(matrix_X)
		#print(type(X_transpose))
		#print(len(X_transpose),len(X_transpose[0]))
		#print(len(matrix_X),len(matrix_X[0]))
		XtransX=matrixmultiply(X_transpose,matrix_X)
		#print(XtransX)
		XtransX_inverse=np.linalg.inv(XtransX)
		matrix_B=matrixmultiply(matrixmultiply(XtransX_inverse,X_transpose),matrix_Y)			# B = values of B in regression line
		#print(matrix_B)

		
		sum_abs_error=0
		sum_square_error=0
	
		#print(temp_data[k])
		
		# to find the error % in each test case combination ...
		for j in range(0,i+1):
			kk=0
			expected_y=matrix_B[0]
			for k in inn:
				expected_y+=float(temp_data[k][1:-1])*matrix_B[kk]
				kk=kk+1
			sum_abs_error+=abs(float(temp_data[9][1:-1]) - expected_y)
			sum_square_error+=(float(temp_data[9][1:-1]) - expected_y)**2

		for j in  range(i+to_choose,n):
			expected_y=matrix_B[0]
			kk=0
			for k in inn:
				expected_y+=float(temp_data[k][1:-1])*matrix_B[kk]
				kk=kk+1
			sum_abs_error+=abs(float(temp_data[9][1:-1]) - expected_y)
			sum_square_error+=(float(temp_data[9][1:-1]) - expected_y)**2

		if abs(sum_abs_error)<absolute_error_final:
			absolute_error_final=abs(sum_abs_error)
			
		if abs(sum_square_error)<square_error_final:
			square_error_final=sum_square_error
	combo_list.append(combo(str(input_combination),absolute_error_final,square_error_final))
	#print("error for - " + str(input_combination) + "   ---   " + str(absolute_error_final))

#-------------------- for printing output -------------------------------
import operator
combo_list.sort(key=operator.attrgetter('abs_error'))

file_to.write("AS PER --- MEAN ABSOLUTE ERROR IN ASCENDING ORDER IS AS FOLLOWS" + "\n\n")

file_to.write("1 = SJR " + "\n" + "2 = H-Index" + "\n" + "3 = Total docs (3 yrs)" + "\n" + "4 = Total references" + "\n" + "5 = Total cites" + "\n" + "6 = Citable docs" + "\n" + "7 = Cites/Doc" + "\n" + "8 = Reference/Doc" + "\n")

file_to.write("\n" + "combination  ----------  mean absolute error  ------------ mean square error " + "\n")


N=len(combo_list)
for i in range(17):
	s="error for - " + str(combo_list[i].combination) + "  ----  " + str(combo_list[i].abs_error/n) +"  ----  " + str(combo_list[i].mean_square_error/n) + "\n"
	file_to.write(s)

	
file_from.close()
file_to.close()


