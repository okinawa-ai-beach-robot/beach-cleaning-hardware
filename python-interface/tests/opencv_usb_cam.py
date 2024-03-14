import beachbot
import time

cam1 = beachbot.sensors.UsbCameraOpenCV()

cam1.list_cameras()
print("My resolution is:", cam1.get_size())
time.sleep(1)



img1 = cam1.read()
print(img1)
w1 = beachbot.utils.ImageViewer("test")
w1.show(img1)

try:
    for i in range(200):
        img1 = cam1.read()
        print(img1)
        w1.show(img1)
        time.sleep(0.1)
except KeyboardInterrupt as ex:
    pass

w1.close()
cam1.stop()
