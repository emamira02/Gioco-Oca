import redis
from builtins import print
from startdb import start

# Configurazione di Redis
# Creiamo un'istanza del client Redis collegandolo al server Redis locale sulla porta predefinita 6379 e utilizzando il database 0
redis_client = start()

# Funzione di registrazione
def registrazione(nome_utente, password):
    # Controlla se l'utente esiste già
    if redis_client.hexists('users', nome_utente):
        print("User already exists")
        return
# Crea una chiave utente con il formato 'user:username'
    user_key = f'user:{nome_utente}'
# Memorizza la password e lo stato di 'voted' (votato) come campi hash per l'utente
    redis_client.hset(user_key, 'password', password)
    redis_client.hset(user_key, 'voted', 'False')
    print("Utente registrato")

# Funzione di login
def login(username, password):
# Crea una chiave utente con il formato 'user:username'
    user_key = f'user:{username}'
# Controlla se la chiave utente esiste nel database
    if not redis_client.exists(user_key):
        print("Invalid credentials")
        return
# Recupera la password memorizzata per l'utente
    stored_password = redis_client.hget(user_key, 'password')
# Verifica se la password fornita corrisponde a quella memorizzata
    if stored_password != password:
        print("Invalid credentials")
        return

# Imposta lo stato di login per l'utente memorizzando una chiave di sessione
    redis_client.set(f'user_session:{username}', 'logged_in')
    print("Login successful")

# Funzione di logout
def logout(username):
# Elimina la chiave di sessione dell'utente per effettuare il logout
    redis_client.delete(f'user_session:{username}')
    print("Logout successful")

# Funzione per inviare un messaggio
def send_message(username, message):
# Controlla se l'utente è loggato verificando l'esistenza della chiave di sessione
    if not redis_client.exists(f'user_session:{username}'):
        print("User not logged in")
        return
# Incrementa l'ID del messaggio per ottenere un nuovo ID unico
    message_id = redis_client.incr('message_id')
# Crea una chiave di messaggio con il formato 'message:message_id'
    message_key = f'message:{message_id}'
# Memorizza il nome utente e il messaggio come campi hash per il messaggio
    redis_client.hset(message_key, 'username', username)
    redis_client.hset(message_key, 'message', message)
    print("Message sent successfully")

# Funzione per recuperare i messaggi
def get_messages():
    message_keys = redis_client.keys('message:*')
    for key in message_keys:
        message_data = redis_client.hgetall(key)
        print(f"ID: {key.split(':')[-1]}, User: {message_data['username']}, Message: {message_data['message']}")

# Funzione principale per l'interfaccia a riga di comando
def main():
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Logout")
        print("4. Send Message")
        print("5. Get Messages")
        print("6. Exit")
        choice = input("Enter your choice: ")

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



    




    
