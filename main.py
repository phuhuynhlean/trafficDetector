import requests
import json
import time
from PIL import Image
from threading import Thread
from detect import *
from datetime import datetime
from urls import *

def write_json(new_data, filename='data.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data.append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 2)

def captureTraffic():
    loop = 1
    #Thread for parallel execution
    threads = []
    for i in range(0, len(paths)):
      threads.append(Thread(target = capture, args = [paths[i]]))
    
    for i in range(0, len(paths)):
      threads[i].start()

def capture(path):
    while True:
        url = path[2]
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"}
        
        # Save image
        k = 'data/images/' + f'{path[0]}.jpg'
        print(k)
        try:
            if (requests.get(url, headers=headers).headers['Content-Type']):
                timepoint = str(datetime.now())
                with open(k, 'wb') as f:
                    f.write(requests.get(url, headers=headers).content)
                #Resizing image
                im = Image.open(k)
                imB = im.resize((1024,576))
                imB.save(k)
                print("Traffic captured at", time.ctime())
                s = run(source=k, nosave=True)
                print("s is",s)
                x = s.split()
                count, car, bike, truck, bus, person, motorbike = 0, 0, 0, 0, 0, 0, 0
                for part in x:
                    if (count >= 3):
                        if ("car" in part):
                            car = int(temp)
                        elif ("truck" in part):
                            truck = int(temp)
                        elif ("bus" in part):
                            bus = int(temp)
                        elif ("motorcycle" in part):
                            motorbike = int(temp)
                        elif ("bicycle" in part):
                            bike = int(temp)
                    temp = part
                    count += 1
                print(car, bike, truck, bus, person, motorbike)

                y = {
                    "location": path[1],
                    "time": timepoint,
                    "traffic-data" : {
                    "car": car,
                    "bike": bike,
                    "truck": truck,
                    "bus": bus,
                    "person": person,
                    "motorbike": motorbike
                    }
                }
                print(y)
                write_json(y)
        except:
            print("Error when loading at", path[1])

        time.sleep(60)



captureTraffic()

