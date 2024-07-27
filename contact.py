import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

conn = sqlite3.connect('contacts.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS contacts 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              name TEXT, 
              phone TEXT, 
              email TEXT, 
              address TEXT)''')
conn.commit()

def add_contact():
    name = simpledialog.askstring("Input", "Enter Contact Name:")
    if not name:
        messagebox.showwarning("Input Error", "Name cannot be empty.")
        return

    phone = simpledialog.askstring("Input", "Enter Phone Number:")
    email = simpledialog.askstring("Input", "Enter Email:")
    address = simpledialog.askstring("Input", "Enter Address:")

    c.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
              (name, phone, email, address))
    conn.commit()
    messagebox.showinfo("Success", "Contact added successfully!")
    view_contacts()

def view_contacts():
    contact_list.delete(0, tk.END)
    c.execute("SELECT name, phone FROM contacts")
    for row in c.fetchall():
        contact_list.insert(tk.END, f"{row[0]} - {row[1]}")

def search_contact():
    search_term = simpledialog.askstring("Search", "Enter name or phone number to search:")
    c.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?", 
              ('%' + search_term + '%', '%' + search_term + '%'))
    results = c.fetchall()
    if not results:
        messagebox.showinfo("Search Result", "No contacts found.")
    else:
        result_text = "\n".join([f"Name: {r[1]}, Phone: {r[2]}, Email: {r[3]}, Address: {r[4]}" for r in results])
        messagebox.showinfo("Search Result", result_text)

def update_contact():
    contact_id = simpledialog.askinteger("Update", "Enter contact ID to update:")
    if not contact_id:
        messagebox.showwarning("Input Error", "Contact ID is required.")
        return
    
    c.execute("SELECT * FROM contacts WHERE id=?", (contact_id,))
    result = c.fetchone()
    if not result:
        messagebox.showwarning("Update Error", "Contact not found.")
        return

    new_name = simpledialog.askstring("Input", f"Enter new name (current: {result[1]}):")
    new_phone = simpledialog.askstring("Input", f"Enter new phone (current: {result[2]}):")
    new_email = simpledialog.askstring("Input", f"Enter new email (current: {result[3]}):")
    new_address = simpledialog.askstring("Input", f"Enter new address (current: {result[4]}):")

    c.execute("UPDATE contacts SET name=?, phone=?, email=?, address=? WHERE id=?", 
              (new_name or result[1], new_phone or result[2], new_email or result[3], new_address or result[4], contact_id))
    conn.commit()
    messagebox.showinfo("Success", "Contact updated successfully!")
    view_contacts()

def delete_contact():
    contact_id = simpledialog.askinteger("Delete", "Enter contact ID to delete:")
    if not contact_id:
        messagebox.showwarning("Input Error", "Contact ID is required.")
        return
    
    c.execute("SELECT * FROM contacts WHERE id=?", (contact_id,))
    result = c.fetchone()
    if not result:
        messagebox.showwarning("Delete Error", "Contact not found.")
        return

    c.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()
    messagebox.showinfo("Success", "Contact deleted successfully!")
    view_contacts()

app = tk.Tk()
app.title("Contact Book")
app.geometry("400x300")

add_button = tk.Button(app, text="Add Contact", command=add_contact)
view_button = tk.Button(app, text="View Contacts", command=view_contacts)
search_button = tk.Button(app, text="Search Contact", command=search_contact)
update_button = tk.Button(app, text="Update Contact", command=update_contact)
delete_button = tk.Button(app, text="Delete Contact", command=delete_contact)

add_button.pack(pady=5)
view_button.pack(pady=5)
search_button.pack(pady=5)
update_button.pack(pady=5)
delete_button.pack(pady=5)

contact_list = tk.Listbox(app, width=50)
contact_list.pack(pady=10)

view_contacts()
app.mainloop()
