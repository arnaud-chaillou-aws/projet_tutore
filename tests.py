from tkinter import *

fenetre = Tk()
def premier_bouton():
    validlogin()
    validpassword()

def validlogin():
    loginval = login.get()
    if loginval == "":
        pass
    else:
        print(loginval)
def validpassword():
    passwordval = password.get()
    if passwordval == "":
        pass
    else:
        print(passwordval)

# premier message
label = Label(fenetre, text="Une authentification est requise", bg="light grey")
label.pack()

#message login
label = Label(fenetre, text="\rLogin", bg="light grey")
label.pack()
# entrée login
value = StringVar()
value.set("")
login = Entry(fenetre, textvariable=value)
login.pack()

#message password
label = Label(fenetre, text="\rPassword", bg="light grey")
label.pack()
# entrée password
value = StringVar()
value.set("")
password = Entry(fenetre,textvariable=value, show='*')
password.pack()
#message password
label = Label(fenetre, text="\r", bg="light grey")
label.pack()
#Bouton validé
bouton = Button(fenetre, text="Valider", command=premier_bouton)
bouton.pack()

def main():
    fenetre.mainloop()

if __name__ == ("__main__"):
    main()
