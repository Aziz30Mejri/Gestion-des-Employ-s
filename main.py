from tkinter import *
from tkinter import ttk
import re
from db import Database
from tkinter import messagebox, END
db = Database("Employee.db")


root = Tk()
root.title('Système de Gestion des Employés')
root.geometry('1240x615+0+0')
root.resizable(False, False)
root.configure(bg='#2c3e50')

nom = StringVar()
age = StringVar()
#age = IntVar()
emploi = StringVar()
genre = StringVar()
email = StringVar()
mobile = StringVar()

#==== Entries Frame ====#
entries_frame = Frame(root, bg='#2c3e50')
entries_frame.place(x=1, y=1, width=360, height=510)
title = Label(entries_frame, text='Employé Entreprise', font=('Calibri', 18, 'bold'), bg='#2c3e50', fg='white')
title.place(x=10, y=1)
lblNom = Label(entries_frame, text='Nom', font=('Calibri', 16), bg='#2c3e50', fg='white')
lblNom.place(x=10, y=50)
txtNom = Entry(entries_frame, textvariable=nom, width=20, font=('Calibri', 16))
txtNom.place(x=120, y=50)
lblEmploi = Label(entries_frame, text='Emploi', font=('Calibri', 16), bg='#2c3e50', fg='white')
lblEmploi.place(x=10, y=90)
txtEmploi = Entry(entries_frame, width=20, textvariable=emploi, font=('Calibri', 16))
txtEmploi.place(x=120, y=90)
lblGenre = Label(entries_frame, text='Genre', font=('Calibri', 16), bg='#2c3e50', fg='white')
lblGenre.place(x=10, y=130)
comboGenre = ttk.Combobox(entries_frame, textvariable=genre, state='readonly', width=18, font=('Calibri', 16))
comboGenre['values'] = ("Mâle","Féminin")
comboGenre.place(x=120, y=130)
lblAge = Label(entries_frame, text='Âge', font=('Calibri', 16), bg='#2c3e50', fg='white')
lblAge.place(x=10, y=170)
spinAge = Spinbox(entries_frame, from_=18, to=50, textvariable=age, width=18, font=('Calibri', 16))
spinAge.place(x=120, y=170)
lblEmail = Label(entries_frame, text='Email', font=('Calibri', 16), bg='#2c3e50', fg='white')
lblEmail.place(x=10, y=210)
txtEmail = Entry(entries_frame, textvariable=email, width=20, font=('Calibri', 16))
txtEmail.place(x=120, y=210)
lblMobile = Label(entries_frame, text='Mobile', font=('Calibri', 16), bg='#2c3e50', fg='white')
lblMobile.place(x=10, y=250)
txtMobile = Entry(entries_frame, textvariable=mobile, width=20, font=('Calibri', 16))
txtMobile.place(x=120, y=250)
lblAdresse = Label(entries_frame, text='Adresse :', font=('Calibri', 16), bg='#2c3e50', fg='white')
lblAdresse.place(x=10, y=290)
txtAdresse = Text(entries_frame, width=30, height=2, font=('Calibri', 16))
txtAdresse.place(x=10, y=330)


#==== Define ====#
def hide():
    root.geometry("375x515+0+0")


def show():
    root.geometry("1240x615+0+0")
btnhide = Button(entries_frame, text='Cacher', cursor='hand2', bg='white', bd=1, relief=SOLID, command=hide)
btnhide.place(x=240, y=10)
btnshow = Button(entries_frame, text='Afficher', cursor='hand2', bg='white', bd=1, relief=SOLID, command=show)
btnshow.place(x=300, y=10)


def getData(event):
    selected_row = tv.focus()
    data = tv.item(selected_row)
    global row
    row = data["values"]
    nom.set(row[1])
    age.set(row[2])
    emploi.set(row[3])
    email.set(row[4])
    genre.set(row[5])
    mobile.set(row[6])
    txtAdresse.delete(1.0, END)
    txtAdresse.insert(END, row[7])


def update():
    nom_value = txtNom.get().strip()
    age_value = age.get().strip()
    #age_value = age.get()
    emploi_value = txtEmploi.get().strip()
    email_value = txtEmail.get().strip()
    genre_value = comboGenre.get().strip()
    mobile_value = txtMobile.get().strip()
    adresse_value = txtAdresse.get(1.0, END).strip()
    if (nom_value == "" or age_value == "" or emploi_value == "" or email_value == "" or
            genre_value == "" or mobile_value == "" or adresse_value == ""):
        messagebox.showerror("Erreur", "Veuillez remplir toutes les entrées")
        return
    if (nom_value == "" or age_value == "" or emploi_value == "" or email_value == "" or
            genre_value == "" or mobile_value == "" or adresse_value == ""):
        messagebox.showerror("Erreur", "Veuillez remplir toutes les entrées")
        return
    if not re.match(r'^[a-zA-Z\s-]+$', nom_value):
        messagebox.showerror("Erreur", "Le nom ne doit contenir que des caractères alphabétiques")
        return
    if not emploi_value.isalpha():
        messagebox.showerror("Erreur", "L'emploi ne doit contenir que des caractères alphabétiques")
        return
    if not (age_value.isdigit() and 18 <= int(age_value) <= 50):
        messagebox.showerror("Erreur", "Veuillez entrer âge validé ")
        return
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email_value):
        messagebox.showerror("Erreur", "Veuillez entrer une adresse email valide")
        return
    if not re.match(r'^\d{8}$', mobile_value):
        messagebox.showerror("Erreur", "Le numéro de mobile doit comporter 8 chiffres")
        return
    try:
        db.update(
            row[0],
            nom_value,
            int(age_value),
            emploi_value,
            email_value,
            genre_value,
            mobile_value,
            adresse_value
        )
        messagebox.showinfo('Succès', 'Les données des employés sont mises à jour')
        Clear()
        displayAll()
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue: {e}")


def delete():
    try:
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cet employé?"):
            db.remove(row[0])
            Clear()
            displayAll()
            messagebox.showinfo('Succès', 'Employé supprimé avec succès')
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue: {e}")


def Clear():
    nom.set("")
    age.set("")
    emploi.set("")
    genre.set("")
    email.set("")
    mobile.set("")
    txtAdresse.delete(1.0, END)


def displayAll():
    tv.delete(* tv.get_children())
    for row in db.fetch():
        tv.insert("", END, values=row)


def add_employee():
    nom_value = txtNom.get().strip()
    age_value = age.get().strip()
    #age_value = age.get()
    emploi_value = txtEmploi.get().strip()
    email_value = txtEmail.get().strip()
    genre_value = comboGenre.get().strip()
    mobile_value = txtMobile.get().strip()
    adresse_value = txtAdresse.get(1.0, END).strip()
    if (nom_value == "" or age_value == "" or emploi_value == "" or email_value == "" or
        genre_value == "" or mobile_value == "" or adresse_value == ""):
        messagebox.showerror("Erreur", "Veuillez remplir toutes les entrées")
        return
    if not re.match(r'^[a-zA-Z\s-]+$', nom_value):
        messagebox.showerror("Erreur", "Le nom ne doit contenir que des caractères alphabétiques")
        return
    if not emploi_value.isalpha():
        messagebox.showerror("Erreur", "L'emploi  ne doit contenir que des caractères alphabétiques")
        return
    if not (age_value.isdigit() and 18 <= int(age_value) <= 50):
        messagebox.showerror("Erreur", "Veuillez entrer âge validé")
        return
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email_value):
        messagebox.showerror("Erreur", "Veuillez entrer une adresse email valide")
        return
    if not re.match(r'^\d{8}$', mobile_value):
        messagebox.showerror("Erreur", "Le numéro de mobile doit comporter 8 chiffres")
        return
    try:
        db.insert(
            nom_value,
            int(age_value),
            #age_value,
            emploi_value,
            email_value,
            genre_value,
            mobile_value,
            adresse_value
        )
        messagebox.showinfo("Succès", "Ajout d'un nouvel employé")
        Clear()
        displayAll()
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")


#==== Buttons Frame ====#
btn_frame = Frame(entries_frame,bg='#2C3E50', bd=1, relief=SOLID)
btn_frame.place(x=10, y=410, width=335, height=100)

btnAdd = Button(btn_frame,
                text='Ajouter Détails',
                width=14,
                height=1,
                font=('Calibri',16),
                fg='white',
                bg='#16A085',
                bd=0,
                command=add_employee
                ).place(x=4,y=5)

btnEdit = Button(btn_frame,
                text='Modifier Détails',
                width=14,
                height=1,
                font=('Calibri',16),
                fg='white',
                bg='#2980B9',
                bd=0,
                 command=update
                ).place(x=4,y=50)

btnDelete = Button(btn_frame,
                text='Supprimer Détails',
                width=14,
                height=1,
                font=('Calibri',16),
                fg='white',
                bg='#C0392B',
                bd=0,
                command=delete
                ).place(x=170,y=5)

btnClear = Button(btn_frame,
                text='Effacer Détails',
                width=14,
                height=1,
                font=('Calibri',16),
                fg='white',
                bg='#F39C12',
                bd=0,
                command=Clear
                ).place(x=170,y=50)

#==== Table Frame ====#
tree_frame = Frame(root, bg='white')
tree_frame.place(x=365, y=1, width=875, height=610)
style = ttk.Style()
style.configure("mystyle.Treeview", font=('Calibri', 13), rowheight=50)
style.configure("mystyle.Treeview.Heading", font=('Calibri', 13))

tv = ttk.Treeview(tree_frame, columns=(1,2,3,4,5,6,7,8), style="mystyle.Treeview")
tv.heading("1", text='ID')
tv.column("1", width='35', anchor='center')
tv.heading("2", text='Nom')
tv.column("2", width='140', anchor='center')
tv.heading("3", text='Age')
tv.column("3", width='45', anchor='center')
tv.heading("4", text="Emploi")
tv.column("4", width="120", anchor='center')
tv.heading("5", text="Email")
tv.column("5", width="175", anchor='center')
tv.heading("6", text="Genre")
tv.column("6", width="90", anchor='center')
tv.heading("7", text="Mobile")
tv.column("7", width="110", anchor='center')
tv.heading("8", text="Adresse")
tv.column("8", width="150", anchor='center')
tv['show'] = 'headings'
tv.bind("<ButtonRelease-1>", getData)
tv.place(x=1, y=1, height=610, width=875)
root.after(0, lambda: age.set(""))

displayAll()
root.mainloop()
