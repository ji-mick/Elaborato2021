import gnupg
import os
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import messagebox

# gnupghome="/home/miki/.gnupg"
gpg = gnupg.GPG()
gpg.encoding = "utf-8"
encrypted_folder_path = "./encrypted/"
decrypted_folder_path = "./decrypted/"


def from_path_to_filename(filename):
    temp = filename.split("/")
    foo = temp[len(temp)-1]
    bar = foo.split(".")
    return bar[0]


def export_key():

    # genero chiavi
    email = simpledialog.askstring(
        "email", "inserisci la tua mail per accedere a pgp")
    passphrase = simpledialog.askstring(
        "passphrase", "inserisci la tua passphrase per accedere al portafoglio di chiavi")

    input_data = gpg.gen_key_input(
        name_email=email,
        passphrase=passphrase,
        key_type="RSA",
        key_length=1024
    )

    key = gpg.gen_key(input_data)
    print(key)

    public_key = gpg.export_keys(str(key))
    with open("user_public_key.asc", "w") as f:
        f.write(public_key)
    messagebox.showinfo(
        "Info", "ho inserito la tua chiave pubblica nel file: \n user_public_key.asc")


def import_key():
    file = filedialog.askopenfilename(
        initialdir="/home/", title="seleziona il file da importare per la chiave pubblica")
    key_data = open(file).read()

    import_key = gpg.import_keys(key_data)
    gpg.trust_keys(import_key.fingerprints, "TRUST_ULTIMATE")

    mykeys = gpg.list_keys()
    print(mykeys)


def encryption(path, lbl, window):

    if path == None:
        lbl.config(text="Non hai scelto un allegato!!")
        window.destroy()
        return
    import_key()

    emailDest = simpledialog.askstring(
        "email", "inserisci la mail del destinatario per cifrare")
    passphrase = simpledialog.askstring(
        "passphrase", "inserisci la tua passphrase per cifrare")
    print(path)
    stream = open(path, "rb")
    fp = gpg.list_keys(True).fingerprints[0]
    print(gpg.list_keys(True))
    print(fp)

    filename = from_path_to_filename(path)
    # chiave pubblica del destinatario e chiave privata del mittente
    data = gpg.encrypt_file(
        stream, recipients=emailDest, sign=fp, passphrase=passphrase, output=encrypted_folder_path + filename + ".pgp")
    print(data.status)
    print(data.ok)
    print(data.stderr)
    filename += ".pgp"
    lbl.config(text=f"il tuo allegato criptato è: {filename}")
    window.destroy()


def decription():
    path = filedialog.askopenfilename(
        initialdir="/home/", title="seleziona il file da decifrare")
    passphrase = simpledialog.askstring(
        "passphrase", "Inserisci la tua passphrase")
    filename = from_path_to_filename(path)
    import_key()
    stream = open(path, "rb")
    # chiave pubblica del mittente chiave privata del destinatario
    decrypted_data = gpg.decrypt_file(
        stream, passphrase=passphrase, output=decrypted_folder_path + filename + ".verified")
    stream.close()
    print(decrypted_data.status)
    print(decrypted_data.valid)
    print(decrypted_data.stderr)
