import pika, json
from publish import generatePubs
from subscribe import generateSubs
from complexsubscribe import generateComplexSubs

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='simple subs')
channel.queue_declare(queue='complex subs')
channel.queue_declare(queue='filtered pubs')

channel.exchange_declare(exchange='notifications', exchange_type='fanout')
channel.queue_declare(queue='notifs', exclusive=False)
channel.queue_bind(exchange='notifications', queue='notifs')

notifs = open('results/notifs.txt', 'a')
prev_notifs = open('results/notifs.txt', 'r')

def callback(ch, method, properties, body):
    print(prev_notifs.read())
    if body.decode() == 'stop':
        channel.stop_consuming()
    else:
        notifs.write(body.decode())
        print("Received message:", body.decode())
        
def get_selected_pubs(ch, method, properties, body):
    channel.stop_consuming()
    with open('results/filtered_pubs.json', 'w')as f:
        f.write(body.decode())

while (True):
    command = input("Choose a command:")
    if command == 'simple sub':
        nr_subs = int(input("Number of simple subs to be generated:"))
        simple_subs = generateSubs(nr_subs)
        
        channel.basic_publish(exchange='', routing_key='simple subs', body=json.dumps(simple_subs, indent=1))
        print("Subscriptions sent to broker successfully")
        
        channel.basic_consume(queue='filtered pubs', on_message_callback=get_selected_pubs, auto_ack=True)
        channel.start_consuming()
        print("Selected publications successfully arrived - see it on filtered pubs file")
        
    elif command == 'complex sub':
        complex_subs = {}
        nr_subs = int(input("Number of complex subs to be generated:"))
        complex_subs = generateComplexSubs(nr_subs)
        
        channel.basic_publish(exchange='', routing_key='complex subs', body=json.dumps(simple_subs, indent=1))
        print("Complex subscriptions sent to broker successfully")
        
        channel.basic_consume(queue='filtered pubs', on_message_callback=get_selected_pubs, auto_ack=True)
        channel.start_consuming()
        print("Selected publications successfully arrived - see it on filtered pubs file")
        
    elif command == 'notifs':
        channel.basic_publish(exchange='', routing_key='notifs', body='stop')
        channel.basic_consume(queue='notifs', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
        
    elif command == 'quit':
        connection.close()
        break
    
    else:
        print("Incorrect command, here's some help: \
              \n 'simple sub' - add a simple subscription \
              \n 'complex sub' - add a complex subscription \
              \n 'notifs' - see notifications from publishers and brokers \
              \n 'quit' - exit the server")