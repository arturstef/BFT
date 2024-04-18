import tkinter as tk
from tkinter import ttk


def create_menu(root):
    menubar = tk.Menu(root)

    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Otwórz", command=lambda: print("Otwórz"))
    file_menu.add_command(label="Zapisz", command=lambda: print("Zapisz"))
    file_menu.add_separator()
    file_menu.add_command(label="Zamknij", command=root.destroy)

    menubar.add_cascade(label="Plik", menu=file_menu)

    root.config(menu=menubar)

def create_notebook(root):
    notebook = ttk.Notebook(root)

    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)

    notebook.add(tab1, text="Zakładka 1")
    notebook.add(tab2, text="Zakładka 2")

    label1 = tk.Label(tab1, text="Zawartość zakładki 1")
    label1.pack(padx=10, pady=10)

    label2 = tk.Label(tab2, text="Zawartość zakładki 2")
    label2.pack(padx=10, pady=10)

    notebook.pack(expand=1, fill="both")

# Tworzenie głównego okna
root = tk.Tk()
root.title("Tkinter - Menubar i Notebook")

# Dodanie paska menu
create_menu(root)

# Dodanie notebooka
create_notebook(root)

# Rozpoczęcie głównej pętli programu
root.mainloop()
