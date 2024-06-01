import tkinter as tk
from tkinter import simpledialog, messagebox
from startdb import start
from silent_mode import stampa_notifica
from datetime import datetime

# Configurazione di Redis
r = start()

# Funzione di registrazione
def registrazione(nome_utente, password):
    if r.hexists('users', nome_utente):
        messagebox.showinfo("Errore", "User already exists")
        return False
    user_key = f'user:{nome_utente}'
    r.hset(user_key, 'password', password)
    r.hset(user_key, 'voted', 'False')
    messagebox.showinfo("Successo", "Utente registrato")
    return True

# Funzione di login
def login(username, password):
    user_key = f'user:{username}'
    if not r.exists(user_key):
        messagebox.showinfo("Errore", "Invalid credentials")
        return False
    stored_password = r.hget(user_key, 'password')
    if stored_password != password:
        messagebox.showinfo("Errore", "Invalid credentials")
        return False
    r.set(f'user_session:{username}', 'logged_in')
    messagebox.showinfo("Successo", "Login successful")
    return True

# Funzione di logout
def logout(username):
    r.delete(f'user_session:{username}')
    messagebox.showinfo("Successo", "Logout successful")

# Funzione per aggiungere un contatto
def aggiungi_contatto(username, contatto):
    rubrica_key = f'rubrica:{username}'
    r.sadd(rubrica_key, contatto)

# Funzione per visualizzare la rubrica
def visualizza_rubrica(username):
    rubrica_key = f'rubrica:{username}'
    contatti = r.smembers(rubrica_key)
    if contatti:
        contatti_str = "\n".join(contatti)
        messagebox.showinfo("Rubrica", f"Contatti:\n{contatti_str}")
    else:
        messagebox.showinfo("Rubrica", "Rubrica vuota")

# Funzione per gestire la rubrica
def gestisci_rubrica(username):
    while True:
        root = tk.Tk()
        root.withdraw()
        scelta = simpledialog.askstring("Gestione della rubrica",
                                        "1. Aggiungi contatto\n2. Visualizza rubrica\n3. Torna al menu precedente",
                                        parent=root)

        if scelta == "1":
            contatto = simpledialog.askstring("Aggiungi contatto", "Inserisci il nome del contatto da aggiungere:", parent=root)
            if contatto:
                aggiungi_contatto(username, contatto)
                messagebox.showinfo("Successo", "Contatto aggiunto con successo.")
        elif scelta == "2":
            visualizza_rubrica(username)
        elif scelta == "3":
            break
        else:
            messagebox.showinfo("Errore", "Scelta non valida, riprova.")

# Funzione per inviare un messaggio
def send_message(username):
    rubrica_key = f'rubrica:{username}'
    contatti = r.smembers(rubrica_key)
    if not contatti:
        messagebox.showinfo("Errore", "/Rubrica vuota. Aggiungi un contatto prima di inviare un messaggio.")
        return
    
    root = tk.Tk()
    root.withdraw()
    contatto = simpledialog.askstring("Invia Messaggio", f"Scegli il contatto:\n{list(contatti)}", parent=root)
    if contatto in contatti:
        message = simpledialog.askstring("Invia Messaggio", "Inserisci il messaggio:", parent=root)
        if message:
            message_id = r.incr('message_id')
            message_key = f'message:{message_id}'
            r.hset(message_key, 'username', username)
            r.hset(message_key, 'message', message)
            r.hset(message_key, 'recipient', contatto)
            r.hset(message_key, 'timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            messagebox.showinfo("Successo", "Message sent successfully")
    else:
        messagebox.showinfo("Errore", "Contatto non trovato nella rubrica.")

# Funzione per recuperare i messaggi
def get_messages(username):
    root = tk.Tk()
    root.withdraw()
    rubrica_key = f'rubrica:{username}'
    contatti = r.smembers(rubrica_key)
    contatto = simpledialog.askstring("Invia Messaggio", f"Scegli il contatto:\n{list(contatti)}", parent=root)
    message_keys = r.keys('message:*')
    if not message_keys:
        messagebox.showinfo("Messaggi", "Nessun messaggio trovato")
        return

    messaggi = []
    for key in message_keys:
        message_data = r.hgetall(key)
        recipient = message_data.get('recipient', 'Sconosciuto')
        timestamp = message_data.get('timestamp', 'Data non disponibile')
        messaggi.append(f"ID: {key.split(':')[-1]}, User: {message_data['username']}, Message: {message_data['message']}, Recipient: {recipient}, Timestamp: {timestamp}")
    
    messaggi_str = "\n\n".join(messaggi)
    messagebox.showinfo("Messaggi", messaggi_str)

def ricezione_messaggio(user_hash):
    # Codice per la ricezione dei messaggi in tempo reale 
    pubsub = r.pubsub()
    pubsub.subscribe(f'chat:{user_hash}:*', f'chat:*:{user_hash}')
    for message in pubsub.listen():
        if message['type'] == 'message':
            channel = message['channel'].decode('utf-8')
            _, sender_hash, recipient_hash = channel.split(':')
            if sender_hash == user_hash:
                sender_hash, recipient_hash = recipient_hash, sender_hash
            stampa_notifica(sender_hash, recipient_hash, message['data'].decode('utf-8'))


            

def main():
    root = tk.Tk()
    root.withdraw()
    root.geometry("500x500")
    while True:
        scelta = simpledialog.askstring("Benvenuto!", "Cosa vuoi fare?\n1. Registrati\n2. Accedi\n3. Esci", parent=root)

        if scelta == "1":
            while True:
                nome_utente = simpledialog.askstring("Registrati", "Inserisci il tuo username:", parent=root)
                if r.hexists('users', nome_utente):
                    messagebox.showinfo("Errore", "Nome utente già utilizzato, inseriscine un altro.")
                else:
                    break
            password = simpledialog.askstring("Registrati", "Inserisci la tua password:", parent=root)
            if nome_utente and password:
                registrazione(nome_utente, password)
        elif scelta == "2":
            username = simpledialog.askstring("Accedi", "Inserisci il tuo username:", parent=root)
            password = simpledialog.askstring("Accedi", "Inserisci la tua password:", parent=root)
            if username and password and login(username, password):
                while True:
                    sub_scelta = simpledialog.askstring("Azioni disponibili", "1. Logout\n2. Invia Messaggio\n3. Visualizza Messaggi\n4. Gestisci Rubrica", parent=root)
                    
                    if sub_scelta == "1":
                        logout(username)
                        break
                    elif sub_scelta == "2":
                        send_message(username)
                    elif sub_scelta == "3":
                        get_messages(username)
                    elif sub_scelta == "4":
                        gestisci_rubrica(username)
                    else:
                        messagebox.showinfo("Errore", "Scelta non valida, riprova.")
        elif scelta == "3":
            messagebox.showinfo("Arrivederci!", "Arrivederci!")
            break
        else:
            messagebox.showinfo("Errore", "Scelta non valida, riprova.")

if __name__ == '__main__':
    main()
