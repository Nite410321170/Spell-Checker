##############################################
#
#		TuWorld Slader
#
#		410321170
#
#		Pattern Recognition Assignment 2
#
#############################################

"""
NON-CASE SENSITIVE
"""

import sys
import numpy as np

## Files
##########
IN_FILE="dictionary.txt"
#The maximum edit distance of a word for it to be considered a suggestion.
editLIMIT = 3

##  Collecting dictionary
#############################
try:
	ip=open(IN_FILE,"r")
except:
	print("Import file missing")
	sys.exit(0)
#The words in the dictionary.
wordList=ip.read().splitlines()

##  Functions
##############
#Calculates the diagonal distance.
def diagDist(i, j, word1, word2):
	if word1[i-1].lower() == word2[j-1].lower():
		return 0
	return 1
#Finds the Levenstein Distance between two words.
def LevensteinDis(word1, word2):
	D = np.zeros((len(word1)+1, len(word2)+1))
	
	for x in range(1,len(word1)+1):
		D[x][0] = D[x-1][0] + 1
	for y in range(1,len(word2)+1):
		D[0][y] = D[0][y-1] + 1
	
	for x in range(1,len(word1)+1):
		for y in range(1,len(word2)+1):
			#Diagonal transition.
			D_D = D[x-1][y-1] + diagDist(x, y, word1, word2)
			#Horizontal transition.
			H_D = D[x-1][y] + 1
			#Vertical transition.
			V_D = D[x][y-1] + 1
			D[x][y] = min(D_D,H_D,V_D)
			
	return int(D[len(word1)][len(word2)])

#Creates a set for faster searching if the word is in the dictionary.
wordListSET = set()
for x in wordList:
	wordListSET.add(str.lower(x))
	
inpWord = input("NON-CASE SENSITVE Spell Checker (type 'end' to end)\nWord: ")
while(inpWord!="end"):
	editValue = 1
	x=0
	autoCorrect = []
	#Creates a list of lists to hold the suggested words.
	for x in range(editLIMIT):
		autoCorrect.append([])
	#Searches for the word in the dictionary.
	#Set is used to speed up search.
	if(str.lower(inpWord) in wordListSET):
		print("Word is correctly spelt\n")
	else:
		#Searches entire dictionary for close words.
		while(x<len(wordList)):
			#Excludes words that are either too long or too short to
			# generate Edit distances less than or equal to the set editLIMIT.
			if(abs(len(wordList[x]) - len(inpWord))<=editLIMIT):
				editValue = LevensteinDis(inpWord, wordList[x])
				if editValue<=editLIMIT:
					#Words with edit distance values of 1 are places in the first list, words
					#with edit distance values of 2 are placed in the 2nd list, etc.
					#This is done for easier sorting of the suggestions based on their edit distance.
					autoCorrect[editValue-1].append(wordList[x])
			x+=1

		counter=1
		#Prints out the correct spelling suggestions in alphabetic and ascending order 
		# of the edit distance.
		for x in range(editLIMIT):
			#Just a little extra space so the words with a different edit distance can be better seen.
			if(len(autoCorrect[x])>0): print("")
			for y in range(len(autoCorrect[x])):
				print(str(counter)+".",autoCorrect[x][y],"\t\t",end="")
				counter+=1
				#Prints 3 words on the same line to save space.
				if(y%3 == 2 or y==(len(autoCorrect[x])-1)):
					print("")
		
	inpWord = input("\nNON-CASE SENSITVE Spell Checker (type 'end' to end)\nWord: ")