from Search import Search

'''
To Do:
	1) Parse Args
	2) Parse queryfile to read and generate file finally
	3) Match all the submission instructions
	4) Search for better saving and loading techniques
	5) Run of full fledged dataset
	6) Make a priority queue data structure, to reduce the ranking time
	7) Think about evaluation strategy
'''


if __name__ == '__main__':
	search = Search('./indexfile.dict', './indexfile.idx')
	query = "Viet* has former officers."
	ranklist = search.get_ranking_list(query)
	print(ranklist)