#!/usr/bin/env python
import datetime
import psutil
from influxdb import InfluxDBClient
import json
import requests

# influx configuration - edit these
ifuser = "grafana"
ifpass = "grafana"
ifdb   = "home"
ifhost = "127.0.0.1"
ifport = 8086
measurement_name = "SHahab-PC"
measurement_name2 = "SHahab-VAIO"
url = "http://192.168.88.12:8085/data.json"
url2 = "http://192.168.88.2:8085/data.json"


def OHM(url,Text, Children):

    def checkData(data,Text, Children):
        try:
            for data in data['Children']:
                if (data['Text']==Text):
                    for data in data['Children']:
                        if (data['Text']==Children):
                            return (data['Value'])
                else:
                    result = (checkData(data, Text, Children))
                    if (result):
                        return(result)
        except NameError:
            print("well, it WASN'T defined after all!")


    try:
        file = requests.get(url)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)
    data = json.loads(file.content)
    
    return (checkData(data,Text,Children))
    



# take a timestamp for this measurement
time = datetime.datetime.utcnow()




# chekc data validation
data = OHM(url,"Temperatures", "CPU Package")
if (data): CPU_Temp= float(data.split('°C')[0])
else: CPU_Temp=0.0

data = OHM(url,"Temperatures", "GPU Core")
if (data): GPU_Temp = float(data.split('°C')[0])
else: GPU_Temp=0.0

data = OHM(url,"Load", "CPU Total")
if(data): CPU_Load = float(data.split('%')[0])
else: CPU_Load = 0.0

data = OHM(url,"Load", "GPU Core")
if (data): GPU_Load = float(data.split('%')[0])
else: GPU_Load=0.0

body = [
    {
        "measurement": measurement_name,
        "time": time,
        "fields": {
            "CPU Temperatures": CPU_Temp,
            "GPU Temperatures": GPU_Temp,
            "CPU Load": CPU_Temp,
            "GPU Load": CPU_Load,
        }
    }
]




data = OHM(url2,"Temperatures", "CPU Package")
if (data): CPU_Temp2= float(data.split('°C')[0])
else: CPU_Temp2=0.0

data = OHM(url2,"Temperatures", "GPU Core")
if (data): GPU_Temp2 = float(data.split('°C')[0])
else: GPU_Temp2=0.0

data = OHM(url2,"Load", "CPU Total")
if(data): CPU_Load2 = float(data.split('%')[0])
else: CPU_Load2 = 0.0

data = OHM(url2,"Load", "GPU Core")
if (data): GPU_Load2 = float(data.split('%')[0])
else: GPU_Load2=0.0


body2 = [
    {
        "measurement": measurement_name2,
        "time": time,
        "fields": {
            "CPU Temperatures": CPU_Temp2,
            "GPU Temperatures": GPU_Temp2,
            "CPU Load": CPU_Temp2,
            "GPU Load": CPU_Load2,
        }
    }
]

# connect to influx
ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

# write the measurement
ifclient.write_points(body)

ifclient.write_points(body2)

