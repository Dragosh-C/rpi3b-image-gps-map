import serial
import requests
import time
import re
from datetime import datetime, timedelta
import logging

FLASK_URL_GPS = 'http://localhost:80/gps-data'
FLASK_URL_UTC = 'http://localhost:80/utc-data'

logging.basicConfig(
    filename='gps_daemon.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

def convert_ddmm_to_decimal(degrees_minutes, is_longitude=False):
    if is_longitude:
        degrees = int(degrees_minutes[:3])
        minutes = float(degrees_minutes[3:])
    else:
        degrees = int(degrees_minutes[:2])
        minutes = float(degrees_minutes[2:])
    decimal_degrees = degrees + minutes / 60
    return decimal_degrees

def parse_nmea_line(line):
    gga_pattern = r'^\$GPGGA,(?P<time>\d{6}\.\d{2}),(?P<lat>\d+\.\d+),(?P<lat_dir>[NS]),(?P<lon>\d+\.\d+),(?P<lon_dir>[EW]),'
    zda_pattern = r'^\$GPZDA,(?P<time_utc>\d{6}\.\d{3}),(?P<day>\d{2}),(?P<month>\d{2}),(?P<year>\d{4}),(?P<offset_hours>[+-]?\d+),(?P<offset_minutes>\d+)\*'
    gga_match = re.match(gga_pattern, line)
    zda_match = re.match(zda_pattern, line)
    gps_data = {}

    if gga_match:
        lat = gga_match.group('lat')
        lat_dir = gga_match.group('lat_dir')
        lon = gga_match.group('lon')
        lon_dir = gga_match.group('lon_dir')
        time = gga_match.group('time')
        latitude = convert_ddmm_to_decimal(lat, is_longitude=False)
        longitude = convert_ddmm_to_decimal(lon, is_longitude=True)

        if lat_dir == 'S':
            latitude = -latitude
        if lon_dir == 'W':
            longitude = -longitude
        
        gps_data['latitude'] = latitude
        gps_data['longitude'] = longitude
        send_data_to_server(gps_data, FLASK_URL_GPS) 
    elif zda_match:
        time_utc = zda_match.group('time_utc')
        day = zda_match.group('day')
        month = zda_match.group('month')
        year = zda_match.group('year')
        offset_hours = int(zda_match.group('offset_hours'))
        offset_minutes = int(zda_match.group('offset_minutes'))

        timestamp_str = f'{year}-{month}-{day} {time_utc}'
        timestamp_utc = datetime.strptime(timestamp_str, '%Y-%m-%d %H%M%S.%f')
        utc_offset = timedelta(hours=offset_hours, minutes=offset_minutes)
        timestamp_utc -= utc_offset
        gps_data['time_utc'] = timestamp_utc.strftime('%Y-%m-%d %H:%M:%S.%f UTC')
        send_data_to_server(gps_data, FLASK_URL_UTC) 

def send_data_to_server(gps_data, url):
    try:
        response = requests.post(url, json=gps_data)
        if response.status_code == 200:
            logging.info(f"Data sent successfully: {gps_data}")
        else:
            logging.error(f"Failed to send data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending data to Flask: {e}")

def listen_to_serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1):
    try:
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            while True:
                try:
                    line = ser.readline().decode('utf-8').strip()
                    if line:
                        logging.info(f"Received: {line}")
                        parse_nmea_line(line)
                except UnicodeDecodeError:
                    logging.warning("Data can't be decoded.")
                except KeyboardInterrupt:
                    logging.info("\nStopped listening.")
                    break
    except serial.SerialException as e:
        logging.error(f"Serial error: {e}")

if __name__ == "__main__":
    listen_to_serial(port='/dev/ttyUSB0', baudrate=9600)
