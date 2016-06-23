import sqlite3
from Tkinter import *
import ttk
import re
import string

#
# load sqlite db into dictionary
# keys = terms; values hold tuples with indices:
#   0 = chapter_index, 1 = order_in_chapter, 2 = gloss
#

con = sqlite3.connect('GlossThinkPython-db.sqlite')
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute('SELECT * FROM Glosses')

def sql_to_dict(cursor, target_dict):
    for row in cursor:
        if len(row) == 0:
            break
        target_dict[row[0]] = row[1], row[2], row[3]

glosses_dict = dict()
sql_to_dict(cur, glosses_dict)

#
# functions to generate text content of Tkinter widgets
#

# wrap text for results, terms, and glosses, called from functions
# keypress_results and show_glosses

def wrap_text(unwrapped_text, line_max_length, wrappable_spacer):
    wrapped_text = ''
    while True:
        unwrapped_text = string.lstrip(unwrapped_text)
        if len(unwrapped_text) <= line_max_length:
            wrapped_text += unwrapped_text
            return wrapped_text
        else:
            line_break_index = unwrapped_text.rfind(wrappable_spacer, 0, line_max_length)
            wrapped_text += unwrapped_text[:line_break_index] + '\n'
            unwrapped_text = unwrapped_text[line_break_index + 1:]

# sort results by chapter_index and order_in_chapter, then pass sorted list
# to function show_glosses
# sort_by_chapter called from functions all_terms_chapter and keypress_results

def sort_by_chapter(list_in):
    sorting_list = []
    for item in list_in:
        sorting_list.append([glosses_dict[item][0], glosses_dict[item][1], item])
    sorting_list.sort()
    sorted_list = []
    for item in sorting_list:
        sorted_list.append(item[2])
    show_glosses(sorted_list)

# generate list of all terms in chapter, then pass list to function sort_by_chapter

def all_terms_chapter(chapter_title):
    chapter_list = []
    space = chapter_title.rfind(' ')
    chapter_number = chapter_title[(space + 1):]
    if chapter_number == 'B':
        chapter_index = 20
    else:
        chapter_index = int(chapter_number) - 1
    for item in glosses_dict:
        if glosses_dict[item][0] == chapter_index:
            chapter_list.append(item)
    sort_by_chapter(chapter_list)

# generate list of all terms by letter, then pass list to function show_glosses

def all_terms_alpha(letter):
    alpha_list = []
    for item in glosses_dict:
        if item[0] == letter:
            alpha_list.append(item)
    alpha_list.sort()
    show_glosses(alpha_list)

# populate glosses frame with terms and glosses, called from
# functions sort_by_chapter, all_terms_chapter, and all_terms_alpha

def show_glosses(list):
    for widget in glosses_window.winfo_children():
        widget.destroy()
    row_num = 0
    chapter_text = str()

    for item in list:
        wrapped_item = wrap_text(item, 20, ' ')
        term = ttk.Label(glosses_window, text=wrapped_item)
        term.grid(column=0, row=row_num, sticky=(W, N))
        wrapped_gloss = wrap_text(glosses_dict[item][2], 60, ' ')
        gloss = ttk.Label(glosses_window, text=wrapped_gloss)
        gloss.grid(column=1, row=row_num, sticky=(W))
        row_num += 1
        if glosses_dict[item][0] == 20:
            chapter_text = 'Appendix B'
        else:
            chapter_text = 'Chapter %d' % (glosses_dict[item][0] + 1)
        chapter = ttk.Label(glosses_window, text=chapter_text)
        chapter.grid(column=1, row=row_num, sticky=(E))
        row_num += 1
        empty_row = ttk.Label(glosses_window, text=' ')
        empty_row.grid(column=0, columnspan=2, row=row_num)
        for child in glosses_window.winfo_children():
            child.grid(padx=3, pady=3)
        row_num += 1

    if len(list) == 0:
        term = ttk.Label(glosses_window, text='...')
        term.grid(column=0, row=row_num, sticky=(W, N))

    glosses_window.update_idletasks()
    glosses_canvas.config(scrollregion=glosses_canvas.bbox(ALL))
    glosses_window.grid_columnconfigure(0, minsize=175)
    glosses_window.grid_columnconfigure(1, minsize=425)

# display search results in results pane, <Return> calls function show_glosses

def keypress_results(KeyPress):

    # reset everything for each keypress

    results_list = list()
    results_string = ''
    match = False
    entry = search_text.get()
    entry_reg = '.*' + entry + '.*'

    # look for matching terms for search strings of more than 2 characters

    if len(entry) == 0:
        results_list = []
        results_string = ''
    elif len(entry) == 1:
        results_list = []
        results_string = '...'
    elif len(entry) > 1:
        for key in glosses_dict:
            if re.search(entry_reg, key, re.IGNORECASE):
                match = True
                results_list.append(key)
                results_list.sort()

                # recreate results_string with new results_list,
                # insert line breaks with function wrap_text

                results_spacer = '      '
                results_list_stringified = results_spacer.join(results_list)
                results_string = wrap_text(results_list_stringified, 100, results_spacer)

    # if there are no matching terms

    if len(entry) > 1 and match == False:
        results_list = []
        results_string = '...'

    # <Return> clears results_string and passes results_list to
    # show_glosses function

    if KeyPress.keysym_num == 65293:
        results_string = ''
        search_text.set('')
        sort_by_chapter(results_list)

    # after all is said and done, display results_string

    results_text.set(results_string)
    results_window.update_idletasks()
    results_canvas.config(scrollregion=results_canvas.bbox(ALL))

#
# functions to configure Tkinter widgets
#

def config_col_row_std(name):
    name.grid_columnconfigure(0, weight=1)
    name.grid_rowconfigure(0, weight=1)

def config_labelframe(name, column_pos, row_pos):
    col_dims = [150, 700]
    row_dims = [100, 400]
    name.configure(width=col_dims[column_pos], height=row_dims[row_pos])
    name.grid(column=column_pos, row=row_pos)
    config_col_row_std(name)
    name.grid(padx=Tk_global_opts('pad'), pady=Tk_global_opts('pad'), sticky=(W, N, E, S))
    name.grid_propagate(0)

def config_canvas(name):
    name.config(borderwidth=0, highlightthickness=0, background=Tk_global_opts('bg_col'))
    name.grid(column=0, row=0, sticky=(N,W,E,S))
    config_col_row_std(name)

def config_canvas_scroll_window(canvas, scrollbar, window):
    canvas.config(borderwidth=0, highlightthickness=0, background=Tk_global_opts('bg_col'))
    canvas.grid(column=0, row=0, sticky=(N,W,E,S))
    config_col_row_std(canvas)

    canvas.config(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=canvas.yview)
    scrollbar.grid(column=1, row=0, sticky=(N,S))

    canvas.create_window((0,0), window=window, anchor="nw")
    config_col_row_std(window)

def list_buttons(list, parent, button_lambda):
    button = {}
    row_num = 0
    for item in list:
        button[item] = ttk.Button(parent, text=item)
        button[item].configure(command= lambda item=item: button_lambda(item))
        button[item].grid(column=0, row=row_num, sticky=(W, N, E, S))
        parent.grid_rowconfigure(row_num, weight=1)
        row_num += 1

def Tk_global_opts(opt):
    options = {
        'pad': 5,
        'bg_col': 'gray'
    }
    return options[opt]

#
# Tkinter root and widgets
#

#
# hierarchical map of Tkinter grids:
#    root
#       search_frame
#       results_frame
#          results_canvas
#             results_window
#       lists_frame
#          lists_notebook
#             alpha_tab
#                alpha_canvas
#                   alpha_window
#             chapter_tab
#                chapter_canvas
#                   chapter_window
#       glosses_frame
#          glosses_canvas
#             glosses_window
#

root = Tk()
root.title('Gloss Think Python')

for i in range(0, 2):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

root.configure(padx=Tk_global_opts('pad'), pady=Tk_global_opts('pad'), background=Tk_global_opts('bg_col'))

#
# ttk styling
#

style = ttk.Style()
style.theme_use('alt')

style.configure('.', background=Tk_global_opts('bg_col'))
style.configure('TLabelframe', padding=5)

#
# Tkinter control variables
#

search_text = StringVar()
results_text = StringVar()

#
# search frame
#

search_frame = ttk.LabelFrame(root, labelanchor='nw', text='Search')
config_labelframe(search_frame, 0, 0)

search_entry = ttk.Entry(search_frame, width=20, textvariable=search_text)
search_entry.grid(column=0, row=0)

#
# results frame
#

results_frame = ttk.LabelFrame(root, labelanchor='nw', text='Results')
config_labelframe(results_frame, 1, 0)

results_canvas = Canvas(results_frame)
results_scrollbar = ttk.Scrollbar(results_frame, orient=VERTICAL)
results_window = ttk.Label(results_canvas)
config_canvas_scroll_window(results_canvas, results_scrollbar, results_window)

results_window.configure(textvariable=results_text)

#
# lists frame
#

lists_frame = ttk.LabelFrame(root, labelanchor='nw', text='Lists')
config_labelframe(lists_frame, 0, 1)

lists_notebook = ttk.Notebook(lists_frame)
lists_notebook.grid(column=0, row=0, sticky=(W, N, E, S))
config_col_row_std(lists_notebook)

# alpha tab

alpha_tab = ttk.Frame(lists_notebook)
alpha_tab.grid(column=0, row=0)
config_col_row_std(alpha_tab)

alpha_canvas = Canvas(alpha_tab)
alpha_scrollbar = ttk.Scrollbar(alpha_tab, orient=VERTICAL)
alpha_window = ttk.Frame(alpha_canvas)
config_canvas_scroll_window(alpha_canvas, alpha_scrollbar, alpha_window)

# create alpha buttons

letters = string.ascii_lowercase
list_buttons(letters, alpha_window, all_terms_alpha)

alpha_window.update_idletasks()
alpha_canvas.config(scrollregion=alpha_canvas.bbox(ALL))

# chapters tab

chapter_tab = ttk.Frame(lists_notebook)
chapter_tab.grid(column=0, row=0)
config_col_row_std(chapter_tab)

chapter_canvas = Canvas(chapter_tab)
chapter_window = ttk.Frame(chapter_canvas)
chapter_scrollbar = ttk.Scrollbar(chapter_tab, orient=VERTICAL)
config_canvas_scroll_window(chapter_canvas, chapter_scrollbar, chapter_window)

# create chapter buttons

chapter_titles = []
for i in range(1, 22):
    if i != 21:
        chapter_titles.append('Ch %d' % i)
    else:
        chapter_titles.append('Appendix B')
list_buttons(chapter_titles, chapter_window, all_terms_chapter)

chapter_window.update_idletasks()
chapter_canvas.config(background=Tk_global_opts('bg_col'), scrollregion=chapter_canvas.bbox(ALL))

# add alpha and chapter tabs to lists notebook

lists_notebook.add(alpha_tab, text='Alpha')
lists_notebook.add(chapter_tab, text='Chapters')

#
# glosses frame
#

glosses_frame = ttk.LabelFrame(root, labelanchor='nw', text='Glosses')
config_labelframe(glosses_frame, 1, 1)

glosses_canvas = Canvas(glosses_frame)
glosses_scrollbar = ttk.Scrollbar(glosses_frame, orient=VERTICAL)
glosses_window = ttk.Frame(glosses_canvas)
config_canvas_scroll_window(glosses_canvas, glosses_scrollbar, glosses_window)

# events, event loop, focus on entry box

search_entry.focus()
root.bind('<KeyPress>', keypress_results)
root.mainloop()
