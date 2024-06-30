import sys
sys.path.append('..')

from CarCommunication.threadwithstop import ThreadWithStop
import cv2, threading
import numpy as np
import matplotlib.pyplot as plt
from utils import utils
from utils.PIDcontroller import PIDController
from utils.client import Client

DEBUG = True

class threadLaneFollowing(ThreadWithStop):
    def __init__(self, Ip):
        self.cap = cv2.VideoCapture("http://" + Ip + ":8000/stream.mjpg")
        super(threadLaneFollowing, self).__init__()
        self.roi_vertices = [[(0, 480), (180 , 300), (540 , 300), (720, 480)]]
        self.pid_controller = PIDController(Kp=0.5, Ki=0, Kd=0, setpoint=0)
        self.client = Client(server_ip=Ip)
        self.client.connect()

    def run(self):
        deviation = 0
        while self._running:
            _,src_img = self.cap.read() 
            if src_img is None:
                break
            src_img = cv2.resize(src_img,(720,480))
            cropped_img = utils.process_image(src_img, self.roi_vertices)
            lines ,(x,y), slope, deviation_angle = utils.lane_tracking(cropped_img)
            if slope is not None:
                intercept = 400 - slope*360 
                new_x_point = (350-intercept)/slope
                if new_x_point < 0:
                    new_x_point = 0
                elif new_x_point > 720:
                    new_x_point = 720
                #draw bisector line and vertical line
                cv2.line(src_img,(360,400),(int(new_x_point),300),(33,220,208),1)
                cv2.line(src_img,(360,400),(360,300),(220,33,96),1)
            else:
                cv2.line(src_img,(360,400),(360,300),(220,33,96),1)
        
            if lines is None:
                cv2.imshow("black white image",cropped_img)
                cv2.imshow("Image with lines",src_img)
                continue
            
            deviation = x - 360
            control_signal = self.pid_controller.update(deviation_angle)

            try:
                control_signal = "{:.1f}".format(control_signal)
                if DEBUG:
                    # print("deviation:",deviation)
                    print("control signal:",control_signal)
                    # print("slope of bisector:",slope)
                    # print("deviation angle:",deviation_angle)

                
                threading.Thread(target=self.client.client_send, args=(((control_signal)),)).start()
                # [right_slope]
                print("Control signal send:", control_signal)
            except: 
                continue
            for line in lines:
                x1,y1,x2,y2=line
                cv2.line(src_img,(x1,y1),(x2,y2),(0,255,0),2)

            #draw init point and deviation
            image = cv2.circle(src_img, (x,y), radius=1, color=(0, 0, 255), thickness=4)
            image = cv2.circle(src_img, (360,400), radius=1, color=(0, 255, 0), thickness=4)

            #draw ROI
            vertices_array = np.array(self.roi_vertices, dtype=np.int32)  # Convert to NumPy array
            vertices_array = vertices_array.reshape((-1, 1, 2))
            image = cv2.polylines(src_img, [vertices_array], isClosed=True, color=(0, 0, 255), thickness=2)
            
            cv2.imshow("black white image",cropped_img)
            cv2.imshow("Image with lines",src_img)
            cv2.waitKey(10)

    def stop(self):
        super(threadLaneFollowing, self).stop()
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    Ip = "192.168.0.101"

    proc = threadLaneFollowing(Ip)
    proc.start()

    from multiprocessing import Event

    blocker = Event()

    try:
        blocker.wait()
    except KeyboardInterrupt:
        print("\nCatching a KeyboardInterruption exception! Shutdown all processes.\n")
        proc.stop()
        proc.join()