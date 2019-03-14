#dinoparser.py
#vers: 1.0
#program to parse the weekly dino menus, to automate the entry of the menu
#into 'BaxtaBot'
#Rohan Maloney
#12/3/2019

import re

#name of the html file to parse
fileName = "testdino.htm"

#read the entire file into one string
lines =  open(fileName, "r").read()

#replace some encoded characters with what they should be
#also remove all newline characters
subs = {"&amp;": "&", "\\x96":"-", "\n|\r\n|\r|\xa0":"", "\\x92":"'"}
for sub, repl in subs.items():
	lines = re.sub(sub, repl, lines)

#find every table element in the html file, read each of these strings into a list
#(also find every gap between the table elements)
#the gaps may also contain important elements so they are treated like tables

tables = []
cur = 0;

match = re.search(r"<table|$",lines[cur:])
tables.append(lines[cur:cur+match.start()]) 
#the first "table" or "row" contains all header and file info up to the first table
#this is not being used as of version 1.0 of dinoparser

#move the search index to the index of the start of the found table
cur += match.start()

test = []
while cur < len(lines):
	match = re.search(r"</table>",lines[cur:])
	if match == None:
		print("ERROR table not closed")
	tables.append(lines[cur:cur+match.end()])
	cur += match.end()

	match = re.search(r"<table",lines[cur:])
	if match == None:
		#there are no more tables, enter the remainder of the file as the last "table"
		match = re.search(r"$",lines[cur:])
	tables.append(lines[cur:cur+match.start()])
	cur += match.start()


rows = []
for table in tables:
	if table.startswith("<table"):
		#break all table elements down into rows
		row = re.findall(r"<tr.+?</tr>",table)
		rows+= row
		#all rows are added to rows independent of their table grouping, yet order is preserved
	else:
		rows.append(table)
		#gaps are added as a single row


elements = []
for row in rows:
	if row.startswith("<tr"):
		#rows are split into their individual row cells/elements
		elements.append(re.findall(r"<td.+?</td>",row))
	else:
		#gaps are added as a single-cell row
		elements.append([row])


paras = []
for row in elements:
	newrow = []
	for ele in row:
		ps = [i[1:-1].strip() for i in re.findall(r">[^<]+?<",ele)]
		#everything between a ">" and a "<" is assumed to be information visible to a viewer
		#hence it is stored
		texts = []
		for p in ps:
			if p != '' and p != '&nbsp;':
				#ignore all empty texts and space markers
				texts.append(p)

		# **** do not omit empty elements ([]) as this signify an empty table cell
		#		This means the cell inherits the value of a neighbouring cell
		#		Information is not used as of v 1.0, however if meals want to be separated into
		#		main/veg/salad etc this is needed
		newrow.append(texts)
	paras.append(newrow)

mealsByDay = [[[]] for i in range(7)]

#this stores all the sublabels for the meals (main, vegetarian, salad, desert)
#this info is not currently used v1.0
mealLabels = []

#stores the dates that the menu is for, relies on the fact that the dates are the 
#first element of the second 'row' (first table row_)
startDate = ' '.join(paras[1][0])

#stores the days of the week as listed along the top
days = paras[1][1:]

mealIndex = ['breakfast', 'lunch', 'dinner','brekfast','brekkie','launch','diner','dinenr','beakfast']
curMeal = 0;
mealKnown = False
mealValue = ''

for row in paras[2:]:
	if len(row) == 0 or len(row[0]) == 0:
		continue
	if row[0][0].lower() in mealIndex:
		for i in range(7):
			mealsByDay[i].append([])
		curMeal += 1;
		continue
	if (' '.join(row[0])).lower().startswith("special"):
		#last line often refers to special dietary requirements, no useful information after
		break
	mealLabel = ' '.join(row[0])
	mealLabels.append(mealLabel)
	if mealLabel.lower().startswith("continental"):
		#ignore the line explaining what a continental breakfast is
		continue
	if len(row) < 2:
		continue
	for day, ele in enumerate(row[1:]):
		#add each meal into a new list which orders the individual meals by their day and then
		#by which meal of the day
		mealsByDay[day][curMeal].append(' '.join(ele))
print ''
print("Menu for: " + startDate)
print ''


##below is purely for visual output of the parsed menu to test code 


days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
for num, day in enumerate(mealsByDay):
	print ''
	print("################   " + days[num] + "   #################")
	print ''
	for ind, meal in enumerate(day[1:]):
		print ">>>>>> " + mealIndex[ind] + " <<<<<<<"
		for thing in meal:
			if thing != '':
				print thing
		print ''
print ''
print ''
print("Menu for: " + startDate)
