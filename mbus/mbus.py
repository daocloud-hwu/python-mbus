#!/usr/bin/env python

import pika

def connect(host='localhost', port=5672):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, port=port)
    )
    channel = connection.channel()
    channel.exchange_declare(exchange='daocloud', type='topic', durable=True)
    return Mbus(connection, channel)

class Mbus:
    def __init__(self, connection, channel):
        self.conn = connection
        self.chan = channel
        self.queue = None
        self.handlers = {}

    def close(self):
        self.conn.close()

    def subscribe(self, topic, cb):
        if self.queue is None:
            result = self.chan.queue_declare(exclusive=True)
            self.queue = result.method.queue

        self.chan.queue_bind(
            exchange='daocloud',
            queue=self.queue,
            routing_key=topic
        )
        self.handlers[topic] = cb

    def unsubscribe(self, topic):
        if self.queue is None:
            return

        self.chan.queue_unbind(
            exchange='daocloud',
            queue=self.queue,
            routing_key=topic
        )
        del self.handlers[topic]

    def start_consuming(self):
        if self.queue is None:
            result = self.chan.queue_declare(exclusive=True)
            self.queue = result.method.queue

        def process(ch, method, properties, body):
            if method.routing_key not in self.handlers:
                return
            self.handlers[method.routing_key](body)

        self.chan.basic_consume(process, queue=self.queue, no_ack=True)
        self.chan.start_consuming()

    def publish(self, topic, message):
        self.chan.basic_publish(
            exchange='daocloud',
            routing_key=topic,
            body=message
        )
