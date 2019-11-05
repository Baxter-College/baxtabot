import re
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

    mealsByDay = [[[]] for i in range(7)]
    mealTitles = [
        ["breakfast", "brekfast", "brekkie", "beakfast"],
        ["lunch", "luch", "launch", "lunc"],
        ["dinner", "dinenr", "dins", "supper"]
    ]

def spanned_on(rowspans, row, col):
    if str(row) in rowSpans and col in rowSpans[str(row)]:
        rowSpans[str(row)].remove(col)
        return True
    return False
def update_spans(rowspans, span, row, col):
    for i in range(1, span):
        later_row = span + i
        if later_row in rowSpans:
            rowSpans[later_row].append(col)
        else:
            rowSpans[later_row] = [col]
def next_meal(string, current_meal):
    if current_meal >= 3:
        return False
    return any([i in string for i in MEAL_TITLES[current_meal]])
def ignore_row(string):
    return any([i in string for i in IGNORED_ROWS])
def get_date(soup):
    pass
def guess_date():
    pass
def get_rows(soup):
    pass



def get_meals(soup):
    pass