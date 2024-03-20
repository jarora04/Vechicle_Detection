import serial
import cv2
import glob
import time
from vehicle_detector import VD

for i in range(3):
    vd = VD()

    images_folder = glob.glob("images/*.jpg")
    #print(images_folder)

    vehicles_folder_count = 0
    roads = []
    for img_path in images_folder:
        print("Img path", img_path)
        img = cv2.imread(img_path)

        vehicle_boxes = vd.detect_vehicles(img)
        vehicle_count = len(vehicle_boxes)
        roads.append(vehicle_count)

        print(vehicle_count)
        vehicles_folder_count += vehicle_count

        for box in vehicle_boxes:
            x, y, w, h = box

            cv2.rectangle(img, (x, y), (x + w, y + h), (25, 0, 180), 3)

            cv2.putText(img, "Counted Vehicles:" + str(vehicle_count), (20, 50), 0, 2, (100, 200, 0), 3)

        cv2.imshow("Cars", img)
        cv2.waitKey(1)

    # MAX TRAFFIC ON WHICH ROAD

    r1=roads[0]
    r2=roads[1]
    r3=roads[2]
    r4=roads[3]

    Obj = serial.Serial("/dev/cu.usbmodem101")
    Obj.Baudrate = 9600
    Obj.Bytesize = 8
    Obj.parity = 'N'
    Obj.stopbits = 1

    time.sleep(3)
    r3=32
    if ((r1 >= r2 and r1 >= r3) and r1 >= r4) or (r1 >= r2 and (r1 >= r3 and r1 >= r4)):
        r = 1
        max = r1
        print("Road 1 is the busiest")

    elif ((r2 >= r1 and r2 >= r3) and r2 >= r4) or (r2 >= r1 and (r2 >= r3 and r2 >= r4)):
        r = 2
        max = r2
        print("Road 2 is the busiest")

    elif ((r3 >= r1 and r3 >= r2) and r3 >= r4) or (r3 >= r1 and (r3 >= r3 and r3 >= r4)):
        r = 3
        max = r3
        print("Road 3 is the busiest")

    elif ((r4 >= r1 and r4 >= r3) and r4 >= r3) or (r4 >= r1 and (r4 >= r3 and r4 >= r3)):
        r = 4
        max = r4
        print("Road 4 is the busiest")
        
    if (r == 1):
        Obj.write(b"1")
    elif (r == 2):
        Obj.write(b"2")
    elif (r == 3):
        Obj.write(b"3")
    elif (r == 4):
        Obj.write(b"4")

    def countdown(t):
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1
        print('Restarting AI')
    countdown(8)

