import numpy as np
from egcd import egcd


alpha='abcdefghijklmnopqrstuvwxyz '				#notice that space is also a character, with the index as 26. therefore, the modulus will now be mod(27)
letter_to_ind=dict(zip(alpha, range(len(alpha))))   #dictionary to store a=0, b=1 blah blah
ind_to_letter=dict(zip(range(len(alpha)), alpha))	#dictionary to go from indexing to letters, ie, 0=a, 1=b, blah blah
mod=len(alpha)+1


def encrypt(pt, k) : 
	#pass pt and key as arguements, convert pt to numbers
	#convert pt to a column matrix according to the key so matrix multiplication is possible
	# use the formula ct=pt*k%26 to encrypt the given pt
	#convert numbers back to text , return cipher text to main function

	enc_text=""
	pt_as_num=[]
	
	for i in pt :
		pt_as_num.append(letter_to_ind[i])		#converted plain text to respective index numbers

	#split numbered plain text to list items having same  number of columns as key to make sure matrix multiplication works

	split_pt = [pt_as_num [ j : j+int(k.shape[0]) ] for j in range (0, len(pt_as_num), int(k.shape[0] )) ]		 	

	for p in split_pt :
		p = np.transpose(np.asarray(p))[ : , np.newaxis]	#converted list items from above to arrays (using them row by row, so its the same as single row matrices)
														# np.newaxis is used because numpy does matrix calculations in ways unknown to humankind	
		while p.shape[0] != k.shape[0] :					#checking if the matrix of the plain text is complete or not , otherwise appending a space at the end to m ake it a complete matrix
			p=np.append(p, " ")[ : , np.newaxis]
		num_pt = np.dot(k,p) % mod							#here is where the actual encoding happens, the much required multiplication and modulus function

		for i in range (num_pt.shape[0]) :						#converting the numbers back to letters and returning the encrypted text
			n = int(num_pt[i,0]) 
			enc_text += ind_to_letter[n]

	return enc_text 
	#pass


def decrypt(ct, kinv) : 
	#pass ct and inverse of key matrix as arguements, convert ct to numbers
	#convert ct to a column matrix according to the inverse of key so matrix multiplication is possible
	# use the formula pt=ct*kinv%26 to decrypt the given pt
	#convert numbers back to text , return plain text to main function

	dec_text=""
	ct_as_num=[]
	
	for i in ct :
		ct_as_num.append(letter_to_ind[i])		#converted cipher text to respective index numbers

	#split numbered cipher text to list items having same  number of columns as key inverse to make sure matrix multiplication works

	split_ct = [ct_as_num [ j : j+int(kinv.shape[0]) ] for j in range (0, len(ct_as_num), int(kinv.shape[0] )) ]		 	

	for c in split_ct :
		c = np.transpose(np.asarray(c))[ : , np.newaxis]	#converted list items from above to arrays (using them row by row, so its the same as single row matrices)
														# np.newaxis is used because numpy does matrix calculations in ways unknown to humankind	
		while c.shape[0] != kinv.shape[0] :					#checking if the matrix of the plain text is complete or not , otherwise appending a space at the end to m ake it a complete matrix
			c=np.append(c, " ")[ : , np.newaxis]
		num_ct = np.dot(kinv,c) % mod							#here is where the actual encoding happens, the much required multiplication and modulus function

		for i in range (num_ct.shape[0]) :						#converting the numbers back to letters and returning the encrypted text
			n = int(num_ct[i,0]) 
			dec_text += ind_to_letter[n]

	return dec_text 
	#pass


def mat_key_inv(key, mod) : 
	#pass key matrix,  and the required modulus(26 as mentioned in the previous functions) as arguements
	#convert the message into a matrix following the required modulus
	#returns the inverse of the given matrix in the required modulus

	det=int(np.round(np.linalg.det(key)))	#finds the determinant of the matrix : message
	det_inv=egcd(det, mod)[1] % mod	#finds det of the inverse of the matrix in the required modulus
	key_inv_matrix = det_inv * np.round(det * np.linalg.inv(key)) % mod	

	return key_inv_matrix	
	#pass


def main() : 
	#all user input, calling functions, displaying output blah blah is done here

	key=np.array([[3,6],[2,9]])
	plaintext = 'help'
	encrypted_text = encrypt(plaintext, key)
	key_inv = mat_key_inv(key, mod)
	decrypted_text = decrypt(encrypted_text, key_inv)
	print("original message : ", plaintext)
	print("encrypted text : ", encrypted_text)
	print("message after decryption : ", decrypted_text)


main()
