#copia del main per dividere gli if in più passaggi successivi con una funzione e un dizionario
#da completare

import redis
from builtins import print

# Configurazione di Redis
# Creiamo un'istanza del client Redis collegandolo al server Redis locale sulla porta predefinita 6379 e utilizzando il database 0
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

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

#Funzione che decide quali scelte si possono effettuare nello stato attuale dell'utente
def current_choices(username):

    all_choices = {'Sign up': registrazione,
                    'Login' : login,
                    'Logout': logout,
                    'Send Messagges': send_message,
                    'Get Messages': get_messages,
                    'Exit' : exit
                    }
    if not r.exists(f'user_session:{username}'):
        actions = {key:value for (key, value) in all_choices.items()}

    

def choice():
    
    choices = current_choices()

    while True:
        for index, key in enumerate(choices.keys(), start = 1):
            print(f'{index}.{key}')
        user_input = input("Enter your choice: ")

        if not user_input.isdigit():
            print("You must enter a number.")
            break
        user_input = int(user_input)
        if user_input < 1 or user_input > len(choices):
            print("Action not found, retry.")
            break

        choice = list(choices.keys())[user_input - 1]
        function = choices[choice]
        return function



# Funzione principale per l'interfaccia a riga di comando
def main():
    while True:
        


        if choice == '1':
            nome_utente = input("Enter username: ")
            password = input("Enter password: ")
            registrazione(nome_utente, password)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            login(username, password)
        elif choice == '3':
            username = input("Enter username: ")
            logout(username)
        elif choice == '4':
            username = input("Enter username: ")
            message = input("Enter message: ")
            send_message(username, message)
        elif choice == '5':
            get_messages()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()


