from tkinter import Tk, Label, Entry, Text, Button, END, messagebox, filedialog
import imghdr
import smtplib
import ssl
from email.message import EmailMessage
import os
from datetime import datetime

# Ülemaailmne muutuja lisatud failide teekondade salvestamiseks
root = Tk()
root.title("E-kirja saatmine")

files = []

Label(root, text="EMAIL (komadega):").pack()
email_box = Entry(root, width=60)
email_box.pack()

Label(root, text="TEEMA:").pack()
teema_box = Entry(root, width=60)
teema_box.pack()

Label(root, text="TEKST:").pack()
kiri_box = Text(root, width=60, height=10)
kiri_box.pack()

Label(root, text="ALLKIRI:").pack()
allkiri_box = Entry(root, width=60)
allkiri_box.pack()

# Märgistus manuste arvu kuvamiseks
l_lisatud = Label(root, text="Lisa: (faile pole valitud)")
l_lisatud.pack()

# Valige mitu faili
def vali_pilt():
    global files
    files=filedialog.askopenfilenames()
    if files:
        l_lisatud.configure(text=f"Lisatud failid: {len(files)}")


def saada_kiri():
    kellele_raw=email_box.get().strip() #from Entry
    teematekst = teema_box.get().strip()
    kiri=kiri_box.get("1.0", END).strip() #from Text
    allkiri = allkiri_box.get().strip()

    # Kohustuslike väljade kontrollimine
    if not kellele_raw or not kiri:
        messagebox.showerror("Viga", "Palun sisestage saajad ja kiri.")
        return

    # Toetus mitmele e-posti aadressile, mis on eraldatud komadega
    kellele_list = [email.strip() for email in kellele_raw.split(",") if email.strip()]

    smtp_server="smtp.gmail.com"
    port=587
    sender_email="nikitosgoldboss@gmail.com"
    password="yfct fdko yjie khof" #Teie rakenduse võti

    # Lisa e-kirja lõppu allkiri
    full_kiri = f"{kiri}\n\n--\n{allkiri}"

    msg=EmailMessage()
    msg.set_content(full_kiri)   
    msg['Subject']= teematekst or "E-kiri saatmine"
    msg['From']="Marina Oleinik"
    msg['To']= ", ".join(kellele_list)

    # Kõigi valitud failide kinnitamine
    for f in files:
        try:
            with open(f, 'rb') as fp:
                sisu = fp.read()
            ext = imghdr.what(None, sisu) or "octet-stream"
            msg.add_attachment(sisu, maintype='image', subtype=ext, filename=os.path.basename(f))
        except Exception as e:
            messagebox.showerror("Manuse viga", f"{os.path.basename(f)}: {e}")
            return


    try:
        context = ssl.create_default_context()
        server=smtplib.SMTP(smtp_server, port)
        server.starttls(context=context)
        server.login(sender_email, password)
        server.send_message(msg)
        messagebox.showinfo("Informatsioon", "Kiri saadeti edukalt")

        # E-kirja salvestamine logifaili
        with open("logs.txt", "a", encoding="utf-8") as log:
            log.write(f"{datetime.now()}\nSaajad: {msg['To']}\nTeema: {msg['Subject']}\nSisu:\n{full_kiri}\n{'-'*40}\n")

    except Exception as e:
        messagebox.showerror("Saatmise viga", str(e))
    finally:
        try:
            server.quit()
        except:
            pass

Button(root, text="LISA FAILID", command=vali_pilt).pack(pady=5)
Button(root, text="SAADA", command=saada_kiri).pack(pady=5)

root.mainloop()
