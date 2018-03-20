import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as msg
import pyperclip
import crypto
import authentification
import fonctions
import communication

class Homepage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menu")
        self.geometry("400x300")

        self.label1 = tk.Label(self, text ="\nVeuiller choisir une action :").pack()
        self.videlabel = tk.Label(self, text = "\n").pack()
        self.create_user_bouton = tk.Button(self, text="Create user", command=self.createuserform)
        self.create_user_bouton.pack()
        self.videlabel = tk.Label(self, text = "\n").pack()
        self.create_network_bouton = tk.Button(self, text="Create network", command=self.createnetworkform)
        self.create_network_bouton.pack()
        self.videlabel = tk.Label(self, text = "\n").pack()
        self.join_network_bouton = tk.Button(self, text="Join network", command=self.joinnetwork)
        self.join_network_bouton.pack()
        self.videlabel = tk.Label(self, text = "\n").pack()
        self.authentification_form_bouton = tk.Button(self, text="Authentification", command=self.authentification_form)
        self.authentification_form_bouton.pack()
        self.videlabel = tk.Label(self, text = "\n").pack()
        self.mainloop()

    def authentification_form(self):
        self.destroy()
        Auth()

    def joinnetwork(self):
        JoinNetwork(self)

    def createnetworkform(self):
        CreateNetwork(self)

    def createuserform(self):
        CreateUser(self)

class JoinNetwork(tk.Toplevel):
    def __init__(self, master):
        super().__init__()

        self.master = master
        self.title("Join Network")
        self.geometry("350x200")

        self.label1 = tk.Label(self, text = "Veuiller renseigner l'ip d'un noeud, l'id du reseau, votre ip et le mot de passe du reseau:").pack()
        self.videlabel = tk.Label(self, text = "\n").pack()
        self.master_ip = tk.Label(self, text="Ip noeud ?")
        self.master_ip_entrer = tk.Entry(self, bg="white", fg="black")
        self.id_reseau = tk.Label(self, text="Id reseau ?")
        self.id_reseau_entrer = tk.Entry(self, bg="white", fg="black")
        self.ip_client = tk.Label(self, text="votre ip ?")
        self.ip_client_entrer = tk.Entry(self, bg="white", fg="black")
        self.password = tk.Label(self, text="Mot de passe réseau")
        self.password_entrer = tk.Entry(self, bg="white", fg="black", show='*')
        self.valid_buttom = tk.Button(self, text="Valider", command=self.valider)

        self.master_ip.pack(fill=tk.BOTH, expand=1)
        self.master_ip_entrer.pack(fill=tk.BOTH, expand=1)
        self.id_reseau.pack(fill=tk.BOTH, expand=1)
        self.id_reseau_entrer.pack(fill=tk.BOTH, expand=1)
        self.ip_client.pack(fill=tk.BOTH, expand=1)
        self.ip_client_entrer.pack(fill=tk.BOTH, expand=1)
        self.password.pack(fill=tk.BOTH, expand=1)
        self.password_entrer.pack(fill=tk.BOTH, expand=1)
        self.valid_buttom.pack(fill=tk.X)

    def valider(self):
        pass

class CreateNetwork(tk.Toplevel):
    def __init__(self, master):
        super().__init__()

        self.master = master
        self.title("Create Network")
        self.geometry("250x150")

        self.label1 = tk.Label(self, text = "Veuiller renseigner le mot de passe et le nombre maximal de noeud du reseau:")
        self.labelmaxnode = tk.Label(self, text = "Nombre de noeud maximal ?").pack()
        self.maxnode_entrer = tk.Entry(self, bg="white", fg="black")
        self.labelpassword = tk.Label(self, text = "Mot de passe ?").pack()
        self.password_entrer = tk.Entry(self, bg="white", fg="black", show='*')
        self.valid_buttom = tk.Button(self, text="Valider", command=self.valider)

        self.label1.pack(fill=tk.BOTH, expand=1)
        self.maxnode_entrer.pack(fill=tk.BOTH, expand=1)
        self.password_entrer.pack(fill=tk.BOTH, expand=1)
        self.valid_buttom.pack(fill=tk.X)

    def valider(self):
        password = str(self.password_entrer.get())
        try :
            maxnode = int(self.password_entrer.get())
        except:
            maxnode = 20
        if password == "" or maxnode > 200:
            msg.showerror("Erreur", "Veuillez entrer un mot de passe ou un nombre de noeud maximum inferieur a 200")
        else:
            state, network_id = fonctions.createnetwork(password, maxnode)
            if state == 0:
                msg.showinfo("Validation", "Le réseau à bien été ajouté à la base de donnée local\nL'id reseau est : %s" % (network_id))
                pyperclip.copy(network_id)
            else:
                msg.showerror("Erreur", "Erreur lors de la création du réseau veuillez réessayer")
        self.destroy()

class CreateUser(tk.Toplevel):
    def __init__(self, master):
        super().__init__()

        self.master = master
        self.title("Create user")
        self.geometry("400x300")

        self.label1 = tk.Label(self, text ="Veuiller renseigner les informations suivante:").pack()
        self.videlabel = tk.Label(self, text = "\n").pack()
        self.username = tk.Label(self, text="Username ?")
        self.username_entrer = tk.Entry(self, bg="white", fg="black")
        self.password = tk.Label(self, text="Password ?")
        self.password_entrer = tk.Entry(self, bg="white", fg="black", show='*')
        self.email = tk.Label(self, text="Addresse email ? \r(optionnel)")
        self.email_entrer = tk.Entry(self, bg="white", fg="black")
        self.valid_buttom = tk.Button(self, text="Valider", command=self.valider)

        self.username.pack(fill=tk.BOTH, expand=1)
        self.username_entrer.pack(fill=tk.BOTH, expand=1)
        self.password.pack(fill=tk.BOTH, expand=1)
        self.password_entrer.pack(fill=tk.BOTH, expand=1)
        self.email.pack(fill=tk.BOTH, expand=1)
        self.email_entrer.pack(fill=tk.BOTH, expand=1)
        self.valid_buttom.pack(fill=tk.X)

    def valider(self):
        username = self.username_entrer.get()
        password = self.password_entrer.get()
        email = self.email_entrer.get()
        if email == "":
            email = "Non renseigné"

        if username == "" or password == "":
            msg.showerror("Erreur", "Veuillez entrer un Username et un mot de passe")
        else:
            state = fonctions.createuser(username, password, email)
            if state == 0:
                msg.showinfo("Validation", "Vous avez bien été ajouté a la base de donnée local")

            else:
                msg.showerror("Erreur", "Username déjà utilisé")
        self.destroy()

class Auth(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("authentification")
        self.geometry("400x250")

        #Message n°1
        self.label = tk.Label(self, text="Une authentification est requise").pack()

        #Demande login
        self.label = tk.Label(self, text="\rLogin").pack()

        #Champ login
        self.value = tk.StringVar()
        self.value.set("")
        self.login = tk.Entry(self, textvariable=self.value)
        self.login.pack()

        #Demande password
        self.label = tk.Label(self, text="\rPassword").pack()

        #Champ mot de passe
        self.value = tk.StringVar()
        self.value.set("")
        self.password = tk.Entry(self,textvariable=self.value, show='*')
        self.password.pack()

        #Demande network
        self.label = tk.Label(self, text="\rid reseau").pack()

        #Champ id reseau

        self.value = tk.StringVar()
        self.value.set("")
        self.id_reseau = tk.Entry(self,textvariable=self.value, show='*')
        self.id_reseau.pack()

        #Vide
        self.label = tk.Label(self, text="\r").pack()

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

class HelpMe():
    def __init__(self):
        self.FileSelectionForm = ("Pop-up bouton download")
        self.Action = ("Fenetre post authentification, bouton upload inclu dans la classe")
        self.Auth = ("Fenetre d'authentification, utilise authentification.py et crypto.py")
        self.CreateUser = ("Fenetre create user classe enfant de Homepage")
        self.CreateNetwork = ("Fenetre creation du reseau classe enfant de Homepage")
        self.JoinNetwork = ("Fenetre connexion a un réseau classe enfant de Homepage")
        self.Homepage = ("Page d'aceuille principale")

    def __str__(self):
        return("Fonctions explique : FileSelectionForm, Action, Auth, CreateUser, CreateNetwork, JoinNetwork, Homepage")
if __name__ == "__main__":
    try:
        Homepage()
    except:
        print("Service isn't started")
