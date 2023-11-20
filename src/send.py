import pika 
import json

def send_payload_user(user):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='user')

        channel.basic_publish(exchange='',
                            routing_key='user',
                            body= json.dumps(user))
        
        print(json.dumps(user))
        connection.close()
        return 'success'
    except:
        return "failed"
    
def send_payload_pets(pets):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='pets')

        channel.basic_publish(exchange='',
                            routing_key='pets',
                            body= json.dumps(pets))
        
        print(json.dumps(pets))
        connection.close()
        return 'success'
    except:
        return "failed"
    
def send_payload_exams(exams):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='exams')

        channel.basic_publish(exchange='',
                            routing_key='exams',
                            body= json.dumps(exams))
        
        print(json.dumps(exams))
        connection.close()
        return 'success'
    except:
        return "failed"
    
def send_payload_medicineVaccine(medicineVaccine):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='medicineVaccine')

        channel.basic_publish(exchange='',
                            routing_key='medicineVaccine',
                            body= json.dumps(medicineVaccine))
        
        print(json.dumps(medicineVaccine))
        connection.close()
        return 'success'
    except:
        return "failed"