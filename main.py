import requests
import time
from PIL import Image
from threading import Thread
from detect import *

#URL and Metadata
path_quoclo1    = ["loc01","Highway A1","http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id=58afea5dbd82540010390c4d&t=1667011700842"]
path_vovankiet  = ["loc02","Vo Van Kiet","http://giaothong.hochiminhcity.gov.vn:80/render/ImageHandler.ashx?id=56de42f611f398ec0c481296&t=1666752019191"]
path_cauphumi   = ["loc03","Vo Chi Cong","http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id=5a8269c45058170011f6eae4"]
path_binhtrieu  = ["loc04","Highway 13 - Pham Van Dong","http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id=58affc6017139d0010f35cc8"]
path_caotocLTDG = ["loc05","Long Thanh - Dau Giay Expressway","http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id=5d9de43b766c880017188cb6&t=1667014633438"]
path_quoclo22   = ["loc06","Highway 22","http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id=589b4379b3bf7600110283c9"]
path_binhphuoc  = ["loc07","Highway 13 - Highway A1","http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id=5874656eb807da0011e33cde&t=1667015665586"]
path_linhxuan   = ["loc08","Highway A1 - Kha Van Can","http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id=58746314b807da0011e33cce&t=1667015860315"]
path_vothisau   = ["loc09","Vo Thi Sau - Dinh Tien Hoang","http://giaothong.hochiminhcity.gov.vn/render/ImageHandler.ashx?id=5a823e425058170011f6eaa4"]
paths   = [path_quoclo1, path_vovankiet, path_cauphumi, path_binhtrieu, path_caotocLTDG, path_quoclo22, path_binhphuoc,path_linhxuan,path_vothisau]

def captureTraffic():
    loop = 1
    #Thread for parallel execution
    threads = []
    for i in range(0, 9):
      threads.append(Thread(target = capture, args = [paths[i]]))
    
    for i in range(0, 9):
      threads[i].start()

def capture(path):
    count = 1
    while True:
        url = path[2]
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"}
        #Save image
        k = 'data/images/' + f'{path[0]}-{time.strftime("%Y_%m_%d_%H_%M_%S")}.jpg'
        print(k)
        try:
            if (requests.get(url, headers=headers).headers['Content-Type']):
                print(path[0], requests.get(url, headers=headers).headers['Content-Type'])
                with open(k, 'wb') as f:
                    f.write(requests.get(url, headers=headers).content)
                #Resizing image
                im = Image.open(k)
                imB = im.resize((1024,576))
                imB.save(k)
                print("Loop",count,"Traffic captured at", time.ctime())
                run(source=k, nosave=True)
                print("Detect "+k)
        except:
           print("Error")
        time.sleep(30)
        count+=1

captureTraffic()

