#!/usr/bin/env python

import sys
import mbus

def my_print(body):
    print(" [x] %r" % (body))

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

client = mbus.connect('192.168.3.50', 5672)

for binding_key in binding_keys:
    client.subscribe(binding_key, my_print)

print(' [*] Waiting for messages. To exit press CTRL+C')

client.start_consuming()
