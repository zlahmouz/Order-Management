import pika
import time
import ast

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Déclarer les files d'attente
channel.queue_declare(queue='order_queue', durable=True)
channel.queue_declare(queue='status_queue', durable=True)


def callback(ch, method, properties, body):
    # Convertir le message en dictionnaire
    order = ast.literal_eval(body.decode())
    order_id = order['order_id']
    items = order['items']
    print(f"[Chef] Préparation de la commande {order_id} avec {items} items.")

    # Simuler le temps de préparation en fonction du nombre d'items
    preparation_time = items * 3
    time.sleep(preparation_time)

    # Envoyer un statut de commande prête
    status_message = f"Commande {order_id} est prête."
    channel.basic_publish(
        exchange='',
        routing_key='status_queue',
        body=status_message,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"[Chef] {status_message}")

    # Accuser réception du message
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Activer l’écoute des commandes
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='order_queue', on_message_callback=callback)

print(' [*] En attente des commandes en cuisine. Appuyez sur CTRL+C pour quitter.')
channel.start_consuming()
