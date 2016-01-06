import web
import convey as cv
import json

urls = (
	'/pairing_gui', 'Pairing',
	'/add', 'Add',
	'/remove', 'Remove', 
	'/warriorinfo', 'WarriorInfo',
	'/friendinfo', 'FriendInfo',
	'/add'        , 'Add',
	'/remove'     , 'Remove'
)

app = web.application(urls, globals())
render = web.template.render('templates/')

class Pairing(object):
	def GET(self):
	#once /Pairing webpage is loaded the GET method
	#renders the pairing gui.html from the templates folder

		#list names in the Friend and Warrior qs
		#both are formatted so names are in column 1
		friendq  = cv.names_no_null("Friend-Q", 1)
		warriorq = cv.names_no_null("Warrior-Q", 1)
		
		total = [friendq, warriorq]
		
		return render.pairing_gui(list_of_names = total)
#the rendered pairing gui contains a form on it, which
#once submitted calls on the POST method below	
	

	#the pairing gui in templates will call upon this method to
	#record information submitted to the website
	def POST(self):
#once this method is called upon it takes the pairs and 
#removes them from the current queue, adding them to the
#current pairings list. THIS IS WHERE THE MAGIC HAPPENS.		
		form = web.input(friend = 'friend', warrior = 'warrior')
	#let this if statement verify that the user submitted
	#everything correctly. that means ADD MORE HERE
	#ik what ur thinking, wheres the more? wheres
	#the if statements? well, now its dropdown, so user
	#would need to be rly dumb, i guess there could be
	#check that chosen is what they want... an r u sure button
		
		chosen_pair = [form.warrior, form.friend]
		
		#these three functions just updates sheets removing both 
		#from the queues and adding them to both pairing sheets
		cv.add_pair(chosen_pair)
		
		#this runs default and only removes their names once
		cv.remove_from_queue("Friend-Q", form.friend)
		cv.remove_from_queue("Warrior-Q", form.warrior)

		friendContact = cv.get_friend_info(form.friend, 'contact')
		warriorContact = cv.get_warrior_info(form.warrior, 'contact')

		#redownload queues to display updated versions.
		friendq  = cv.names_no_null("Friend-Q", 1)
		warriorq = cv.names_no_null("Warrior-Q", 1)
		this = [chosen_pair, friendq, warriorq, friendContact, warriorContact]
	

#this renders display.html. It shows the new queues and the
#pair of people you added to both pairings lists
		return render.display(this)
		
		"""all_lists should be of the form
		[chosen_pair, friendQ, warriorq]
		where chosen_pair = [chosen_friend, chosen_warrior]
		"""

class Add(object):
	#this is the code for the buttons for friends to add 
	#themselves to the queue
	def GET(self):
		return render.add(stuff = 3)
		

	#THIS whole thing needs to be rewritten to check if 
	#a friend is verified and if they are then add them to the list
	#if not then display a correct error message of them either
	#not being verified or not being on the list
	#
	def POST(self):	
		#im assuming this means the default setting is 1
		form = web.input(netid = "netid", number = 1)
		#dont need to format name here because search does it for us
		
		#make a default setting of nothing being because if adding is not
		#a success then the html doesnt need the new list anyways.
		new_list =[]
		i =1
		#this is the number of times their name will be added to the list
		#it is the number of warriors they are able to help. (battle can be ruf)
		num = int(form.number)
		
		#check that they are on friend list AND verified
		
		sheet = cv.open_sheet('Friend-List')
		#find columns of all these things
		name_col  = cv.search_row(sheet, 1, 'name')
		netid_col = cv.search_row(sheet, 1, 'netid')
		veri_col  = cv.search_row(sheet, 1, 'verified')

		#find the row the netid they give is in and use this row to
		#and other columns we found to find their other info
		#case and extra spaces do not matter for this function
		row_num = cv.search_column(sheet, netid_col, form.netid)

		#this error becomes a problem if we have more than 1000
		#people sign up OR if we randomly get a spreadsheet that is
		#automatically sized to 100 rows. (default was said to be 100
		#or 1000 but ive only seen 1000 so far.)
		if row_num >= 1000:
			message = "FAILURE! We could not find your netID on the list. Please make sure you submitted the correct netID (%s). If this is the correct netID it is possible that was incorrectly entered on our spreadsheet or there is something wrong with this code (which is a very likely possibility). Please let us know about this problem, whether through our website, facebook, slack, next meeting, or randomly in the quad. THANK YOU!" % form.netid	

		else:
			#see all values in the users row
			the_values = sheet.row_values(row_num)
			
			#find the name of the person with that netID
			#and whether or not they are verified
			#sheets columns is one ahead of arrary
			name = the_values[name_col - 1]
			verified = the_values[veri_col - 1]
	
			#check that a friend is verified and if they are add them 
			#to the queue 'num' times.
			#because array starts at 0 and gsheets starts at 1
			if verified.lower().strip() == 'yes':
				name_count = []
				while i <= num:
				#remember, names must be submitted as arrays.
					name_count.append(name)
					i = i + 1
			
				cv.add_to_queue("Friend-Q", name_count)				
				message = "SUCCESS!"			
				
				#new list is only rendered if there is sucess so
				#user can make sure their name is on it.
				#actually, you should probably remove this when done testing
				new_list = cv.names_no_null("Friend-Q", 1)
			else:
				message = "FAILURE! You're name is on the list but it looks like you have not been verified. In order to become verified you must come to a sufficient amount of trainings. At the trainings we go over situations you may encounter and talk about what the process of being a friend will be like (good ole logistics and all.) It is really quite fun. Once there was even candy. So please try to come out if you have not yet. If anything you'll at least learn how this stupid interface works. If you believe you have been verified though and have gone through trainings then please let somebody know so they can fix it. Again, its a stupid interface. But with your help maybe it can just be dumb."

		#message, times added to queue, and new list of names on queue
		return render.add(stuff = [message, i-1, new_list])


class Remove(object):
	#this is the code for the buttons for friends to 
	#remove themselves from the queue
	def GET(self):
		#this is three to display the part of if statement i want
		#maybe calling a different .html woulda been better. maybe
		return render.remove(friendq = 3)
		
	#This requires a rewrite of the function remove_from_queue()
	#so that it allows a more lenient input
	def POST(self):
		form = web.input(netid = "netid")

		#this is done in a similar way to the Add POST method
		#using their netID find the associated name and remove that
		#from the queue
		sheet = cv.open_sheet('Friend-List')
		name_col  = cv.search_row(sheet, 1, 'name')
		netid_col = cv.search_row(sheet, 1, 'netid')
		row_num = cv.search_column(sheet, netid_col, form.netid)

		#use col and row info to find the name
		#dont need to format because remove function will do that
		name_values = sheet.col_values(name_col)
		name = name_values[row_num - 1]
		print name_values, name, row_num
		cv.remove_from_queue("Friend-Q", name, 'rm all')
		new_list = cv.names_no_null("Friend-Q", 1)
		return render.remove(friendq = new_list)


class WarriorInfo(object):
	def POST(self):
		warriorName = web.input()
		textName = warriorName['name']
		info = cv.get_warrior_info(textName, 'info')
		return json.dumps({'sex': info[0], 'year': info[1], 'interests': info[2], 'hobbies': info[3], 'struggle':info[4]})

class FriendInfo(object):
	def POST(self):
		warriorName = web.input()
		textName = warriorName['name']
		info = cv.get_friend_info(textName, 'info')
		return json.dumps({'sex': info[0], 'year': info[1], 'major':info[2], 'interests':info[3], 'hobbies':info[4]})

if __name__ == '__main__':
	app.run()
