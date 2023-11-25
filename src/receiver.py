import pika, json
from models import session, User, Pets, Exams, MedicineVaccine
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

def send_db(args):
    try:
        url = URL.create(
            drivername='postgresql+psycopg2',
            username='postgres',
            password='banco',
            host='postgres',
            database='bestfriend',
            port=5432
        )

        engine = create_engine(url)
        Session = sessionmaker(bind=engine)
        session = Session()

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()


        print("Consumer started...")

        class_type = args

        def callback(ch, method, properties, body):
            print('Received message:')
            dados_mensagem = json.loads(body.decode())
            print(dados_mensagem)

            if (class_type == 'users'):
                new_user = User(
                    name = dados_mensagem.get('name'),
                    email = dados_mensagem.get('email'),
                    password = dados_mensagem.get('password')
                )
                session.add(new_user)
                session.commit()

                connection.close()

            if(class_type == 'pets'):
                new_pet = Pets(
                    user_id = dados_mensagem.get('user_id'),
                    name = dados_mensagem.get('name'),
                    years_old = dados_mensagem.get('years_old'),
                    weight = dados_mensagem.get('weight')
                )
                session.add(new_pet)
                session.commit()

                connection.close()

            if (class_type == 'exams'):
                new_exam = Exams(
                    pet_id = dados_mensagem.get('pet_id'),
                    place = dados_mensagem.get('place'),
                    name_exam = dados_mensagem.get('name_exam'),
                    date = dados_mensagem.get('date'),
                )
                session.add(new_exam)
                session.commit()

                connection.close()

            if(class_type == 'medVacc'):
                new_medvacc = MedicineVaccine(
                    pet_id = dados_mensagem.get('pet_id'),
                    type_of = dados_mensagem.get('type_of'),
                    name = dados_mensagem.get('name'),
                    date = dados_mensagem.get('date'),
                )
                session.add(new_medvacc)
                session.commit()

                connection.close()


        while True:
            if (class_type == 'users'):
                method_frame, header_frame, body = channel.basic_get(queue='user',auto_ack=True)

                if method_frame:
                    callback(None, method_frame, None, body)
                    break
            if(class_type == 'pets'):
                method_frame, header_frame, body = channel.basic_get(queue='pets',auto_ack=True)

                if method_frame:
                    callback(None, method_frame, None, body)
                    break
            if(class_type == 'exams'):
                method_frame, header_frame, body = channel.basic_get(queue='exams',auto_ack=True)

                if method_frame:
                    callback(None, method_frame, None, body)
                    break
            if(class_type == 'medVacc'):
                method_frame, header_frame, body = channel.basic_get(queue='medicineVaccine',auto_ack=True)

                if method_frame:
                    callback(None, method_frame, None, body)
                    break

        #usado para escuta continua
        #channel.basic_consume(queue='aluno', on_message_callback=callback, auto_ack=True)
        #channel.start_consuming()
        

    except Exception as e:
        print(f"Error: {e}")


