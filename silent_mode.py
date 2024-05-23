import redis as r
import time 
from startdb import start

r = start()
print(r.ping())


def invio_messaggio(sender_hash, recipient_hash, messaggio):
    timestamp = int(time.time())
    r.zadd(f'notifications:{recipient_hash}', {messaggio: timestamp})
    r.publish(f'chat:{sender_hash}:{recipient_hash}', messaggio)
    r.publish(f'chat:{recipient_hash}:{sender_hash}', messaggio)
    if r.hget(f'person:{recipient_hash}', 'notification_enabled') == '1':
        stampa_notifica(sender_hash, recipient_hash, messaggio)


def stampa_notifica(sender_hash, recipient_hash, messaggio):
    print(f"Nuova notifica per {recipient_hash}:")
    print(f"Messaggio da {sender_hash}:")
    print(messaggio)
    print("-" * 50)


def ricezione_messaggio(user_hash):
    # Questo è il codice che il client dovrebbe eseguire in un loop per ricevere i messaggi in tempo reale
    pubsub = r.pubsub() #Crea un'istanza di PubSub di Redis. Questo ci permetterà di sottoscriverci ai canali di pub/sub per ricevere i messaggi in tempo reale.
    pubsub.subscribe(f'chat:{user_hash}:*', f'chat:*:{user_hash}') #cioè tutti i canali di chat in cui l'utente user_hash è il mittente, #tutti i canali di chat in cui l'utente user_hash è il destinatario
    for message in pubsub.listen(): #Avvia un loop che rimane in ascolto sui canali a cui ci siamo sottoscritti. Ogni volta che arriva un messaggio, il loop lo elabora
        if message['type'] == 'message':
            channel = message['channel'].decode('utf-8')
            _, sender_hash, recipient_hash = channel.split(':')
            if sender_hash == user_hash:
                sender_hash, recipient_hash = recipient_hash, sender_hash
            stampa_notifica(sender_hash, recipient_hash, message['data'].decode('utf-8'))


def silent_mode(hash_persona, mode):
    #hash_persona = codice identificativo di una persona
    #mode on: modalità silenziosa attiva;
    #mode off: modalità silenziosa disattivata

    if mode:
        #attiva modalità silenziosa
        r.hset(f'utente: {hash_persona}', 'ricezione_messaggi', 1)
        print(f"Notifica dei messaggi attivata per l'utente: {hash_persona}")
    else: 
        #disattiva modalità silenziosa 
        r.hset(f'person: {hash_persona}', 'ricezione_messaggi', 0)
        print(f"Notifica dei messaggi disattivata per l'utente: {hash_persona}")



