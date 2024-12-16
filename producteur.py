import pika
import random
import time
import uuid

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Déclarer la file des commandes
channel.queue_declare(queue='order_queue', durable=True)

# Créer des commandes aléatoires
def create_order():
    order_id = str(uuid.uuid4())  # ID unique pour chaque commande
    items = random.randint(1, 5)  # Nombre d'items dans la commande
    order = {
        'order_id': order_id,
        'items': items
    }
    return order

# Envoyer des commandes
for _ in range(10):
    order = create_order()
    channel.basic_publish(
        exchange='',
        routing_key='order_queue',
        body=str(order),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Message persistant
        ))
    print(f"[Serveur] Commande envoyée : {order}")
    time.sleep(2)  # Simule le temps entre les commandes

connection.close()
