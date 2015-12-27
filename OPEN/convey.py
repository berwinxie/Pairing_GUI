import os
import time
import authenticate as au

#this is for testing atm
def list_available_sheets(gc)
	all_sheets = []
	for sheet in gc.openall():
		all_sheets.append("{}".format(sheet.title))
	return all_sheets

#given a spreadsheet name, opens the spreadsheet
#and returns a sheet that you can manipulate.
def open_sheet(spreadsheet):
	#change into key usage later
	#key = turn_to_key(spreadsheet)

	#turn this into url to some cloud so dont have to
	#show the file on github.
	path2secretfile = 'first-eb1baeb00baf.json'
	
	#load authentication with .json file
	#like the file once you open a txt file
	gc = au.LOAD(path2secretfile)
		
	#assume the sheet exists
	sheet = gc.open(spreadsheet).sheet1

	'''
	#list all workbooks you can edit and make sure
	#the user is opening one that they can.
	here = list_available_sheets(gc)
	if spreadsheet in here:
		#sheet = gc.open_by_key(key).sheet1
		sheet = gc.open(spreadsheet).sheet1
	else:
	#if spreadsheet isnt available tell user and give them a
	#list of all the ones that the user can edit.
		return "Spreadsheet is not available.", here
	'''
	return sheet


#only kinda stolen from Analyze_Docs
def list_names(sheet_name):
	#this function takes a document and creates an array
	#of all the lines in the document in order.	
	#and lower case
	path = path = os.getcwd() + "/spreadsheets/"
	sheet = open(path + sheet_name + ".txt", 'r')
	list_of_lines = sheet.readlines()

	sheet.close()
	return list_of_lines

#given the sheet_name takes that and turns each individual line
#into an array
#this is really just changing list lines into this function....
def queues_as_arrays(queue):
	array = list_lines(queue)
	new_array = []
	for element in array:
		new_array.append(element.lower())
	#array1 = remove_newlines(array)
	return new_array

#given a sheet name and list of names this function
#writes those names to the sheet
#writelines method REQUIRES \n in there for new lines, make sure to have it!!
def rewrite_sheet(sheet_name, new_list_of_names):
	
	path = os.getcwd() + "/spreadsheets/"
	sheet = open(path + sheet_name + ".txt", 'w')
	sheet.writelines(new_list_of_names)
	sheet.close()

def add_pair(chosen_pair):
	#given a pair, friend, warrior this will add the pair to the
	#current pairings sheet and the all pairings sheet
	#along with a time stamp and in the future a tag showing who
	#paired them.	
	for element in ["Current-Pairings", "All-Pairings"]:
		pairs = queues_as_arrays(element)
		the_time = time.strftime("%m-%d-%y", time.gmtime())
		pairs.append(chosen_pair[0] + ' ' + chosen_pair[1] + ' ' + the_time + '\n')
		rewrite_sheet(element, pairs)
		

def remove_from_queue(sheet_name, name, extra=1):
	#this removes a person from a queue
	#used after they have been paired so dont need to be paired anymore
	#remove only one instance of name so that friends who place themselves
	#on the q multiple times to be paired multiple times dont have all of
	#their names they put on removed
	list_of_names = queues_as_arrays(sheet_name)
	new_names = []
	i = 0
	#extra represents how many instances of the name to remove
	for element in list_of_names:
		if element == name and i < extra:
			i = i + 1
		else:
			new_names.append(element)
	rewrite_sheet(sheet_name, new_names)


#used to add friends who want to be added to queue, maybe also to create
#warrior queue from
#array of names without \n at the end already
def add_to_queue(sheet_name, list_of_names):
	names = queues_as_arrays(sheet_name)
	for name in list_of_names:
		names.append(name + '\n')
	rewrite_sheet(sheet_name, names)
		



