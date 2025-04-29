import tkinter as tk
from tkinter import messagebox
import json
import os

CONTACTS_FILE = "contacts.json"


def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)
    return []


def save_contacts():
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)


def add_contact():
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    email = entry_email.get().strip()
    address = entry_address.get().strip()

    if not name or not phone:
        messagebox.showwarning("Input Error", "Store name and phone number are required.")
        return

    contacts.append({
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    })
    save_contacts()
    update_contact_list()
    clear_fields()


def update_contact_list(filtered=None):
    listbox_contacts.delete(0, tk.END)
    show_list = filtered if filtered is not None else contacts
    for contact in show_list:
        listbox_contacts.insert(tk.END, f"{contact['name']} - {contact['phone']}")


def select_contact(event):
    try:
        index = listbox_contacts.curselection()[0]
        selected = contacts[index]
        entry_name.delete(0, tk.END)
        entry_name.insert(0, selected["name"])
        entry_phone.delete(0, tk.END)
        entry_phone.insert(0, selected["phone"])
        entry_email.delete(0, tk.END)
        entry_email.insert(0, selected["email"])
        entry_address.delete(0, tk.END)
        entry_address.insert(0, selected["address"])
    except IndexError:
        pass


def search_contact():
    query = entry_search.get().lower()
    filtered = [c for c in contacts if query in c["name"].lower() or query in c["phone"]]
    update_contact_list(filtered)


def update_contact():
    try:
        index = listbox_contacts.curselection()[0]
    except IndexError:
        messagebox.showwarning("Selection Error", "Select a contact to update.")
        return

    contacts[index] = {
        "name": entry_name.get().strip(),
        "phone": entry_phone.get().strip(),
        "email": entry_email.get().strip(),
        "address": entry_address.get().strip()
    }
    save_contacts()
    update_contact_list()
    clear_fields()


def delete_contact():
    try:
        index = listbox_contacts.curselection()[0]
    except IndexError:
        messagebox.showwarning("Selection Error", "Select a contact to delete.")
        return

    del contacts[index]
    save_contacts()
    update_contact_list()
    clear_fields()


def clear_fields():
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_address.delete(0, tk.END)


root = tk.Tk()
root.title("Contact Book")
root.geometry("500x600")

contacts = load_contacts()


tk.Label(root, text="Contact Name:").pack()
entry_name = tk.Entry(root, width=50)
entry_name.pack()

tk.Label(root, text="Phone Number:").pack()
entry_phone = tk.Entry(root, width=50)
entry_phone.pack()

tk.Label(root, text="Email:").pack()
entry_email = tk.Entry(root, width=50)
entry_email.pack()

tk.Label(root, text="Address:").pack()
entry_address = tk.Entry(root, width=50)
entry_address.pack()


tk.Button(root, text="Add Contact", command=add_contact, bg="lightgreen").pack(pady=5)
tk.Button(root, text="Update Contact", command=update_contact, bg="lightblue").pack(pady=5)
tk.Button(root, text="Delete Contact", command=delete_contact, bg="tomato").pack(pady=5)


tk.Label(root, text="Search (by name or phone):").pack(pady=5)
entry_search = tk.Entry(root, width=50)
entry_search.pack()
tk.Button(root, text="Search", command=search_contact).pack(pady=5)


listbox_contacts = tk.Listbox(root, height=10, width=60)
listbox_contacts.pack(pady=10, fill=tk.BOTH, expand=True)
listbox_contacts.bind("<<ListboxSelect>>", select_contact)

update_contact_list()

root.mainloop()
