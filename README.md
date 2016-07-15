# python-mbus
daocloud mbus implemented by rabbitmq, written by python

## Subscribe
    def handler(message):
        print(message)

    client = mbus.connect('localhost', 5672)
    client.subscribe('topic01', handler)
    client.start_consuming()

## Publish
    client = mbus.connect('localhost', 5672)
    client.publish('topic01', 'message01')

## Example
    Please make sure rabbitmq is installed

    python example_receive.py "a.b"
    python example_emit.py "a.b" "hello"
