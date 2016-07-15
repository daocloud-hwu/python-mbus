#!/usr/bin/env python

import sys
import mbus

topic = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

client = mbus.connect('192.168.3.50', 5672)
client.publish(topic, message)

print(" [x] Sent %r:%r" % (topic, message))
client.close()
