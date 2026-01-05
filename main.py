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
	# print("Filling diagonal boxes...")

	nums = list(range(1, 10))
	random.shuffle(nums) # shuffle list from 1 to 9

	for k in range(0,9,3): # 3 diagonal boxes
		n=0
		for i in range(0+k,3+k):
			for j in range(0+k,3+k):

				grid[i][j] = nums[n] # try a number
				n+=1

		# random.shuffle(nums) # re-shuffle for each diagonal box

	# print("Done.")



def fill_remaining(grid):
	# print("Filling remaining elements...")

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
					
					if n == len(nums) and not is_valid: # all tries failed
						#print(Fore.RED + str("no correct value was found. Abandon."))
						#print()
						#print_sudoku(grid, in_evidence=[i,j])
						grid[i][j] = 0
						return False

	# print("Done.")
	return True

def removeElements(grid, k):

	print("Removing k elements from grid...")

	while k > 0:

		# pick random
		i = random.randint(0,8)
		j = random.randint(0,8)

		if grid[i][j] != 0: # not already emptied
			grid[i][j] = 0
			k -= 1

	print("Done.")

def get_candidates(grid):

	nums = list(range(1, 10))
	random.shuffle(nums) # shuffle list from 1 to 9

	candidates = {}

	for i in range(0,9):
			for j in range(0,9):

				if grid[i][j] == 0: # cell to be filled
					candidates[(i, j)] = []
					n=0

					while n < len(nums):
						grid[i][j] = nums[n]
						is_valid = is_element_valid(grid, i, j)
						if is_valid:
							candidates[(i,j)].append(nums[n])

						n+=1
						grid[i][j] = 0
	
	return candidates

def sort_candidate(candidates):

	sorted_candidates = dict(sorted(candidates.items(), key=lambda item: len(item[1])))
	return sorted_candidates

def solve(grid, sorted_candidates):
	# fill empty cells that only have a single candidate
	to_remove = []

	for (i, j), vals in sorted_candidates.items():
	    if len(vals) == 1:  # only one possibility
	        grid[i][j] = vals[0]
	        to_remove.append((i, j))

	for key in to_remove:
	    sorted_candidates.pop(key)

	print(sorted_candidates)

	solutions = recursive_solve(grid, sorted_candidates, 0)
	return solutions

def recursive_solve(grid, candidates, solutions):

	if not candidates:
		solutions += 1
		return solutions


	# Try remaining possibilities
	for (i, j), vals in candidates.items():
		for n in vals:
			grid[i][j] = n

			# find new candidates
			new_candidates = get_candidates(grid)
			new_candidates = sort_candidate(new_candidates)

			# recurse
			if recursive_solve(grid, new_candidates, solutions):
				solutions += 1
				grid[i][j] = 0
				return solutions

			# Backtrack
			grid[i][j] = 0

	return solutions


def is_uniquely_solvable(grid):

	candidates = get_candidates(grid)
	# print(candidates)

	sorted_candidates = sort_candidate(candidates)
	#print(sorted_candidates)

	# find all possible solutions
	solutions = solve(grid, sorted_candidates)
	print(solutions, " solution(s) found.")
	if solutions == 1:
		print(Fore.BLUE + str("This sudoku grid is uniquely solvable !"))

def build_sudoku():
	print('Lets build a full sudoku grid !')

	success = False
	x = 0

	while not success:
		sudoku_grid = [[0 for _ in range(9)] for _ in range(9)] # empty grid
		fill_diagonals(sudoku_grid)
		success = fill_remaining(sudoku_grid)
		x+=1

	if success:
		print(Fore.BLUE + str("Success"))
		print (x ," tries.")

		print_sudoku(sudoku_grid)

		removeElements(sudoku_grid, 17)
		print_sudoku(sudoku_grid)

		is_uniquely_solvable(sudoku_grid)

	else:
		print(Fore.RED + str("Fail. More than 100 tries to find a full grid."))



if __name__ == '__main__':
	build_sudoku()

