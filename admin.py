import os
import tkinter as tk
from tkinter import ttk, messagebox
from bs4 import BeautifulSoup

# --- CONFIG ---
base_path = r"D:\Hichem\Siteweb\chiheeeem.github.io\specialties"

def get_modules(file_path):
    modules = []
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        for btn in soup.find_all("button", class_="accordion-button"):
            name = btn.get_text(strip=True)
            if name:
                modules.append(name)
    return modules

def get_links(file_path, module):
    links = []
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        for btn in soup.find_all("button", class_="accordion-button"):
            name = btn.get_text(strip=True)
            if name.strip().lower() == module.strip().lower():
                accordion_body = btn.find_next("div", class_="accordion-body")
                if accordion_body:
                    for a in accordion_body.find_all("a"):
                        links.append((a.get_text(strip=True), a.get("href")))
                break
    return links

def refresh_links_list():
    link_listbox.delete(0, tk.END)
    specialty = specialty_var.get().lower()
    semester = semester_var.get().lower()
    module = module_var.get()
    if specialty and semester and module:
        file_path = os.path.join(base_path, specialty, f"{semester}.html")
        if os.path.exists(file_path):
            links = get_links(file_path, module)
            for text, url in links:
                link_listbox.insert(tk.END, f"{text} | {url}")

def add_link():
    specialty = specialty_var.get().lower()
    semester = semester_var.get().lower()
    module = module_var.get()
    link_text = link_text_var.get().strip()
    link_url = link_url_var.get().strip()

    if not (specialty and semester and module and link_text and link_url):
        messagebox.showerror("Error", "Please fill all fields!")
        return

    file_path = os.path.join(base_path, specialty, f"{semester}.html")

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    found = False
    for btn in soup.find_all("button", class_="accordion-button"):
        name = btn.get_text(strip=True)
        if name.strip().lower() == module.strip().lower():
            accordion_body = btn.find_next("div", class_="accordion-body")
            if accordion_body:
                new_tag = soup.new_tag("a", href=link_url, target="_blank")
                new_tag.string = link_text
                p_tag = soup.new_tag("p")
                p_tag.append(new_tag)
                accordion_body.append(p_tag)
                found = True
            break

    if found:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        messagebox.showinfo("Success", f"Added '{link_text}' to module '{module}'")
        refresh_links_list()
    else:
        messagebox.showerror("Error", f"Module '{module}' not found in {file_path}")

def modify_link():
    selected = link_listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "Select a link to modify!")
        return

    specialty = specialty_var.get().lower()
    semester = semester_var.get().lower()
    module = module_var.get()
    new_text = link_text_var.get().strip()
    new_url = link_url_var.get().strip()

    file_path = os.path.join(base_path, specialty, f"{semester}.html")
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    found = False
    for btn in soup.find_all("button", class_="accordion-button"):
        if btn.get_text(strip=True).strip().lower() == module.strip().lower():
            accordion_body = btn.find_next("div", class_="accordion-body")
            if accordion_body:
                a_tags = accordion_body.find_all("a")
                old_text, old_url = link_listbox.get(selected[0]).split(" | ")
                for a in a_tags:
                    if a.get_text(strip=True) == old_text and a.get("href") == old_url:
                        a.string = new_text
                        a['href'] = new_url
                        found = True
                        break
            break

    if found:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        messagebox.showinfo("Success", "Link modified successfully!")
        refresh_links_list()
    else:
        messagebox.showerror("Error", "Link not found!")

def delete_link():
    selected = link_listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "Select a link to delete!")
        return

    specialty = specialty_var.get().lower()
    semester = semester_var.get().lower()
    module = module_var.get()

    file_path = os.path.join(base_path, specialty, f"{semester}.html")
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    found = False
    for btn in soup.find_all("button", class_="accordion-button"):
        if btn.get_text(strip=True).strip().lower() == module.strip().lower():
            accordion_body = btn.find_next("div", class_="accordion-body")
            if accordion_body:
                a_tags = accordion_body.find_all("a")
                old_text, old_url = link_listbox.get(selected[0]).split(" | ")
                for a in a_tags:
                    if a.get_text(strip=True) == old_text and a.get("href") == old_url:
                        a.decompose()
                        found = True
                        break
            break

    if found:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        messagebox.showinfo("Success", "Link deleted successfully!")
        refresh_links_list()
    else:
        messagebox.showerror("Error", "Link not found!")

def update_modules(*args):
    specialty = specialty_var.get().lower()
    semester = semester_var.get().lower()
    if specialty and semester:
        file_path = os.path.join(base_path, specialty, f"{semester}.html")
        if os.path.exists(file_path):
            modules = get_modules(file_path)
            module_menu["values"] = modules
            if modules:
                module_menu.current(0)
                refresh_links_list()

# --- GUI ---
root = tk.Tk()
root.title("Course Link Manager")
root.geometry("800x500")

# Make grid expandable
root.grid_rowconfigure(8, weight=1)  # Listbox row
root.grid_columnconfigure(1, weight=1)  # Inputs column

ttk.Label(root, text="Specialty:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
specialty_var = tk.StringVar()
specialty_menu = ttk.Combobox(root, textvariable=specialty_var, values=["RT", "ST"], state="readonly", width=20)
specialty_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")

ttk.Label(root, text="Semester:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
semester_var = tk.StringVar()
semester_menu = ttk.Combobox(root, textvariable=semester_var, values=["S1", "S2"], state="readonly", width=20)
semester_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")

ttk.Label(root, text="Module:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
module_var = tk.StringVar()
module_menu = ttk.Combobox(root, textvariable=module_var, state="readonly", width=40)
module_menu.grid(row=2, column=1, padx=5, pady=5, sticky="w")

ttk.Label(root, text="Link Label:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
link_text_var = tk.StringVar()
ttk.Entry(root, textvariable=link_text_var, width=50).grid(row=3, column=1, padx=5, pady=5, sticky="w")

ttk.Label(root, text="Link URL:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
link_url_var = tk.StringVar()
ttk.Entry(root, textvariable=link_url_var, width=50).grid(row=4, column=1, padx=5, pady=5, sticky="w")

ttk.Button(root, text="Add Link", command=add_link, width=25).grid(row=5, column=0, columnspan=2, pady=5)
ttk.Button(root, text="Modify Link", command=modify_link, width=25).grid(row=6, column=0, columnspan=2, pady=5)
ttk.Button(root, text="Delete Link", command=delete_link, width=25).grid(row=7, column=0, columnspan=2, pady=5)

# Make Listbox expandable
link_listbox = tk.Listbox(root)
link_listbox.grid(row=8, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

# Scrollbar
scrollbar = ttk.Scrollbar(root, orient="vertical", command=link_listbox.yview)
scrollbar.grid(row=8, column=2, sticky="ns", pady=10)
link_listbox.config(yscrollcommand=scrollbar.set)

# Update module dropdown when specialty/semester changes
specialty_var.trace_add("write", update_modules)
semester_var.trace_add("write", update_modules)
module_var.trace_add("write", lambda *args: refresh_links_list())

root.mainloop()
