import pika
from publish import generatePubs
from datetime import datetime


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='publisher_notif', exchange_type='fanout')
# channel.queue_declare(queue='pub_queue')

generatePubs(10000)

channel.basic_publish(exchange='publisher_notif', routing_key='', body='{} : A publisher node has updated the set of pubs.\n'.format(datetime.now()))

connection.close()
