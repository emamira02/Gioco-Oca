import redis

#Scheletro di una funzione per collegare in automatico il database

def start():
    r = redis.Redis(
        host='redis-13587.c250.eu-central-1-1.ec2.redns.redis-cloud.com',
        port=13587,
        username="default",
        password="UvDrJ3N7kZnlrQ1ScJ2rAl25kAdAtbvt",
        decode_responses=True)
    return r
