import random
from colorama import Fore,init
init(autoreset=True)

def print_sudoku(grid, in_evidence=None):

	for i in range(9):

		if(i==3 or i==6): print() # skip line every 3 rows

		for j in range(9):

			if(j==3 or j==6): print(" ", end = "") # space between 3 elements in row

			if in_evidence is not None and i==in_evidence[0] and j==in_evidence[1]:
				print(Fore.RED + str(grid[i][j]), end = " ")
			else:
				print(grid[i][j], end = " ")
		
		print()

	print("")


def is_element_valid(grid, a, b):
	# print("is ", grid[a][b], " valid.... ?")

	# print_sudoku(grid,in_evidence=[a,b])

	# check col
	for i in range(0,9):
		if grid[a][b] == grid[i][b] and i!=a: 
			# print(Fore.RED + str("not valid, in same col"))
			# print_sudoku(grid, in_evidence=[i,b])
			return False # is not valid
	
	# check row
	for j in range(0,9):
		if grid[a][b] == grid[a][j] and j!=b: 
			# print(Fore.RED + str("not valid, in same row"))
			# print_sudoku(grid, in_evidence=[a,j])
			return False # is not valid

	box_row = a//3 # integer division
	box_col = b//3

	for i in range(box_row*3, box_row*3+3):
		for j in range(box_col*3, box_col*3+3):
			if grid[a][b] == grid[i][j] and a!=i and b!=j: 
				# print(Fore.RED + str("not valid, in same box"))
				# print_sudoku(grid, in_evidence=[i,j])
				return False # is not valid

	# print("element is valid")

	return True # else, is valid



def fill_diagonals(grid):
	print("Filling diagonal boxes...")

	nums = list(range(1, 10))
	random.shuffle(nums) # shuffle list from 1 to 9

	for k in range(0,9,3): # 3 diagonal boxes
		n=0
		for i in range(0+k,3+k):
			for j in range(0+k,3+k):

				grid[i][j] = nums[n] # try a number
				n+=1

		# random.shuffle(nums) # re-shuffle for each diagonal box

	print("Done.")



def fill_remaining(grid):
	print("Filling remaining elements...")

	nums = list(range(1, 10))
	random.shuffle(nums) # shuffle list from 1 to 9
	# print(nums)

	for i in range (9):
		for j in range(9):
			if grid[i][j] == 0: # not filled yet
				# print_sudoku(grid, in_evidence=[i,j])
				n = 0
				is_valid = False

				while not is_valid : # continue until value works in grid
					# print("trying " , nums[n])
					grid[i][j] = nums[n] # try a number
					is_valid = is_element_valid(grid, i, j) # check if valid
					# print("is valid ? ", is_valid)
					n+=1 # move to next number value
					
					if n == 9 and not is_valid: # all tries failed
						print(Fore.RED + str("no correct value was found. Abandon."))
						print()
						print_sudoku(grid, in_evidence=[i,j])
						grid[i][j] = 0
						return False

	print("Done.")
	return True

def removeElements(grid, k):

	resulting_grid = [[0 for _ in range(9)] for _ in range(9)] # empty grid

	return resulting_grid

def is_uniquely_solvable():
	return False



def build_sudoku():
	print('Lets build a full sudoku grid !')

	success = False
	x=0

	while not success and x<100: # max a 100 tries
		sudoku_grid = [[0 for _ in range(9)] for _ in range(9)] # empty grid
		fill_diagonals(sudoku_grid)
		success = fill_remaining(sudoku_grid)
		x+=1

	if success:
		print(Fore.BLUE + str("Success"))
		print_sudoku(sudoku_grid)

	print (x ," tries.")

	removeElements(sudoku_grid, 17)

if __name__ == '__main__':
	build_sudoku()

