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
    r.hset(user_key, 'voted', '0')
    r.hset('users', nome_utente, 1)
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
def silent_mode(username, mode):
    if not mode:
        # Attiva modalità silenziosa
        r.hset(f'user:{username}', 'voted', 1)
        messagebox.showinfo("Do Not Disturb", f"Modalità silenziosa attivata per l'utente: {username}")
    else:
        # Disattiva modalità silenziosa
        r.hset(f'user:{username}', 'voted', 0)
        messagebox.showinfo("Do Disturb", f"Modalità silenziosa disattivata per l'utente: {username}")
#Funzionamento della funzione 
# Quando mode è 0, il codice esegue r.hset(f'user:{username}', 'voted', 1), che imposta il campo voted a 1 per indicare che la modalità silenziosa è attivata.
#Viene mostrato un messaggio con messagebox.showinfo("Do Not Disturb", f"Modalità silenziosa attivata per l'utente: {username}").

#disattivazione mod: Quando mode è diverso da 0 (ad esempio, 1), il codice esegue r.hset(f'user:{username}', 'voted', 0), che imposta il campo voted a 0 per indicare che la modalità silenziosa è disattivata.
#Viene mostrato un messaggio con messagebox.showinfo("Do Disturb", f"Modalità silenziosa disattivata per l'utente: {username}").

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
        contatti_str = ", ".join(contatti)
        messagebox.showinfo("Rubrica", f"Contatti: {contatti_str}")

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

            cerca_contatti = simpledialog.askstring("Cerca contatto", "Inserisci il nome (o una parte) del contatto da aggiungere:", parent=root)
            contatti = []
            for utente in r.scan_iter(f"user:*"):
                if cerca_contatti in utente:
                    contatti.append(utente)
            if contatti:
                contatti_dict = {str(n):nome[5:] for n, nome in enumerate(contatti, start=1)}
                scelta = simpledialog.askstring("Aggiunta contatto", f"Scrivi il numero del contatto che vuoi aggiungere\n{contatti_dict}", parent=root)
                try:
                    contatto = contatti_dict[scelta]
                    aggiungi_contatto(username, contatto)
                    messagebox.showinfo("Successo", "Contatto aggiunto con successo.")
                except KeyError:
                    messagebox.showinfo("Errore", "Scelta non valida, riprova.")
            else:
                messagebox.showinfo("Nessun contatto", "La ricerca non ha restituito alcun contatto")

        elif scelta == "2":
            visualizza_rubrica(username)
        elif scelta == "3":
            break
        else:
            messagebox.showinfo("Errore", "Scelta non valida, riprova.")

# Funzione per avviare una chat a tempo con un contatto
def avvia_chat_tempo(username):
    root = tk.Tk()
    root.withdraw()
    rubrica_key = f'rubrica:{username}'
    contatti = r.smembers(rubrica_key)
    if not contatti:
        messagebox.showinfo("Errore", "Rubrica vuota. Aggiungi un contatto prima di avviare una chat a tempo.")
        return

    contatto = simpledialog.askstring("Avvia Chat a Tempo", f"Scegli il contatto:\n{list(contatti)}", parent=root)
    if contatto:
        mode = int(r.hget(f'user:{contatto}', 'voted'))
        if mode:
            messagebox.showinfo("Errore", "Il contatto non vuole essere disturbato.")
            return
        chat_key = f'chat_tempo:{username}:{contatto}'
        r.set(chat_key, 'active')
        messagebox.showinfo("Successo", f"Chat a tempo con {contatto} avviata.")

# Funzione per inviare un messaggio
def send_message(username):
    rubrica_key = f'rubrica:{username}'
    contatti = r.smembers(rubrica_key)
    if not contatti:
        messagebox.showinfo("Errore", "Rubrica vuota. Aggiungi un contatto prima di inviare un messaggio.")
        return
    
    root = tk.Tk()
    root.withdraw()
    contatto = simpledialog.askstring("Invia Messaggio", f"Scegli il contatto:\n{list(contatti)}", parent=root)
    mode = int(r.hget(f'user:{contatto}', 'voted'))
    if mode:
        messagebox.showinfo("Errore", "Il contatto non vuole essere disturbato.")
        return
    elif contatto in contatti:
        message = simpledialog.askstring("Invia Messaggio", "Inserisci il messaggio:", parent=root)
        if message:
            message_id = r.incr('message_id')
            message_key = f'message:{message_id}'
            r.hset(message_key, 'username', username)
            r.hset(message_key, 'message', message)
            r.hset(message_key, 'recipient', contatto)
            r.hset(message_key, 'timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            messagebox.showinfo("Successo", "Messaggio inviato con successo")
    else:
        messagebox.showinfo("Errore", "Contatto non trovato nella rubrica.")

# Funzione per recuperare i messaggi
def compare_messages(msg1, msg2):
    timestamp1 = msg1[0]
    timestamp2 = msg2[0]
    if timestamp1 < timestamp2:
        return -1
    elif timestamp1 == timestamp2:
        return 0
    else:
        return 1

def get_messages(username):
    root = tk.Tk()
    root.withdraw()
    rubrica_key = f'rubrica:{username}'
    contatti = r.smembers(rubrica_key)
    contatto_str = ", ".join(contatti) 
    contatto = simpledialog.askstring("Visualizza Messaggi", f"Scegli il contatto:\n{contatto_str}", parent=root)
    if contatto not in contatti:
        messagebox.showinfo("Errore", "Contatto non trovato nella rubrica.")
        return
    
    message_keys = r.keys('message:*')
    if not message_keys:
        messagebox.showinfo("Messaggi", "Nessun messaggio trovato")
        return

    messaggi = []
    for key in message_keys:
        message_data = r.hgetall(key)
        sender = message_data.get('username')
        recipient = message_data.get('recipient')
        if (sender == username and recipient == contatto) or (sender == contatto and recipient == username):
            timestamp = message_data.get('timestamp', 'Data non disponibile')
            message_text = message_data.get('message', 'Messaggio non disponibile')
            messaggi.append((timestamp, sender, message_text))
    
    messaggi.sort(key=lambda x: x[0])  # Ordinamento per timestamp
    messaggi_str = "\n\n".join([f"User: {msg[1]}\nMessage: {msg[2]}\nDate: {msg[0]}" for msg in messaggi])
    
    if messaggi:
        messaggi_str = "\n\n".join(
            [f"{msg[0]}\n{msg[1]}: {msg[2]}" for msg in messaggi]
        )
        messagebox.showinfo("Messaggi", messaggi_str)
    else:
        messagebox.showinfo("Messaggi", "Nessun messaggio trovato")


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

# Funzione per gestire la chiusura della finestra principale
def on_closing():
    root.quit()
    root.destroy()

def main():
    global root
    root = tk.Tk()
    root.withdraw()
    root.geometry("500x500")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    while True:
        try:
            scelta = simpledialog.askstring("Benvenuto!", "Cosa vuoi fare?\n1. Registrati\n2. Accedi\n3. Esci", parent=root)
            if scelta is None:
                break
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
                        sub_scelta = simpledialog.askstring("Azioni disponibili", "1. Logout\n2. Invia Messaggio\n3. Visualizza Messaggi\n4. Gestisci Rubrica\n5. Modalità Silenziosa On/Off\n6. Chat a Tempo", parent=root)
                        if sub_scelta is None:
                            break
                        if sub_scelta == "1":
                            logout(username)
                            break
                        elif sub_scelta == "2":
                            send_message(username)
                        elif sub_scelta == "3":
                            get_messages(username)
                        elif sub_scelta == "4":
                            gestisci_rubrica(username)
                        elif sub_scelta == "5":
                            mode = int(r.hget(f'user:{username}', 'voted'))
                            silent_mode(username, mode)
                        elif sub_scelta == "6":
                            avvia_chat_tempo(username)
                        else:
                            messagebox.showinfo("Errore", "Scelta non valida, riprova.")
            elif scelta == "3":
                messagebox.showinfo("Arrivederci!", "Arrivederci!")
                break
            else:
                messagebox.showinfo("Errore", "Scelta non valida, riprova.")
        except tk.TclError:
            break


if __name__ == '__main__':
    main()
