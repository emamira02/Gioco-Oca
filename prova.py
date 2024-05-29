import redis
from builtins import print
from startdb import start
from silent_mode import *
from silent_mode import *

r = start()

def registrazione(nome_utente, password):
    if r.hexists('users', nome_utente):
        print("User already exists")
        return

    user_key = f'user:{nome_utente}'
    r.hset(user_key, 'password', password)
    r.hset(user_key, 'voted', 'False')
    print("Utente registrato")

def login(username, password):
    user_key = f'user:{username}'
    if not r.exists(user_key):
        print("Nome utente non trovato inserire nuovamente le credenziali")
        return

    stored_password = r.hget(user_key, 'password')
    if stored_password != password:
        print("Password non trovata, reinserirla.")
        return

    r.set(f'user_session:{username}', 'logged_in')
    print("Accesso eseguito, benvenuto!")

def logout(username):
    r.delete(f'user_session:{username}')
    print("Sessione terminata")

def send_message(username, message):
    if not r.exists(f'user_session:{username}'):
        print("Utente non registrato")
        return

    message_id = r.incr('message_id')
    message_key = f'message:{message_id}'
    r.hset(message_key, 'username', username)
    r.hset(message_key, 'message', message)
    print("Messaggio inviato con successo")

def get_messages():
    message_keys = r.keys('message:*')
    for key in message_keys:
        message_data = r.hgetall(key)
        print(f"ID: {key.split(':')[-1]}, User: {message_data['username']}, Message: {message_data['message']}")

def ricezione_messaggio(user_hash):
    pubsub = r.pubsub()
    pubsub.subscribe(f'chat:{user_hash}:*', f'chat:*:{user_hash}')
    for message in pubsub.listen():
        if message['type'] == 'message':
            channel = message['channel'].decode('utf-8')
            _, sender_hash, recipient_hash = channel.split(':')
            if sender_hash == user_hash:
                sender_hash, recipient_hash = recipient_hash, sender_hash
            stampa_notifica(sender_hash, recipient_hash, message['data'].decode('utf-8'))

azioni_principali = {
    '1': 'Registrati',
    '2': 'Accedi',
    '3': 'Esci'
}

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
            login(username, password)
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



#-----------------------------------------------------
