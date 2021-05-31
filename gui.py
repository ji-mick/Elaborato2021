from tkinter import *
from tkinter import filedialog
import sendEmail
import encryption
import receiveEmail


main_window = Tk()
main_window.title("Client di posta elettronica")
main_frame = Frame(main_window)
main_frame.pack()
email = Frame(main_frame)
email.pack(side=LEFT)
attachment_path = "./attachment/"
filename = None


def attachment(lbl_attachment):
    global filename
    filename = filedialog.askopenfilename(
        initialdir="/home/", title="select a file")
    temp = filename.split("/")
    string = temp[len(temp)-1]
    lbl_attachment.config(text=f"il tuo allegato: {string}")


def utility(lbl_attachment):
    string = lbl_attachment.cget("text").split(" ")
    temp = string[len(string)-1]
    foo = temp.split(".")
    if foo[len(foo)-1] == "pgp":
        return encryption.encrypted_folder_path + string[len(string)-1]
    else:
        return filename


def cypher_window(lbl_attachment):
    string = """
        Utilizza il pulsante 'cifra' per importare la chiave pubblica
        del destinatario e successivamente firmare e cifrare il tuo documento.

        Utilizza il pulsante 'genara chiavi' per creare una coppia di chiavi
        ed esportarle in un file .asc contenente la chiave pubblica da dare al destinatario.
  
    """
    cypher = Toplevel()
    cypher.title("cifra allegato")
    lbl = Label(cypher,  text=string)
    lbl.pack(padx=20, pady=10)
    btn_key = Button(cypher, text="genera chiavi",
                     command=encryption.export_key)
    btn_key.pack(side=RIGHT, pady=20, padx=30)
    btn_encrypt = Button(cypher, text="cifra",
                         command=lambda: encryption.encryption(filename, lbl_attachment, cypher))
    btn_encrypt.pack(side=LEFT, pady=20, padx=30)


def send_email_gui():
    send_email_W = Frame(
        main_frame, highlightbackground="black", highlightthickness=1)
    send_email_W.pack(side=RIGHT, padx=20, pady=5)
    #send_email_W.title("Client di posta elettronica")
    destinatario = Entry(send_email_W, width=50)
    destinatario.insert(0, 'A:')
    destinatario.pack(padx=20, pady=10)
    oggetto = Entry(send_email_W, width=50)
    oggetto.insert(0, 'Oggetto:')
    oggetto.pack(padx=20, pady=10)
    message = Text(send_email_W, width=50)
    message.pack(padx=20, pady=10)
    lbl_attachment = Label(send_email_W, text="")
    lbl_attachment.pack(padx=20, pady=10)

    btn_delete = Button(send_email_W, text="Chiudi",
                        command=lambda: send_email_W.destroy())
    btn_delete.pack(side=LEFT, pady=20, padx=30)
    btn_attachment = Button(send_email_W, text="Allegato",
                            command=lambda: attachment(lbl_attachment))
    btn_attachment.pack(side=LEFT, pady=20, padx=30)
    btn_invia = Button(
        send_email_W,
        text="Invia",
        command=lambda: sendEmail.send(destinatario, oggetto, message, send_email_W, receiveEmail.login_list) if filename == None else sendEmail.sendV2(
            destinatario, oggetto, message, utility(lbl_attachment), send_email_W, receiveEmail.login_list))
    btn_invia.pack(side=RIGHT, pady=20, padx=30)
    btn_crypt = Button(send_email_W, text="Cifra Allegato",
                       command=lambda: cypher_window(lbl_attachment))
    btn_crypt.pack(side=LEFT, pady=20, padx=30)


def openEmail(my_widget):
    my_w = my_widget.widget
    index = int(my_w.curselection()[0])
    value = my_w.get(index)
    global email
    email = Frame(main_frame, highlightbackground="black",
                  highlightthickness=1)
    email.pack(side=LEFT)
    lbl = Label(email)
    lbl.pack(pady=20, padx=20)
    temp = value.split(" ")
    value = temp[0]
    len_list = len(receiveEmail.dictionary_email[index])
    for el in receiveEmail.dictionary_email:
        if el == index:
            if len_list > 3:
                lbl.config(text=dictionary_to_string(index, True))
                btn_download = Button(email, text="scarica Allegato",
                                      command=lambda: receiveEmail.download_attachments(index))
                btn_download.pack(side=LEFT)
            else:
                lbl.config(text=dictionary_to_string(index))
            btn_destroy = Button(email, text="Chiudi email",
                                 command=lambda: email.destroy())
            btn_destroy.pack(side=RIGHT)


def dictionary_to_string(index, flag=False):
    s = ""
    i = 1
    for el in receiveEmail.dictionary_email[index]:
        if not flag or i != len(receiveEmail.dictionary_email[index]):
            s += f"{el} \n"
        i += 1

    return s


def utilityV2(e):
    email.destroy()
    openEmail(e)


def initUI():
    frame_container = Frame(
        main_frame, highlightbackground="black", highlightthickness=1)
    frame_container.pack(side=LEFT, padx=20, pady=5)
    frame = Frame(frame_container)
    frame.pack()
    lbl_title = Label(frame, text="Posta in Arrivo")
    lbl_title.pack(padx=20, pady=30)
    list_email = Listbox(frame, width=50)
    list_email.pack(padx=20, pady=30, side=LEFT, fill="y")

    scrollbar = Scrollbar(frame, orient="vertical")
    scrollbar.config(command=list_email.yview)
    scrollbar.pack(side=RIGHT, fill="y")

    receiveEmail.receive_email(list_email, main_window)
    list_email.config(yscrollcommand=scrollbar.set)
    list_email.bind('<<ListboxSelect>>', lambda e: utilityV2(e))
    btn_new_email = Button(frame_container, text="+", command=send_email_gui)
    btn_new_email.pack(side=RIGHT, pady=20, padx=30)
    btn_decrypt = Button(frame_container, text="Decifra",
                         command=encryption.decription)
    btn_decrypt.pack(side=LEFT, pady=20, padx=30)


if __name__ == "__main__":
    initUI()
    main_window.mainloop()
