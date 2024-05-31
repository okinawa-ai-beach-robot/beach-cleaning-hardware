from .imageviewermatplotlib import ImageViewerMatplotlib
from .imageviewerjetson import ImageViewerJetson
from .videowriteropencv import VideoWriterOpenCV
from .videoserveropencv import VideoServerOpenCV
from .timer import Timer


import os
import signal, time
import subprocess
from subprocess import Popen, PIPE

def is_running_by_pid(pid):
    #stat = os.system("ps -p %s &> /dev/null" % pid)
    stat = subprocess.call("ps -p %s" % pid,stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    return stat == 0

def kill_by_port(port):
    process = Popen(["lsof", "-i", ":{0}".format(port)], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    print("AAA#", stdout)
    for process in str(stdout.decode("utf-8")).split("\n")[1:]:       
        data = [x for x in process.split(" ") if x != '']
        if (len(data) <= 1):
            continue
        print(data)
        try:
            os.kill(int(data[1]), signal.SIGKILL)
        except:
            pass
        c=0
        while is_running_by_pid(int(data[1])) and c<10:
            time.sleep(.25)
            c += 1
