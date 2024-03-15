import os, threading

try:
    from jetson_utils import videoSource, videoOutput
    from jetson_utils import cudaImage, cudaToNumpy
except ModuleNotFoundError as ex:
    print("Jetson utils not installed or not available!\nJetsonGstCameraNative not available!")




class JetsonGstCameraNative():
    def __init__(self, width=1920, height= 1080, fps=30, dev_id=0) -> None:
        self._camera = videoSource("csi://"+str(dev_id))
            
    @staticmethod
    def list_cameras():
        print (os.popen("v4l2-ctl --list-devices").read())
        print (os.popen("v4l2-ctl --list-formats-ext").read())


    def read(self):
        cuda_img = self._camera.Capture()
        self._frame = cudaToNumpy(cuda_img)
        return self._frame
    
    def stop(self):
        self._camera.Close()


    def get_size(self):
        return (int(self._camera.GetWidth()), int(self._camera.GetHeight()))





