import redis
from builtins import print
from startdb import start
from silent_mode import stampa_notifica

# Configurazione di Redis
# Creiamo un'istanza del client Redis collegandolo al server Redis locale sulla porta predefinita 6379 e utilizzando il database 0
r = start()

# Funzione di registrazione
def registrazione(nome_utente, password):
    # Controlla se l'utente esiste già
    if r.hexists('users', nome_utente):
        print("User already exists")
        return
# Crea una chiave utente con il formato 'user:username'
    user_key = f'user:{nome_utente}'
# Memorizza la password e lo stato di 'voted' (votato) come campi hash per l'utente
    r.hset(user_key, 'password', password)
    r.hset(user_key, 'voted', 'False')
    print("Utente registrato")

# Funzione di login
def login(username, password):
# Crea una chiave utente con il formato 'user:username'
    user_key = f'user:{username}'
# Controlla se la chiave utente esiste nel database
    if not r.exists(user_key):
        print("Invalid credentials")
        return
# Recupera la password memorizzata per l'utente
    stored_password = r.hget(user_key, 'password')
# Verifica se la password fornita corrisponde a quella memorizzata
    if stored_password != password:
        print("Invalid credentials")
        return

# Imposta lo stato di login per l'utente memorizzando una chiave di sessione
    r.set(f'user_session:{username}', 'logged_in')
    print("Login successful")

# Funzione di logout
def logout(username):
# Elimina la chiave di sessione dell'utente per effettuare il logout
    r.delete(f'user_session:{username}')
    print("Logout successful")

# Funzione per inviare un messaggio
def send_message(username, message):
# Controlla se l'utente è loggato verificando l'esistenza della chiave di sessione
    if not r.exists(f'user_session:{username}'):
        print("User not logged in")
        return
# Incrementa l'ID del messaggio per ottenere un nuovo ID unico
    message_id = r.incr('message_id')
# Crea una chiave di messaggio con il formato 'message:message_id'
    message_key = f'message:{message_id}'
# Memorizza il nome utente e il messaggio come campi hash per il messaggio
    r.hset(message_key, 'username', username)
    r.hset(message_key, 'message', message)
    print("Message sent successfully")

# Funzione per recuperare i messaggi
def get_messages():
    message_keys = r.keys('message:*')
    for key in message_keys:
        message_data = r.hgetall(key)
        print(f"ID: {key.split(':')[-1]}, User: {message_data['username']}, Message: {message_data['message']}")

def ricezione_messaggio(user_hash):
    # Codice per la ricezione dei messaggi in tempo reale (già implementato in precedenza)
    pubsub = r.pubsub()
    pubsub.subscribe(f'chat:{user_hash}:*', f'chat:*:{user_hash}')
    for message in pubsub.listen():
        if message['type'] == 'message':
            channel = message['channel'].decode('utf-8')
            _, sender_hash, recipient_hash = channel.split(':')
            if sender_hash == user_hash:
                sender_hash, recipient_hash = recipient_hash, sender_hash
            stampa_notifica(sender_hash, recipient_hash, message['data'].decode('utf-8'))

# Dizionario delle azioni per il menu principale
azioni_principali = {
    '1': 'Registrati',
    '2': 'Accedi',
    '3': 'Esci'
}

# Dizionario delle azioni per il menu dopo il login
azioni_secondarie = {
    '1': 'Logout',
    '2': 'Invia Messaggio',
    '3': 'Visualizza Messaggi'
}

def stampa_azioni(azioni):
    for key, value in azioni.items():
        print(f"{key}. {value}")

def main():
    while True:
        print("Benvenuto! Cosa vuoi fare?")
        stampa_azioni(azioni_principali)

        scelta = input("Inserisci il numero della tua scelta: ")

        if scelta == "1":
            nome_utente = input("Inserisci il tuo username: ")
            password = input("Inserisci la tua password: ")
            registrazione(nome_utente, password)
        elif scelta == "2":
            username = input("Inserisci il tuo username: ")
            password = input("Inserisci la tua password: ")
            if login(username, password):
                while True:
                    print("\nAzioni disponibili:")
                    stampa_azioni(azioni_secondarie)
                    sub_scelta = input("Inserisci il numero della tua scelta: ")

                    if sub_scelta == "1":
                        logout(username)
                        break
                    elif sub_scelta == "2":
                        message = input("Inserisci il messaggio: ")
                        send_message(username, message)
                    elif sub_scelta == "3":
                        get_messages()
                    else:
                        print("Scelta non valida, riprova.")
        elif scelta == "3":
            print("Arrivederci!")
            break
        else:
            print("Scelta non valida, riprova.")

if __name__ == '__main__':
    main()


    




    
