from kafka import KafkaProducer
import json
import time
import uuid
import random as rd

def post_kafka() :
    producer = KafkaProducer(
    bootstrap_servers = ["172.23.152.231:9092"]
    )
    print('='*60)
    print('=== Post data realtime ===')
    print('='*60)
    with open("../data/OnePiece.json" , "r" , encoding = 'utf-8') as f :
        num = 1
        for line in f :
            if line.strip() :
                data = json.loads(line.strip())
    for d in data :        
        print("=== Start send message ===")
        producer.send('one-piece' , key = bytes(str(uuid.uuid4()) , 'utf-8') , value = bytes(json.dumps(d) , 'utf-8'))
        print(f"[{time.strftime('%H:%M:%S')}] Send data {num} successfully ")
        num+=1
        time.sleep(rd.randint(1, 2))
    producer.flush()
    producer.close()
if __name__ == "__main__" :
    while True :
        post_kafka()