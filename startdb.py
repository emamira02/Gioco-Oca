import redis

#Scheletro di una funzione per collegare in automatico il database

def start():
    r = redis.Redis(
        host='redis-13587.c250.eu-central-1-1.ec2.redns.redis-cloud.com',
        port=13587,
        username="admin",
        password="Password123.",
        decode_responses=True)
    return r

if __name__ == "__main__":
    db = start()
    db.set("utente:francesco", "password")
    password = db.get("utente:francesco")
    print(password)
