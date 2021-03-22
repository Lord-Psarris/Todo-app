import sqlite3 as sql
from tkinter import *
from tkinter import ttk
import tkinter as tk

root = tk.Tk()
root.geometry('600x500')
root.resizable(False, False)
root.title('Todo app')

connection = sql.connect('todo')
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS 'todo' ('item' Text);")


def add():
    var = text_.get()
    if var:
        sql_command_ = f"INSERT INTO todo (item) VALUES('{var}');"
        cursor.execute(sql_command_)
        connection.commit()

        added_frame = Frame(scrollable_frame)

        added_ = Label(added_frame, text=var, relief=SOLID, wraplength=280, bd=1, anchor='w', padx=5,
                       justify=LEFT, width=40)
        added_.pack(side=LEFT)

        remove_ = Button(added_frame, text='Remove', command=lambda: remove(var))
        remove_.pack()

        added_frame.pack(fill=X, padx=50, pady=10)

    text_.delete(0, END)


def configure_(event):
    height = 0
    for child in container.grid_slaves():
        height += child.winfo_reqheight()

    canvas.itemconfigure(c_frame, width=event.width, height=height)


def get_all_children():
    global result, scrollable_frame

    children = scrollable_frame.winfo_toplevel().winfo_children()

    return _all_(children, result)


def _all_(children, result_):
    for child in children:
        result_.append(child)
        sub_children = child.winfo_children()
        if sub_children:
            _all_(sub_children, result_)

    return result_


def remove(var):
    global scrollable_frame
    widget_ = 'Label'
    selection = [child for child in get_all_children() if child.winfo_class() == widget_]
    for i in selection:
        print(i['text'])
        if i['text'] == var:
            widget_ = 'Frame'
            selection = [child for child in get_all_children() if child.winfo_class() == widget_]
            for j in selection:
                if i in j.winfo_children():
                    j.pack_forget()
                    sql_command_ = f"DELETE FROM todo WHERE item='{i['text']}';"
                    cursor.execute(sql_command_)
                    connection.commit()


def from_db():
    global cursor

    cursor.execute("SELECT * FROM todo;")
    items = cursor.fetchall()
    print(items)

    for i in items:
        i = i[0]
        added_frame = Frame(scrollable_frame)

        added_ = Label(added_frame, text=i, relief=SOLID, wraplength=280, bd=1, anchor='w', padx=5,
                       justify=LEFT, width=40)
        added_.pack(side=LEFT)

        remove_ = Button(added_frame, text='Remove', command=lambda: remove(i))
        remove_.pack()

        added_frame.pack(fill=X, padx=50, pady=10)


result = []

main_frame = Frame(root, relief=SOLID, height=180)

label_ = Label(main_frame, text='Add to the list', width=30, anchor='w').place(x=50, y=50)

text_ = Entry(main_frame, width=70)
text_.place(x=50, y=80, height=70)

add_ = Button(main_frame, text='Add todo', command=add)
add_.place(x=500, y=80)

main_frame.pack(fill=BOTH)

_frame = Frame(root, bg='green')

container = ttk.Frame(_frame)
canvas = Canvas(container, highlightthickness=0)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas)

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

c_frame = canvas.create_window((0, 0), window=scrollable_frame)

canvas.bind("<Configure>", configure_)

canvas.configure(yscrollcommand=scrollbar.set)

container.pack(fill="both", expand=True)
canvas.pack(side="left", fill="both", expand=1)
scrollbar.pack(side="right", fill="y", expand=0)

_frame.pack(fill=BOTH, expand=True)

from_db()
root.mainloop()

