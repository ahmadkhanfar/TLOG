import re


def generate_generic_mavlink_send_code(message_type, params):
    param_list = []
    for param in params.values():
        # Check if the parameter is a text string or needs quotes
        if isinstance(param, str) and not param.isdigit():
            param_list.append(f'"{param}"')
        else:
            param_list.append(f"{param}")
    param_list_str = ', '.join(param_list)
    arduino_code = f"""
    send{message_type}({param_list_str});
"""
    return arduino_code
 
 
def generate_arduino_code_from_text_file(input_text_file, output_arduino_file):
    with open(input_text_file, 'r') as f:
        lines = f.readlines()
 
    arduino_code = """
#include <WiFi.h>
#include <WiFiUDP.h>
#include <MAVLink.h>
 
// Replace with your network credentials
const char* ssid     = "TELUS9379";
const char* password = "FRxkhF5MJn35";
 
// UDP settings
WiFiUDP udp;
const char* udpAddress = "192.168.1.74";  // Replace with the IP address of the computer running Mission Planner
const int udpPort = 14550;  // Port Mission Planner listens to (default is 14550)
 
void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");
}
 
void loop() {
"""
 
    for line in lines:
        line = line.strip()
        message_type = line.split(" ")[0]
        params = extract_params(line)
 
        if message_type == "GPS_RAW_INT":
            arduino_code += f"""
    sendGPSRawInt({params["time_usec"]}, {params["fix_type"]}, {params["lat"]}, {params["lon"]}, {params["alt"]}, {params["eph"]}, {params["epv"]}, {params["vel"]}, {params["cog"]}, {params["satellites_visible"]});
    delay(100);
"""
        elif message_type == "HEARTBEAT":
            arduino_code += f"""
    sendHeartbeat({params["type"]}, {params["autopilot"]}, {params["base_mode"]}, {params["custom_mode"]}, {params["system_status"]}, {params["mavlink_version"]});
    delay(100);
"""
        else:
            arduino_code += generate_generic_mavlink_send_code(message_type, params)
            arduino_code += "    delay(100);\n"
 
    arduino_code += """
    Serial.println("All MAVLink messages sent.");
    delay(5000);
}
 
"""
 
    arduino_code += generate_send_functions()
 
    with open(output_arduino_file, 'w') as f:
        f.write(arduino_code)
 
    print(f"Arduino code has been generated and saved to {output_arduino_file}")
 
 
def extract_params(message):
    pattern = r"{(.*?)}"
    matches = re.search(pattern, message)
    if matches:
        param_str = matches.group(1)
        params = {}
        for param in param_str.split(", "):
            key, value = param.split(" : ")
            params[key.strip()] = value.strip()
        return params
    return {}
 
def generate_generic_mavlink_send_code(message_type, params):
    param_list = []
    for param in params.values():
        # Check if the parameter is a text string or needs quotes
        if param.replace(".", "").isdigit():
            param_list.append(param)
        else:
            param_list.append(f'"{param}"')
    param_list_str = ', '.join(param_list)
    arduino_code = f"""
    send{message_type}({param_list_str});
"""
    return arduino_code
 
def generate_send_functions():
    functions_code = """
void sendGPSRawInt(uint64_t time_usec, uint8_t fix_type, int32_t lat, int32_t lon, int32_t alt, uint16_t eph, uint16_t epv, uint16_t vel, int16_t cog, uint8_t satellites_visible) {
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_gps_raw_int_pack(1, 1, &msg, time_usec, fix_type, lat, lon, alt, eph, epv, vel, cog, satellites_visible);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    udp.beginPacket(udpAddress, udpPort);
    udp.write(buf, len);
    udp.endPacket();
    Serial.println("GPS_RAW_INT message sent");
}
 
void sendHeartbeat(uint8_t type, uint8_t autopilot, uint8_t base_mode, uint32_t custom_mode, uint8_t system_status, uint8_t mavlink_version) {
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_heartbeat_pack(1, 1, &msg, type, autopilot, base_mode, custom_mode, system_status, mavlink_version);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    udp.beginPacket(udpAddress, udpPort);
    udp.write(buf, len);
    udp.endPacket();
    Serial.println("HEARTBEAT message sent");
}
 
// Add more send functions for other message types here
"""
    return functions_code
 
 
# Usage example
input_text_file = "mavlink_messages.txt"
output_arduino_file = "mavlink_esp32_code_all_types.ino"
 
generate_arduino_code_from_text_file(input_text_file, output_arduino_file)
