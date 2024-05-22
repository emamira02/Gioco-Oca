from flask import Flask, request, jsonify
from flask_socketio import SocketIO, join_room, leave_room, send
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import redis
import json
import uuid


# Configurazione di Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def registrazione():
    data = request.get_json()
    nome_utente = data['nome_utente']
    password = data['password']
    
    if redis_client.hexists('user', nome_utente):
        return jsonify({"message": "User already exists"}), 400
    user_data = {
        'password': password,
        'voted': False
    }
    redis_client.hset('users', nome_utente, json.dumps(user_data))
    return jsonify({"message": "User registered successfully"}), 201

def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if not redis_client.hexists('users', username):
        return jsonify({"message": "Invalid credentials"}), 401
    #Recupera i dati dell'utente memorizzati in Redis sotto la chiave username
    #json.load: Converte la stringa JSON recuperata da Redis in un dizionario Python
    user_data = json.loads(redis_client.hget('users', username))
    #verifica della password
    if user_data['password'] != password:
        return jsonify({"message": "Invalid credentials"}), 401
    #Confronto la password fornita dall'utente (password) con la password memorizzata nel dizionario user_data
    #Se non coincidono restituisce una risposta JSON con un messaggio di errore e lo stato HTTP 401 (Unauthorized)
    
    # Salvare lo stato di login nel Redis
    redis_client.set(f'user_session:{username}', 'logged_in')
    return jsonify({"message": "Login successful"}), 200

    #disconnessione dell'utente dal sistema 
def logout():
    username = request.json.get('username')
    redis_client.delete(f'user_session:{username}')
    #elimina la chiave nomeutente da redis che viene utilizzata per memorizzare lo stato di login dell'utente
    return jsonify({"message": "Logout successful"}), 200



    




    
