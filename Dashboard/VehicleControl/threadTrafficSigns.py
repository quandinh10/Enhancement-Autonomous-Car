import sys
sys.path.append('..')

from CarCommunication.threadwithstop import ThreadWithStop
from ultralytics import YOLO
import threading
from utils.client import Client

class threadTrafficSigns(ThreadWithStop):
    def __init__(self, Ip):
        super(threadTrafficSigns, self).__init__()
        self.model = YOLO('./utils/best.pt')
        self.source = "http://" + Ip + ":8000/stream.mjpg"
        self.stopFlag = False
        self.client = Client(server_ip=Ip)
        self.client.connect()

    def run(self):
        prev_rev = ""
        try:
            for results in self.model.predict(source=self.source, stream=True, show=True, conf = 0.6):
                if not self._running:
                    break
                if (len(results.boxes.cls) == 0):
                    prev_rev = ""
                    continue
                for box in results.boxes:
                    class_id = int(box.cls)
                    class_label = results[0].names[class_id]
                    print(f'Detected class: {class_label}')
                    if (prev_rev != class_label):
                        print("prev_rev:",prev_rev)
                        prev_rev = class_label
                        threading.Thread(target=self.client.client_send, args=(((class_label)),)).start()
                    
        except Exception as e:
            print(e)
        
    def stop(self):
        super(threadTrafficSigns, self).stop()



if __name__ == "__main__":
    Ip = "192.168.0.101"
    proc = threadTrafficSigns(Ip)
    proc.start()

    from multiprocessing import Event

    blocker = Event()

    try:
        blocker.wait()
    except KeyboardInterrupt:
        print("\nCatching a KeyboardInterruption exception! Shutdown all processes.\n")
        proc.stop()
        proc.join()
    