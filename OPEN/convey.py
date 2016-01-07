import time
import authenticate as au
import os

# DEBUGGING
# lists the sheets available to gspread
def list_available_sheets(gc):
	all_sheets = []
	for sheet in gc.openall():
		all_sheets.append("{}".format(sheet.title))
	return all_sheets

# Opens a spreadsheet for r/w
# spreadsheets must be hosted on gdrive and shared with
# open-service@pairing-gui.iam.gserviceaccount.com
def open_sheet(spreadsheet):
	
	#retrieve path to the json file and authenticate with google
	pathfile = open('path2secretfile.txt', 'r')
	path2secretfile = pathfile.readline()[:-1]
	gc = au.LOAD(path2secretfile)
		

	# Open the spreadsheet, throws exception if sheet does not exist
	sheet = gc.open(spreadsheet).sheet1

	return sheet


#list all values in a specified column below the header
def list_col_values(sheet_name, col_num):
	
	#Array of size 100/1000 by default due to google initialization
	sheet = open_sheet(sheet_name)

	#Get the column values and pass them to th user
	val = sheet.col_values(col_num)
	values = val[1::] # index 0 column value is column information
	return values

# return a list in the column number specified without empty values
def names_no_null(sheet_name, col_num):
	array = list_col_values(sheet_name, col_num)
	return [y for y in array if y != '']

#given a sheet name and list of names this function
#writes those names to the given sheet in the given column
def rewrite_column(sheet_name, col_num, new_list_of_names):
	
	sheet = open_sheet(sheet_name)

	length = len(new_list_of_names)
	
	# Copy new list of names over to the sheet
	for i in range(0, length):
		#i+2 because it must start at first index and sheets are 1 indexd
		sheet.update_cell(i + 2, col_num, new_list_of_names[i])
	
	# Overwrite next 20 values as a precaution
	for i in range(length + 2, length+20):
		sheet.update_cell(i, col_num, "")


# search a row within a sheet for a value
def search_row(sheet, row_num, value):

	#find the first empty row in column 1 to update in.
	array = sheet.row_values(row_num)
	
	# find the value and return its index
	for i in range(0, len(array)):
		if array[i].lower().strip() == value.lower().strip():
			return i + 1 # +1 as sheets are 1 indexed
	
	return len(array)


# Searches a column for a value
# Only works if there are no empty cells between values
def search_column(sheet, col_num, value):
	
	#find the first empty row in column 1 to update in.
	array = sheet.col_values(col_num)

	# find the value and return its index
	length = len(array)
	for i in range(0, length):
		if array[i].lower().strip() == value.lower().strip():
			return i+1

	return length


# Given a pair, add them to the current pairings and all pairing sheets
def add_pair(chosen_pair):

	#Find the first empty row within the column and update it for both spreadsheets
	for element in ["Current-Pairings", "All-Pairings"]:
		sheet = open_sheet(element)
		
		first_empty_row = search_column(sheet, 1, '')
		
		#given array should be of form, [warrior, friend]
		sheet.update_cell(first_empty_row, 1, chosen_pair[0])
		sheet.update_cell(first_empty_row, 2, chosen_pair[1])
		
		the_time = time.strftime("%m-%d-%y", time.gmtime())
		sheet.update_cell(first_empty_row, 3, the_time)



# removes names from the queue number times
# sheet_name specifies the sheet that the queue is in
# either 'Current-Pairings' or "All-Pairings"
def remove_from_queue(sheet_name, name, number=1):

	#return all names in current
	current_names = names_no_null(sheet_name, 1)

	times_removed = 0
	new_names = []

	for element in current_names:
		# if we have not removed the user 'number' times, dont append the 
		# name to the new array. Otherwise append all names to new_names
		if element.lower().strip() == name.lower().strip() and times_removed < number:
			times_removed += 1
		else:
			new_names.append(element.strip())

	rewrite_column(sheet_name, 1, new_names)


# adds the list of names to the queue specified in the sheet
def add_to_queue(sheet_name, list_of_names):
	
	# get the current list of names and append list_of_names to it
	names = names_no_null(sheet_name, 1)
	for element in list_of_names:
		names.append(element)
	
	# rewrite the column within the spreadsheet
	rewrite_column(sheet_name, 1, names)
	

# Gets info from the warrior sheet based on specified datatype
# datatype: 'info', 'contact'
def get_warrior_info(warrior_name, datatype):
	sheet = open_sheet('Chat-Form-Responses')
	
	array = sheet.col_values(2)

	#Find the appropriate row
	row = 0
	length = len(array)
	while row < length:
		if array[row] == '':
			row += 1
			continue
		elif array[row].lower().strip() == warrior_name.lower().strip():
			row += 1
			break #arrays 0 indexed, sheets 1 indexed

		row += 1

	#return the appropriate value from the sheet
	if row < length:
		data = sheet.row_values(row)
		if datatype == 'info':
			sex = data[2]
			year = data[6]
			interests = data[7]
			hobbies = data[8]
			struggle = data[10]
			return [sex, year, interests, hobbies, struggle]
		elif datatype == 'contact':
			method = data[3]
			phone = data[4]
			email = data[5]
			return [method, phone, email]
		else:
			return['']
	else:
		return ['','','','','']
	

# Gets info from the friends sheet based on specified datatype
# datatype: 'info', 'contact'
def get_friend_info(friend_name, datatype):
	sheet = open_sheet('Friend-Form')
	
	array = sheet.col_values(18)

	#Find the appropriate row
	row = 0
	length = len(array)
	while row < length:
		if array[row] == '':
			row += 1
			continue
		elif array[row].lower().strip() == friend_name.lower().strip():
			row += 1
			break #arrays 0 indexed, sheets 1 indexed

		row += 1

	# if the row is valid get the data corresponding to the datatype and pass it to the user
	if row < length:
		data = sheet.row_values(row)
		if datatype == 'info':
			sex = data[3]
			year = data[4]
			major = data[5]
			interests = data[6]
			hobbies = data[12]
			return [sex, year, major, interests, hobbies]
		elif datatype == 'contact':
			phone = data[8-1]
			email = data[9]
			return [phone, email]
		else:
			return ['']
	else:
		return ['','','','','']

#Removes a pair from Current-Pairings sheet
#pair: [warrior, friend]
def remove_pair(pair):
	cp = open_sheet('Current-Pairings')
	
	#search sheet for a row with pair 
	one = cp.col_values(1)
	two = cp.col_values(2)
	length = len(one)
	i = 0
	while i < length:
		if one[i].lower().strip() == pair[0].lower().strip() and two[i].lower().strip() == pair[1].lower().strip():
			the_row = i + 1
			i = length + 10
		i += 1

	#Return this if go through whole sheet and no pair found
	if i == length:
		return 'Pair Does Not Exist'

	#clear the_row in Current-Pairings (should work 
	#because add_pair just finds first empty row)
	cp.update_cell(the_row, 1, '')
	cp.update_cell(the_row, 2, '')
	cp.update_cell(the_row, 3, '')

def update_all_pair(pair, notes):
	#update the All-Pairings sheet with end date and notes
	ap = open_sheet('All-Pairings')

	one = ap.col_values(1)
	two = ap.col_values(2)
	length = len(one)
	i = 0
	while i < length:
		if one[i].lower().strip() == pair[0] and two[i].lower().strip() == pair[1]:
			the_row = i + 1
			i = length + 10
		i += 1

	#Return this if go through whole sheet and no pair found
	if i == length:
		return 'Pair Does Not Exist'


	#assume current date is end date
	the_time = time.strftime("%m-%d-%y", time.gmtime())
	ap.update_cell(the_row, 4, the_time)
	ap.update_cell(the_row, 5, notes)




