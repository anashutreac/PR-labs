import sys
import requests
import threading
import queue
import json
import xmltodict
import csv
from io import StringIO

fileAllData = open("AllData", "ab+")

def process(path):
    result = requests.get(url + path, headers=headers)
    data_queue.put(result)
    for k in result:
        fileAllData.write(k)


def parseJsonData(result_text):
    result_dict = json.loads(result_text)
    return [result_dict]



def parseXMLData(result_text):
    result_dict = dict(xmltodict.parse(result_text)['device'])
    result_dict["device_id"] = result_dict.pop("@id")
    result_dict["sensor_type"] = int(result_dict.pop("type"))
    return [result_dict]



def parseCSVData(data):
    str_data = StringIO(data)
    reader = csv.reader(str_data)
    reader = list(map(list, reader))
    reader.pop(0)
    for line in reader:
        result_dict = dict(zip(metric_keys, line))
        result_dict["sensor_type"] = int(result_dict.pop("sensor_type"))
        result_dict["sensor_type"] = int(result_dict.pop("sensor_type"))
        result.append(result_dict)
    return result
#
def printData(sensor_data):
     for k in sensor_types:
         print("\n" + sensor_types[k])
         if k in sensor_data.keys():
             for dct in sensor_data[k]:
                 print("Device " + dct['device_id'] + ' - ' + str(dct['value']))
         else:
            print("Secret data not detected")



def processData(raw_data):
    for result_dict in raw_data:
        if result_dict["sensor_type"] not in sensor_data:
            sensor_data[result_dict["sensor_type"]] = []
            sensor_data[result_dict["sensor_type"]].append(result_dict)
        else:
            sensor_data[result_dict["sensor_type"]].append(result_dict)

url = 'https://desolate-ravine-43301.herokuapp.com'

try:
    result = requests.post(url)
except:
    print("Check your conection")
    sys.exit(1)

key = result.headers['session']
headers = {'session': key}
paths = json.loads(result.text)
paths = [path['path'] for path in paths]

metric_keys = ["device_id","sensor_type","value"]
sensor_types = {0: 'Temperature sensor', 1: 'Humidity Sensor', 2: 'Motion Sensor', 3: 'Alien Presence Detector', 4: 'Dark Matter Detector'}
sensor_data = {}
threads = []
data_queue = queue.Queue()

for path in paths:
    t = threading.Thread(target=process, args=(path,))
    threads.append(t)
    t.start()

for path in paths:
    data = data_queue.get()
    content_type = (data.headers['content-type']).lower()
    if content_type == 'application/json':
        result = parseJsonData(data.text)
    elif content_type == 'application/xml':
        result = parseXMLData(data.text)
    elif content_type == 'text/csv':
        result = parseCSVData(data.text)
    processData(result)

printData(sensor_data)
if __name__ == '__main__':
    pass


