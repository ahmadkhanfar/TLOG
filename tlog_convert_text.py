
from pymavlink import mavutil
 
# Open the TLOG file

mavlog = mavutil.mavlink_connection('flight1.tlog')
 
# Extract the MAVLink messages

messages = []

while True:

    msg = mavlog.recv_match()

    if not msg:

        break

    messages.append(msg)
 
# Optional: Save the messages to a text file or other format for use with ESP32

with open('mavlink_messages.txt', 'w') as f:

    for msg in messages:

        f.write(str(msg) + '\n')

 
