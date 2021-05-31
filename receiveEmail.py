from tkinter.constants import END
from tkinter import simpledialog
from tkinter import messagebox
import imap_tools

attachment_path = "./attachment/"
dictionary_email = {}
login_list = []


def imap_login(window):
    global login_list
    while 1:
        window.update_idletasks()
        email = simpledialog.askstring("email", "inserisci la tua email")
        window.update_idletasks()
        password = simpledialog.askstring(
            "password", "inserisci la tua password")
        mailbox = imap_tools.MailBox("imap.gmail.com")
        try:
            mailbox = mailbox.login(email, password)
            break
        except Exception:
            messagebox.showerror("Error", "Dati non validi")

    login_list.append(email)
    login_list.append(password)
    print(mailbox)
    return mailbox


def receive_email(listEmail, window):
    global dictionary_email
    s = ""
    i = 0
    mailbox = imap_login(window)
    for msg in mailbox.fetch():
        foo = []
        print(f"Da: {msg.from_}\nOggetto: {msg.subject}\nBody: {msg.text}")
        foo.append(f"Da: {msg.from_}")
        foo.append(f"Oggetto: {msg.subject}")
        foo.append(msg.text)
        s += f"{msg.from_} {msg.subject}"
        for att in msg.attachments:
            print(f"Allegato: {att.filename}, {att.content_type}\n")
            foo.append(f"Allegato: {att.filename}")
            foo.append(att.payload)
        
        dictionary_email[i] = foo
        listEmail.insert(END, s)
        i += 1
        s = ""


def download_attachments(i):
    temp = dictionary_email[i][len(dictionary_email[i])-2].split(" ")
    filename = temp[len(temp)-1]
    with open(attachment_path + filename, "wb") as f:
        f.write(dictionary_email[i][len(dictionary_email[i])-1])
    messagebox.showinfo("info", "Ho scaricato il file")
