import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as msg
#import mysqlcmd
import crypto
import authentification

class Auth(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("authentification")
        self.geometry("400x250")

        #Message n°1
        self.label = tk.Label(self, text="Une authentification est requise", bg="light grey").pack()

        #Demande login
        self.label = tk.Label(self, text="\rLogin", bg="light grey").pack()

        #Champ login
        self.value = tk.StringVar()
        self.value.set("")
        self.login = tk.Entry(self, textvariable=self.value)
        self.login.pack()

        #Demande password
        self.label = tk.Label(self, text="\rPassword", bg="light grey").pack()

        #Champ mot de passe
        self.value = tk.StringVar()
        self.value.set("")
        self.password = tk.Entry(self,textvariable=self.value, show='*')
        self.password.pack()

        #Demande network
        self.label = tk.Label(self, text="\rid reseau", bg="light grey").pack()

        #Champ id reseau

        self.value = tk.StringVar()
        self.value.set("")
        self.id_reseau = tk.Entry(self,textvariable=self.value, show='*')
        self.id_reseau.pack()

        #Vide
        self.label = tk.Label(self, text="\r", bg="light grey").pack()

        #Bouton Valider
        self.bouton = tk.Button(self, text="Valider", command=self.bouton_valider)
        self.bouton.pack()

        #Main loop
        self.mainloop()

    def bouton_valider(self):
        login = self.login.get()
        password = self.password.get()
        id_reseau = self.id_reseau.get()
        if login != "" and password != "" and id_reseau != "":
            hashing = crypto.Hash()
            password = hashing.pbkdf2(password)
            print(password)
            self.status = authentification.authentification((login, password))
            if self.status == 1:
                msg.showerror("Erreur", "\rMauvais couple login/mot de passe/reseau")
            else:
                self.destroy()
                Action()
        else:
            msg.showerror("Erreur", "\rRenseigner un login et un mot de passe et un reseau")

class Action(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Action")
        self.geometry("400x300")

        #Menu
        self.menu = tk.Menu(self)

        self.menu1 = tk.Menu(self.menu, tearoff=0)
        self.menu1.add_command(label="Upload", command=self.file_open)
        self.menu1.add_command(label="Download", command=self.file_select)
        self.menu.add_cascade(label="Fichier", menu=self.menu1)

        self.menu2 = tk.Menu(self.menu, tearoff=0)
        self.menu2.add_command(label="documention", command=self.show_help)
        self.menu.add_cascade(label="Aide", menu=self.menu2)

        self.config(menu=self.menu)
        self.mainloop()

    def file_open(self):
        path = filedialog.askopenfilename()
        f=open(path,'rb')
        content = f.read()
        print(content)

    def file_select(self):
        FileSelectionForm(self)

    def show_help(self):
        pass

class FileSelectionForm(tk.Toplevel):
    def __init__(self, master):
        super().__init__()
        self.master = master

        self.title("Selection fichier")
        self.geometry("300x150")

        self.nom_fichier = tk.Label(self, text="Nom du fichier ?")
        self.nom_fichier_entrer = tk.Entry(self, bg="white", fg="black")
        self.code_fichier = tk.Label(self, text="Code de récupération ?")
        self.code_fichier_entrer = tk.Entry(self, bg="white", fg="black")
        self.valid_buttom = tk.Button(self, text="Valider", command=self.submit)

        self.nom_fichier.pack(fill=tk.BOTH, expand=1)
        self.nom_fichier_entrer.pack(fill=tk.BOTH, expand=1)
        self.code_fichier.pack(fill=tk.BOTH, expand=1)
        self.code_fichier_entrer.pack(fill=tk.BOTH, expand=1)
        self.valid_buttom.pack(fill=tk.X)

    def submit(self):
        nom_fichier = self.nom_fichier_entrer.get()
        code_fichier = self.code_fichier_entrer.get()
        print(nom_fichier)
        print(code_fichier)
        self.destroy()

if __name__ == "__main__":
    Auth()
