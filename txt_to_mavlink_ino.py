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
        if line.startswith("GPS_RAW_INT"):
            # Extract values from GPS_RAW_INT message
            time_usec, fix_type, lat, lon, alt, eph, epv, vel, cog, satellites_visible = extract_gps_raw_int(line)
            arduino_code += f"""
    sendGPSRawInt({time_usec}, {fix_type}, {lat}, {lon}, {alt}, {eph}, {epv}, {vel}, {cog}, {satellites_visible});
    delay(100);
"""
        elif line.startswith("HEARTBEAT"):
            # Extract values from HEARTBEAT message
            type_, autopilot, base_mode, custom_mode, system_status, mavlink_version = extract_heartbeat(line)
            arduino_code += f"""
    sendHeartbeat({type_}, {autopilot}, {base_mode}, {custom_mode}, {system_status}, {mavlink_version});
    delay(100);
"""
 
    arduino_code += """
    Serial.println("All MAVLink messages sent.");
    delay(5000);
}
 
void sendGPSRawInt(uint64_t time_usec, uint8_t fix_type, int32_t lat, int32_t lon, int32_t alt, uint16_t eph, uint16_t epv, uint16_t vel, int16_t cog, uint8_t satellites_visible) {
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_gps_raw_int_pack(1, 1, &msg, time_usec, fix_type, lat, lon, alt, eph, epv, vel, cog, satellites_visible,0,0,0,0,0,0);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    udp.beginPacket(udpAddress, udpPort);
    udp.write(buf, len);
    udp.endPacket();
    Serial.println("GPS_RAW_INT message sent");
}
 
void sendHeartbeat(uint8_t type, uint8_t autopilot, uint8_t base_mode, uint32_t custom_mode, uint8_t system_status, uint8_t mavlink_version) {
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_heartbeat_pack(1, 1, &msg, type, autopilot, base_mode, custom_mode, system_status);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    udp.beginPacket(udpAddress, udpPort);
    udp.write(buf, len);
    udp.endPacket();
    Serial.println("HEARTBEAT message sent");
}

void sendREQUEST_DATA_STREAM(uint8_t target_system, uint8_t target_component, uint8_t req_stream_id, uint16_t req_message_rate, uint8_t start_stop) {
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_request_data_stream_pack(1, 1, &msg, target_system, target_component, req_stream_id, req_message_rate, start_stop);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    udp.beginPacket(udpAddress, udpPort);
    udp.write(buf, len);
    udp.endPacket();
    Serial.println("REQUEST_DATA_STREAM message sent");
}


void sendATTITUDE(uint32_t time_boot_ms, float roll, float pitch, float yaw, float rollspeed, float pitchspeed, float yawspeed) {
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_attitude_pack(1, 1, &msg, time_boot_ms, roll, pitch, yaw, rollspeed, pitchspeed, yawspeed);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    udp.beginPacket(udpAddress, udpPort);
    udp.write(buf, len);
    udp.endPacket();
    Serial.println("ATTITUDE message sent");
}


void sendGLOBAL_POSITION_INT(uint32_t time_boot_ms, int32_t lat, int32_t lon, int32_t alt, int32_t relative_alt, int16_t vx, int16_t vy, int16_t vz, uint16_t hdg) {
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_global_position_int_pack(1, 1, &msg, time_boot_ms, lat, lon, alt, relative_alt, vx, vy, vz, hdg);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    udp.beginPacket(udpAddress, udpPort);
    udp.write(buf, len);
    udp.endPacket();
    Serial.println("GLOBAL_POSITION_INT message sent");
}


void sendSTATUSTEXT(uint8_t severity, const char *text) {
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_statustext_pack(1, 1, &msg, severity, text,0,0);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    udp.beginPacket(udpAddress, udpPort);
    udp.write(buf, len);
    udp.endPacket();
    Serial.println("STATUSTEXT message sent");
}

void sendPARAM_REQUEST_LIST(uint8_t target_system, uint8_t target_component) {
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_param_request_list_pack(1, 1, &msg, target_system, target_component);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    udp.beginPacket(udpAddress, udpPort);
    udp.write(buf, len);
    udp.endPacket();
    Serial.println("PARAM_REQUEST_LIST message sent");
}

void sendCOMMAND_LONG(uint8_t target_system, uint8_t target_component, uint16_t command, uint8_t confirmation, float param1, float param2, float param3, float param4, float param5, float param6, float param7) {
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_command_long_pack(1, 1, &msg, target_system, target_component, command, confirmation, param1, param2, param3, param4, param5, param6, param7);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    udp.beginPacket(udpAddress, udpPort);
    udp.write(buf, len);
    udp.endPacket();
    Serial.println("COMMAND_LONG message sent");
}



void sendMISSION_REQUEST(uint8_t target_system, uint8_t target_component, uint16_t seq) {
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_mission_request_pack(1, 1, &msg, target_system, target_component, seq,0);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    udp.beginPacket(udpAddress, udpPort);
    udp.write(buf, len);
    udp.endPacket();
    Serial.println("MISSION_REQUEST message sent");
}
 
// Add more send functions for other message types here



"""
 
    with open(output_arduino_file, 'w') as f:
        f.write(arduino_code)
 
    print(f"Arduino code has been generated and saved to {output_arduino_file}")
 
 
def extract_gps_raw_int(message):
    parts = message.replace("GPS_RAW_INT {", "").replace("}", "").split(", ")
    values = {}
    for part in parts:
        key, value = part.split(" : ")
        values[key.strip()] = int(value.strip())
    return (
        values["time_usec"],
        values["fix_type"],
        values["lat"],
        values["lon"],
        values["alt"],
        values["eph"],
        values["epv"],
        values["vel"],
        values["cog"],
        values["satellites_visible"]
    )
 
def extract_heartbeat(message):
    parts = message.replace("HEARTBEAT {", "").replace("}", "").split(", ")
    values = {}
    for part in parts:
        key, value = part.split(" : ")
        values[key.strip()] = int(value.strip())
    return (
        values["type"],
        values["autopilot"],
        values["base_mode"],
        values["custom_mode"],
        values["system_status"],
        values["mavlink_version"]
    )
 
# Usage example
input_text_file = "test.txt"
output_arduino_file = "test.ino"
 
generate_arduino_code_from_text_file(input_text_file, output_arduino_file)
