import re
from dateutil.parser import parse
import datetime
MEAL_TITLES = [
    ["breakfast", "brekfast", "brekkie", "beakfast"],
    ["lunch", "luch", "launch", "lunc"],
    ["dinner", "dinenr", "dins", "supper"]
]
IGNORED_ROWS = ["special", "continental", "fruit"]

def text_replace(lines):
    lines = lines.lower()
    subs = {"&amp;": "&", "\\x96": "-", "\n|\r\n|\r|\xa0": "", "\\x92": "'",
            r"\bsalad\b" : "salad 🥗", r"\bburger\b" : "burger 🍔", 
            r"\bburgers\b" : "burgers 🍔", r"\begg\b" : "egg 🍳", r"\beggs" : "eggs 🍳",
            r"\bpizza\b" : "pizza 🍕", r"\bbacon\b" : "bacon 🥓", r"\bcake\b" : "cake 🍰",
            r"\bice-cream\b" : "ice-cream 🍨", r"\bicecream\b" : "icecream 🍨", r"\bice cream\b" : "ice cream 🍨",
            r"\bchicken\b" : "chicken 🍗", r"\bsandwich\b" : "sandwich 🥪"}

    for sub, repl in subs.items():
        lines = re.sub(sub, repl, lines)
    

def spanned_on(rowspans, row, col):
    if str(row) in rowspans and col in rowspans[str(row)]:
        rowspans[str(row)].remove(col)
        return True
    return False
def update_spans(rowspans, span, row, col):
    for i in range(1, span):
        later_row = span + i
        if later_row in rowspans:
            rowspans[later_row].append(col)
        else:
            rowspans[later_row] = [col]
def next_meal(string, current_meal):
    if current_meal >= 3:
        return False
    return any([i in string for i in MEAL_TITLES[current_meal]])
def ignore_row(string):
    return any([i in string for i in IGNORED_ROWS])
def get_date(first_row):
    date_cell = first_row.find('td')
    date_str = date_cell.get_text()
    return parse(date_str).date()
def guess_date():
    #finds the next monday
    today = datetime.date.today()
    days_to_monday = 0 - today.weekday()
    if days_to_monday < 0:
        days_to_monday += 7
    return today + datetime.timedelta(days=days_to_monday)

def extract_date(soup):
    sucess = True
    try:
        date = get_date(soup)
    except:
        sucess = False
        date = guess_date()
    return date, sucess
    
def get_rows(soup):
    tables = soup.find_all('table')
    all_rows = []
    for table in tables:
        rows = table.find_all('tr')
        all_rows += rows
    return all_rows



def get_meals(rows):
    mealsByDay = [[[]] for i in range(7)]
    rowspans = {}
    cur_meal = 0
    for rownum, row in enumerate(rows):
        cols = row.find_all('td')
        row_heading = ""
        prev_spans = 0
        for ind, col in enumerate(cols):
            while spanned_on(rowspans, rownum, ind + prev_spans):
                prev_spans += 1
            colnum = ind + prev_spans
            if col.has_key('rowspan'):
                span_size = int(col['rowspan'])
                update_spans(rowspans, span_size, rownum, colnum)

            string = col.get_text()
            if string == "":
                continue
            
            if colnum == 0:
                # first column of a row
                if ignore_row(string):
                    #break out of row loop
                    break
                if next_meal(string, cur_meal):
                    cur_meal += 1
                    for i in range(7):
                        mealsByDay[i].append([])
                    # test if this break is necessary
                    break
                row_heading = string.strip().capitalize()
            else:
                day = colnum - 1
                text = row_heading + ":\n" + string
                mealsByDay[day][cur_meal].append(text)
    return mealsByDay

                