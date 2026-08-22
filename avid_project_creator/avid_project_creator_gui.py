"""CustomTkinter GUI frontend for avid_project_creator.py.
Presents a grid of buttons for each supported project type (Standard, , News at 25p/50i),
and calls avid_project_creator.createProjects() with the selected dummy template on click."""
# exe docs https://github.com/TomSchimansky/CustomTkinter/wiki/Packaging

from customtkinter import *
import tkinter.messagebox as tkmb

import avid_project_creator

app = CTk()
app.title("Avid Project Creator")

# sets window size
app.geometry("400x220")

def buttonAction(name, button):
    if avid_project_creator.createProjects(name) == False:
        button.configure(fg_color="red")
        tkmb.showinfo(title="Trauer!", message="Das Projekt wurde nicht erstellt, da es bereits existiert!")
    else:
        button.configure(fg_color="green")
        tkmb.showinfo(title="Jubel!", message="Die Projekte wurden erfolgreich erstellt!")

# 25p
def Standard25pClicked():
    buttonAction("Dummy_Standard_25p", Dummy_Standard_25p)

def Ingest25pClicked():
    buttonAction("Dummy_Ingest_25p", Dummy_Ingest_25p)

def Sendung25pClicked():
    buttonAction("Dummy_Sendungsprojekt_25p", Dummy_Sendungsprojekt_25p)

def NewsSendung25pClicked():
    buttonAction("Dummy_News_Sendungsprojekt_25p", Dummy_News_Sendungsprojekt_25p)

# 50i
def Standard50iClicked():
    buttonAction("Dummy_Standard_50i", Dummy_Standard_50i)

def Ingest50iClicked():
    buttonAction("Dummy_Ingest_50i", Dummy_Ingest_50i)

def Sendung50iClicked():
    buttonAction("Dummy_Sendungsprojekt_50i", Dummy_Sendungsprojekt_50i)

def NewsSendung50iClicked():
    buttonAction("Dummy_News_Sendungsprojekt_50i", Dummy_News_Sendungsprojekt_50i)

# 25p
Dummy_Standard_25p = CTkButton(app, width=180, text="Standard Projekt 25p", command=Standard25pClicked)
Dummy_Standard_25p.grid(column=0, row=0, padx=10, pady=13)
Dummy_Standard_50i = CTkButton(app, width=180, text="Standard Projekt 50i", command=Standard50iClicked)
Dummy_Standard_50i.grid(column=1, row=0, pady=13)

Dummy_Ingest_25p = CTkButton(app, width=180, text=" Ingest Projekt 25p", command=Ingest25pClicked)
Dummy_Ingest_25p.grid(column=0, row=1, pady=13)
Dummy_Ingest_50i = CTkButton(app, width=180, text=" Ingest Projekt 50i", command=Ingest50iClicked)
Dummy_Ingest_50i.grid(column=1, row=1, pady=13)

Dummy_Sendungsprojekt_25p = CTkButton(app, width=180, text=" Sendungsprojekt 25p", command=Sendung25pClicked)
Dummy_Sendungsprojekt_25p.grid(column=0, row=2, pady=13)
Dummy_Sendungsprojekt_50i = CTkButton(app, width=180, text=" Sendungsprojekt 50i", command=Sendung50iClicked)
Dummy_Sendungsprojekt_50i.grid(column=1, row=2, pady=13)

Dummy_News_Sendungsprojekt_25p = CTkButton(app, width=180, text="News Sendungsprojekt 25p", command=NewsSendung25pClicked)
Dummy_News_Sendungsprojekt_25p.grid(column=0, row=3, pady=13)
Dummy_News_Sendungsprojekt_50i = CTkButton(app, width=180, text="News Sendungsprojekt 50i", command=NewsSendung50iClicked)
Dummy_News_Sendungsprojekt_50i.grid(column=1, row=3, pady=13)

app.mainloop()