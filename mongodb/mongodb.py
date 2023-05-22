from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
import tkinter, tkinter.messagebox
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import certifi


# Loading the data from .env file
load_dotenv()

ca=certifi.where()
# Getting the .env variables
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

# Connecting to DB
client = MongoClient(f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@adslab.cbsxhhr.mongodb.net/test",server_api=ServerApi('1'),tlsCAFile=ca)
db = client[MONGO_DB_NAME] # Select DB
collection = db[MONGO_COLLECTION] # Select collection

# Initializing Window
window = Tk()
window.title("CassandraDB Database Connectivity") # Title of window
window.geometry('900x900') # Size of window (width X height)
window.configure(background = "#7853b7"); # Background color of window
window.option_add("*Font", "Times 16") # Setting the font-family & font-size 

usr_name = Label(window ,text = f"Connected to Cassandra as: Raj Dalvi", background = "white").grid(row = 0, column = 1, pady=20)

# CRUD Functions
# 1. View
def view_tb():
    newWindow = Toplevel(window)
    newWindow.title("VIEW Table")
    newWindow.geometry('1500x900')
    newWindow.configure(background = "#72a64b"); # Background color of window
    newWindow.option_add("*Font", "Times 16") # Setting the font-family & font-size
    
    Label(newWindow ,text = f"Viewing Collection - Assignment09", background = "white").grid(row = 0, column = 0, padx=10, pady=10)

    # Getting all column names from table
    coll_keys = collection.find_one()
    columns = [a for a in coll_keys]
    tree = ttk.Treeview(newWindow, height=20, columns=columns, show='headings')
    tree.grid(row=1, column=0, sticky='news', padx=10, pady=10)

    # setup columns attributes
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor=tkinter.CENTER)

    # populate data to treeview
    all_data = collection.find({})
    data_list = []
    for a in all_data:
        data_list.append(tuple(a.values()))
    for d in data_list:
        tree.insert('', 'end', value=d)

    # scrollbar
    sb = tkinter.Scrollbar(newWindow, orient=tkinter.VERTICAL, command=tree.yview)
    sb.grid(row=1, column=1, sticky='ns', padx=0, pady=10)
    tree.config(yscrollcommand=sb.set)

    sbx = tkinter.Scrollbar(newWindow, orient=tkinter.HORIZONTAL, command=tree.xview)
    sbx.grid(row=2, column=0, sticky='ew', padx=10, pady=0)
    tree.config(xscrollcommand=sbx.set)

# 2. Insert
def insert_tb():
    newWindow = Toplevel(window)
    newWindow.title("INSERT into Table")
    newWindow.geometry('900x900')
    newWindow.configure(background = "#4b81a6"); # Background color of window
    newWindow.option_add("*Font", "Times 16") # Setting the font-family & font-size
    
    Label(newWindow ,text = f"Insert values in collection: Assignment09", background = "white").grid(row = 0, column = 0, padx=10, pady=10)
    
    # Getting columns names
    coll_keys = collection.find_one()
    columns = [a for a in coll_keys]
    columns.pop(0) # Removing the _id field (entered automatically)
    
    ent_ref = [] # For storing the Entry references
    # Populating Labels and Entries
    for ind, nm in enumerate(columns):
        Label(newWindow ,text = nm, background = "white").grid(row = ind+1, column = 0, padx=10, pady=10)
        ent = Entry(newWindow)
        ent.grid(row = ind+1,column = 1)
        ent_ref.append(ent)

    def insert_val():
        val = []
        is_empty = False

        # Getting value from each entry field
        for r in ent_ref:
            if len(r.get()) > 0:
                val.append(r.get())
            else:
                tkinter.messagebox.showerror("ERROR", "All the fields are required!")
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

            doc_obj = dict(zip(columns, v))

            # Inserting values
            try:
                collection.insert_one(doc_obj)
                for r in ent_ref:
                    r.delete(0, END)
                tkinter.messagebox.showinfo("SUCCESS", "Values inserted into Collection successfully!")
            except Exception as e:
                tkinter.messagebox.showerror("ERROR", e)

    Button(newWindow, text="Insert Values", command=insert_val, background="green", foreground="white").grid(row = ind+2, column = 1, pady=20, sticky='ew')

# 3. Update
def update_tb():
    try:
        id = simpledialog.askinteger(title="UPDATE", prompt="Enter the id to be updated: ")

        if id is not None:
            query={"PRN":{"$eq":id}}
            present_data = collection.find_one(query)
            
            if present_data is None:
                tkinter.messagebox.showerror("ERROR", "No record was found with the given PRN !")
            else:
                newWindow = Toplevel(window)
                newWindow.title("UPDATE Table")
                newWindow.geometry('900x900')
                newWindow.configure(background = "white"); # Background color of window
                newWindow.option_add("*Font", "Times 16") # Setting the font-family & font-size
                
                Label(newWindow ,text = f"Update values in collection: Assignment09", background = "white").grid(row = 0, column = 0, padx=10, pady=10)

                coll_keys = collection.find_one()
                columns = [a for a in coll_keys]
                columns.pop(0) # Removing the _id field (entered automatically)

                ent_ref = []

                val = []
                for k, v in present_data.items():
                    val.append(str(v))

                val.pop(0) # Removing ObjectId

                for ind, nm in enumerate(columns):
                    Label(newWindow ,text = nm, background = "white").grid(row = ind+1, column = 0, padx=10, pady=10)
                    ent = Entry(newWindow)
                    ent.grid(row = ind+1,column = 1)
                    ent.insert(0, val[ind])
                    ent_ref.append(ent)

                def update_val():
                    upd_val = []
                    is_empty = False

                    for r in ent_ref:
                        if len(r.get()) > 0:
                            upd_val.append(r.get())
                        else:
                            tkinter.messagebox.showerror("ERROR", "All the fields are required!")
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
                        
                        try:
                            doc_obj = dict(zip(columns, v))
                            new_data = {"$set":doc_obj}
                            collection.update_one(present_data, new_data)
                            newWindow.destroy()
                            tkinter.messagebox.showinfo("SUCCESS", "Values updated successfully!")
                        except Exception as e:
                            tkinter.messagebox.showerror("ERROR", e)

                Button(newWindow, text="Update Values", command=update_val, background="blue", foreground="white").grid(row = ind+2, column = 1, pady=20, sticky='ew')

    except Exception as e:
        tkinter.messagebox.showerror("ERROR", e)

# 4. Delete
def delete_tb():
    try:
        id = simpledialog.askinteger(title="DELETE", prompt="Enter the PRN to be deleted: ")

        if id is not None:
            query={"PRN":{"$eq":id}}
            present_data = collection.find_one(query)
            
            if present_data is None:
                tkinter.messagebox.showerror("ERROR", "Cannot DELETE!\nNo record was found with the given PRN !")
            else:
                collection.delete_one(query)
                tkinter.messagebox.showinfo("SUCCESS", "Deleted record from Collection successfully!")

    except Exception as e:
        tkinter.messagebox.showerror("ERROR", e)

# CRUD operation buttons
Label(window ,text = "Operations on collection:", background = "white", font='Helvetica 18 bold').grid(row = 3, column = 0, padx=10, pady=60)

view_btn = Button(window, text="View", command=view_tb, background="#9629ff", foreground="white", border=3).grid(row = 4, column = 0)
insert_btn = Button(window, text="Insert", command=insert_tb, background="green", foreground="white", border=3).grid(row = 4, column = 1, sticky='w', columnspan=1)
update_btn = Button(window, text="Update", command=update_tb, background="blue", foreground="white", border=3).grid(row = 4, column = 1, columnspan=2)
delete_btn = Button(window, text="Delete", command=delete_tb, background="red", foreground="white", border=3).grid(row = 4, column = 2)

window.mainloop() # window remains until user closes it
client.close() # Closing the connection to database