from websocket import create_connection
ws = create_connection("ws://192.168.0.101:8080")
print("Sending 'Hello World'...")
ws.send("Hello world")
print("Sent")
print("Receving")
result = ws.recv()
print("Received: '%s'" % result)
ws.close()
