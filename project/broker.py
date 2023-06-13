import pika, json
from datetime import datetime
from matching import generateMatchingOneSubscription, generateMatchingOneComplexSubscription

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='simple subs')
channel.queue_declare(queue='complex subs')
channel.queue_declare(queue='filtered pubs')

channel.exchange_declare(exchange='broker_notifs', exchange_type='fanout')
channel.queue_declare(queue='notifs', exclusive=False)
channel.queue_bind(exchange='broker_notifs', queue='notifs')

def callback(ch, method, properties, body):
    print("Received notification:", body.decode())
    
with open('results/publications.json') as f:
    publications = json.load(f)
    
# with open('results/subscriptions.json') as f:
#     subscriptions = json.load(f)
f = open('results/subscription.json', 'w')
    
def get_subs(ch, method, properties, body):
    # channel.stop_consuming()
    with open('results/subscription.json', 'w')as f:
        f.write(body.decode())
        
def get_complex_subs(ch, method, properties, body):
    # channel.stop_consuming()
    with open('results/complexsubscription.json', 'w')as f:
        f.write(body.decode())

# channel.basic_publish(exchange='notifications', routing_key='', body='A broker node has filtered the collection of pubs.')

# connection.close()

selected_subs = {}

while(True):
    command = input("Choose a command:")
    if command == 'simple filter':
        
        channel.basic_consume(queue='simple sub ack', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
        
        selected_pubs = []
        
        channel.basic_consume(queue='simple subs', on_message_callback=get_subs, auto_ack=True)
        channel.start_consuming()
        
        selected_subs = json.loads(open('results/subscription.json', 'r').read())
        
        for sub in selected_subs:
            selected_pubs.append(generateMatchingOneSubscription(sub, publications))
            
        print("Publications filtered successfully")
        channel.basic_publish(exchange='notifications', routing_key='', body='{} : A broker node has filtered the collection of pubs.\n'.format(datetime.now()))
        channel.basic_publish(exchange='', routing_key='filtered pubs', body=json.dumps(selected_pubs, indent=1))
    
    elif command == 'complex filter':
        
        selected_pubs = []
        
        channel.basic_consume(queue='complex subs', on_message_callback=get_complex_subs, auto_ack=True)
        channel.start_consuming()
        
        selected_subs = json.loads(open('results/complexsubscription.json', 'r').read())
        
        for sub in selected_subs:
            selected_pubs.append(generateMatchingOneComplexSubscription(sub, publications))
            
        print("Publications filtered successfully")
        channel.basic_publish(exchange='notifications', routing_key='', body='{} : A broker node has filtered the collection of pubs.\n'.format(datetime.now()))
        channel.basic_publish(exchange='', routing_key='filtered pubs', body=json.dumps(selected_pubs, indent=1))
        
    elif command == 'quit':
        print("Broker exiting the server...")
        connection.close()
        break
    
    else:
        print("Incorrect command, here's some help: \
              \n 'filter' - select a subscription and filter the publications by the sub's details \
              \n 'quit' - exit the server")
        