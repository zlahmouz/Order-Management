import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Déclarer la file d'attente des statuts
channel.queue_declare(queue='status_queue', durable=True)

def callback(ch, method, properties, body):
    status_message = body.decode()
    print(f"[Superviseur] Notification de statut reçue : {status_message}")

# Activer l’écoute des statuts
channel.basic_consume(queue='status_queue', on_message_callback=callback, auto_ack=True)

print(" [*] En attente des statuts de commande. Appuyez sur CTRL+C pour quitter.")
channel.start_consuming()
