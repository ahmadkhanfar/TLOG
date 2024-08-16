This repository is still under testing. Please let me know if there are any errors during compilation or execution.

After successfully creating a simulated trip using Mission Planner, you will need to extract the MAVLink messages from the TLOG file.

Convert from TLOG file to Text:

Use tlogconvert.py. Ensure you have installed the pymavlink library. You can install it using pip install pymavlink.
Specify the log file name; in our case, it's test.log.
Run the program, and you will notice that a test.txt file is generated and saved in your directory.
Convert from Text (JSON output) to MAVLink and upload it to ESP32:

Open messagetoMavlink.py and modify the SSID, password, and the UDP IP address (your laptop's IP address).
Ensure the input example field matches the text file name you have.
Run the program, and you will have your Arduino file ready to be uploaded!
Ahmad Khanfar
