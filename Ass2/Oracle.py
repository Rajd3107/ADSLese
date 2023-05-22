from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
import tkinter
import tkinter.messagebox
import cx_Oracle


# url = "2020BTECS00027/2020BTECS00027@10.10.16.15:1521/pdborcl"
# conn = cx_Oracle.connect(user="2020BTECS00027", password="2020BTECS00027",
#                                dsn="10.10.16.15:1521/pdborcl")
dsn = cx_Oracle.makedsn("10.10.16.15", 1521, service_name="pdborcl")
conn = cx_Oracle.connect(user="2020BTECS00027", password="2020BTECS00027",
                               dsn=dsn,
                               encoding="UTF-8")
c = conn.cursor()

# Initializing Window
window = Tk()
window.title("Oracle Database Connectivity")  # Title of window
window.geometry('850x850')  # Size of window (width X height)
window.configure(background="#EEEEEE")  # Background color of window
window.option_add("*Font", "Times 16")  # Setting the font-family & font-size
usr_name = Label(window, text=f"Connected to DB as: TY2020BTECS00027",
                 background="yellow").grid(row=0, column=1, pady=20)

# Getting the table names
c.execute('select table_name from user_tables')
DB_NAMES = [a[0] for a in c]
variable = StringVar(window)
variable.set(DB_NAMES[0])  # default value
selected_tb = DB_NAMES[0]
tb_select = Label(window, text="Choose the table: ",
                  background="white").grid(row=1, column=0, columnspan=1, padx=10, pady=10)
tb_dropdown = OptionMenu(
    window, variable, *DB_NAMES).grid(row=1, column=0, columnspan=2, padx=15)


def confirm_tb():
    global selected_tb
    tkinter.messagebox.showinfo(
        "SUCCESS", f" Table {variable.get()} is selected!")


tb_btn = Button(window, text="Confirm", command=confirm_tb,
                background="grey", foreground="white", border=5).grid(row=1, column=1)
                
# CRUD Functions
# 1. View


def view_tb():
    newWindow = Toplevel(window)
    newWindow.title("VIEW Table")
    newWindow.geometry('800x800')
    newWindow.configure(background="grey")  # Background color of window
    # Setting the font-family & font-size
    newWindow.option_add("*Font", "Arial 16")
    global selected_tb
    Label(newWindow, font=('Arial bold', 15), text=f"Viewing Table - {selected_tb}",
          background="orange").grid(row=0, column=0, padx=10, pady=10)
    # Getting the primary key
    c.execute(f'''select a.column_name
    from all_cons_columns a
    inner join all_constraints c
    on a.constraint_name=c.constraint_name
    where c.table_name='{selected_tb}' and 
    c.constraint_type='P'
    ''')
    for a in c:
        pk = a[0]
    # Getting all column names from table
    c.execute(f'''SELECT column_name
    FROM USER_TAB_COLUMNS
    WHERE table_name = '{selected_tb}'
    ''')
    columns = [a[0] for a in c]
    tree = ttk.Treeview(newWindow, height=20, columns=columns, show='headings')
    tree.grid(row=1, column=0, sticky='news', padx=10, pady=10)

    # setup columns attributes
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor=tkinter.CENTER)
    # populate data to treeview
    c.execute(f'SELECT * FROM {selected_tb} ORDER BY {pk}')
    for a in c:
        tree.insert('', 'end', value=a)
    # scrollbar
    sb = tkinter.Scrollbar(
        newWindow, orient=tkinter.VERTICAL, command=tree.yview)
    sb.grid(row=1, column=1, sticky='ns', padx=0, pady=10)
    tree.config(yscrollcommand=sb.set)
    sbx = tkinter.Scrollbar(
        newWindow, orient=tkinter.HORIZONTAL, command=tree.xview)
    sbx.grid(row=2, column=0, sticky='ew', padx=10, pady=0)
    tree.config(xscrollcommand=sbx.set)
# 2. Insert


def insert_tb():
    newWindow = Toplevel(window)
    newWindow.title("INSERT into Table")
    newWindow.geometry('900x900')
    newWindow.configure(background="Grey")  # Background color of window
    # Setting the font-family & font-size
    newWindow.option_add("*Font", "Times 16")
    global selected_tb
    Label(newWindow, font=('Arial bold', 15), text=f"Insert values in table: {selected_tb}", background="white").grid(
        row=0, column=0, padx=10, pady=10)
    c.execute(f'''SELECT column_name
    FROM USER_TAB_COLUMNS
    WHERE table_name = '{selected_tb}'
    ''')
    # Getting columns names
    columns = [a[0] for a in c]
    ent_ref = []  # For storing the Entry references
    # Populating Labels and Entries
    for ind, nm in enumerate(columns):
        Label(newWindow, font=('Arial bold', 15), text=nm, background="white").grid(row=ind+1,
                                                                                    column=0, padx=10, pady=10)
        ent = Entry(newWindow)
        ent.grid(row=ind+1, column=1)
        ent_ref.append(ent)

    def insert_val():
        val = []
        is_empty = False
    # Getting value from each entry field
        for r in ent_ref:
            if len(r.get()) > 0:
                val.append(r.get())
            else:
                tkinter.messagebox.showerror(
                    "ERROR", "All the fields are required!")
                is_empty = True
                break
    # Checking if all fields are filled, before inserting
        if not is_empty:
            v = []
    # Typecasting values (int, float & string)
            for x in val:
                try:
                    v.append(int(x))
                except ValueError:

                    try:
                        v.append(float(x))
                    except ValueError:
                        v.append(x)
    # Inserting values
            s = f'insert into {selected_tb}('+','.join(
                ['?']*len(v))+')' + ' values('+','.join([':?']*len(v))+')'
            for a in columns:
                s = s.replace('?', a, 1)
            for a in columns:
                s = s.replace('?', a, 1)
        try:
            c.execute(s, v)
            conn.commit()
            for r in ent_ref:
                r.delete(0, END)
                tkinter.messagebox.showinfo(
                    "SUCCESS", "Values inserted into table successfully!")
        except Exception as e:
            tkinter.messagebox.showerror("ERROR", e)

    Button(newWindow, text="Insert Values", command=insert_val,
           background="green", foreground="white").grid(row=ind+2, column=1, pady=20,
                                                        sticky='ew')
# 3. Update


def update_tb():
    global selected_tb
    try:
        c.execute(f'''select a.column_name
        from all_cons_columns a
        inner join all_constraints c
        on a.constraint_name=c.constraint_name
        where c.table_name='{selected_tb}' and 
        c.constraint_type='P'
        ''')
        for a in c:
            pk = a[0]
        id = simpledialog.askinteger(
            title="UPDATE", prompt="Enter the ID to be updated: ")
        if id is not None:
            c.execute(f'select * from {selected_tb} where {pk}={id}')
        if len(c.fetchall()) == 0:
            tkinter.messagebox.showerror(
                "ERROR", "No record was found with the given ID !")
        else:
            newWindow = Toplevel(window)
            newWindow.title("UPDATE Table")
            newWindow.geometry('900x900')
            # Background color of window
            newWindow.configure(background="grey")
            # Setting the fontfamily & font-size
            newWindow.option_add("*Font", "Times 16")
            Label(newWindow, text="Update values in table:",
                  background="orange").grid(row=0, column=0, padx=10, pady=10)
            c.execute(f'''SELECT column_name
            FROM USER_TAB_COLUMNS
            WHERE table_name = '{selected_tb}'
            ''')
            columns = [a[0] for a in c]
            ent_ref = []
            c.execute(f'select * from {selected_tb} where {pk}={id}')
            val = []
            for a in c:
                val.append(a)
            val = [str(item) for t in val for item in t]
            for ind, nm in enumerate(columns):
                Label(newWindow, text=nm, background="orange").grid(
                    row=ind+1, column=0, padx=10, pady=10)
                ent = Entry(newWindow)
                ent.grid(row=ind+1, column=1)
                ent.insert(0, val[ind])
                ent_ref.append(ent)

            def update_val():
                upd_val = []
                is_empty = False
                for r in ent_ref:
                    if len(r.get()) > 0:
                        upd_val.append(r.get())
                    else:
                        tkinter.messagebox.showerror(
                            "ERROR", "All the fields are required!")
                        is_empty = True
                        break
                if not is_empty:
                    v = []
                    for x in upd_val:
                        try:
                            v.append(int(x))
                        except ValueError:
                            try:
                                v.append(float(x))
                            except ValueError:
                                v.append(x)
                    s = f'update {selected_tb} set ' + \
                        ','.join(['? = :?']*len(v))+f' where {pk}={id}'
                    for a in columns:
                        s = s.replace('?', a, 2)
                    try:
                        c.execute(s, v)
                        conn.commit()
                        newWindow.destroy()
                        tkinter.messagebox.showinfo(
                            "SUCCESS", "Values updated successfully!")
                    except Exception as e:
                        tkinter.messagebox.showerror("ERROR", e)
        Button(newWindow, font=('Arial bold', 15), text="Update Values", command=update_val,
               background="blue", foreground="white").grid(row=ind+2, column=1, pady=20,
                                                           sticky='ew')
    except Exception as e:
        tkinter.messagebox.showerror("ERROR", e)
# 4. Delete


def delete_tb():
    global selected_tb
    try:
        c.execute(f'''select a.column_name
        from all_cons_columns a
        inner join all_constraints c
        on a.constraint_name=c.constraint_name
        where c.table_name='{selected_tb}' and 
        c.constraint_type='P'
        ''')
        for a in c:
            pk = a[0]
        id = simpledialog.askinteger(
            title="DELETE", prompt="Enter the ID to be deleted: ")
        if id is not None:
            c.execute(f'delete from {selected_tb} where {pk}={id}')
            if c.rowcount == 0:
                tkinter.messagebox.showerror(
                    "ERROR", "Cannot DELETE!\nNo record was found with the given ID !")
        else:
            conn.commit()
            tkinter.messagebox.showinfo(
                "SUCCESS", "Deleted record from table successfully!")
    except Exception as e:
        tkinter.messagebox.showerror("ERROR", e)


# CRUD operation buttons
if selected_tb is not None:
    Label(window, text="Select the Operation: ", background="orange",
          font='Helvetica 18 bold').grid(row=3, column=0, padx=10, pady=60)
    view_btn = Button(window, text="View", command=view_tb,
                      background="#9629ff", foreground="white", border=3).grid(row=4, column=0)
    insert_btn = Button(window, text="Insert", command=insert_tb,
                        background="green", foreground="white", border=3).grid(row=4, column=1,
                                                                               sticky='w', columnspan=1)
    update_btn = Button(window, text="Update", command=update_tb,
                        background="blue", foreground="white", border=3).grid(row=4, column=1,
                                                                              columnspan=2)
    delete_btn = Button(window, text="Delete", command=delete_tb,
                        background="red", foreground="white", border=3).grid(row=4, column=2)
window.mainloop()  # window remains until user closes it
conn.close()
