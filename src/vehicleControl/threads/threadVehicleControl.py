import threading
import time
import select
from multiprocessing import Pipe
from src.utils.messages.allMessages import (
    LaneDetect,
    SpeedMotor,
    SteerMotor,
    Control,
    Brake,
)
from src.templates.threadwithstop import ThreadWithStop


class ThreadVehicleControl(ThreadWithStop):
    def __init__(self, pipeRecv, pipeSend, queuesList, logger, debugger):
        super(ThreadVehicleControl, self).__init__()
        self.queuesList = queuesList
        self.logger = logger
        self.pipeRecv = pipeRecv
        self.pipeSend = pipeSend
        self.debugger = debugger
        self.subscribe()

    def subscribe(self):
        self.queuesList["Config"].put(
            {
                "Subscribe/Unsubscribe": "subscribe",
                "Owner": LaneDetect.Owner.value,
                "msgID": LaneDetect.msgID.value,
                "To": {"receiver": "threadVehicleControl", "pipe": self.pipeSend},
            }
        )

    def stop(self):
        super(ThreadVehicleControl, self).stop()


    def run(self):
        # recv_flag = False
        stop_flag = False
        ped_flag = False
        parking_flag = True
        counter_stop = 0
        counter_ped = 0
        while self._running:
            if (stop_flag):
                counter_stop+=1
                if counter_stop == 200:
                    print("Counter stop update")
                    counter_stop = 0
                    stop_flag = False
            if (ped_flag):
                counter_ped+=1
                if counter_ped == 200:
                    print("Counter ped update")
                    counter_ped = 0
                    ped_flag = False
            try:
                if self.pipeRecv.poll():

                    msg = self.pipeRecv.recv()
                    
                    if msg["value"] == "parking" and not parking_flag:
                        # self.pipeRecv.poll().settimeout(5)
                        print("Parking is activated")
                        message_values = [
                            {"Speed": 45, "Time": 0.8, "Steer": -23},
                            {"Speed": 40, "Time": 0.9, "Steer": 0},
                            {"Speed": 40, "Time": 0.5, "Steer": 23},
                            {"Speed": 0, "Time": 0.5, "Steer": -23},
                            {"Speed": -45, "Time": 0.6, "Steer": -23},  
                            {"Speed": 0, "Time": 2, "Steer": 0},
                            {"Speed": -40, "Time": 0.5, "Steer": 0},
                            {"Speed": 0, "Time": 1, "Steer": 23},
                            {"Speed": 45, "Time": 0.8, "Steer": 23},
                            {"Speed": 45, "Time": 1.3, "Steer": -23}
                        ]
                        for msg_value in message_values:
                            self.queuesList[Control.Queue.value].put(
                                {
                                    "Owner": Control.Owner.value,
                                    "msgID": Control.msgID.value,
                                    "msgType": Control.msgType.value,
                                    "msgValue": msg_value,
                                }
                            )
                            time.sleep(msg_value["Time"] + 0.1)
 
                    elif msg["value"] == "stop" and not stop_flag:
                        stop_flag = True
                        print("Stop is activated")
                        message_values = [
                            {"Speed": 30, "Time": 2, "Steer": 0},
                            {"Speed": 25, "Time": 1.5, "Steer": -20},
                            {"Speed": 0, "Time": 3, "Steer": 0},
                            {"Speed": 40, "Time": 2, "Steer": -4}
                        ]
                        for msg_value in message_values:
                            self.queuesList[Control.Queue.value].put(
                                {
                                    "Owner": Control.Owner.value,
                                    "msgID": Control.msgID.value,
                                    "msgType": Control.msgType.value,
                                    "msgValue": msg_value,
                                }
                            )
                            time.sleep(msg_value["Time"] + 0.1)
                            
                        while self.pipeRecv.poll():
                            self.pipeRecv.recv()
     
                    elif msg["value"] == "pedestrian" and not ped_flag:
                        ped_flag = True
                        print("pedestrian is activated")
                        message_values = [
                            {"Speed": 40, "Time": 1, "Steer": -2},
                            {"Speed": 20, "Time": 7, "Steer": -4},
                            {"Speed": 45, "Time": 0.8, "Steer": -23},
                            {"Speed": 40, "Time": 0.9, "Steer": 0},
                            {"Speed": 40, "Time": 0.5, "Steer": 23},
                            {"Speed": 0, "Time": 0.5, "Steer": -23},
                            {"Speed": -45, "Time": 0.6, "Steer": -23},  
                            {"Speed": 0, "Time": 2, "Steer": 0},
                            {"Speed": -40, "Time": 0.5, "Steer": 0},
                            {"Speed": 0, "Time": 1, "Steer": 23},
                            {"Speed": 45, "Time": 0.8, "Steer": 23},
                            {"Speed": 45, "Time": 1.3, "Steer": -23}
                        ]
                        for msg_value in message_values:
                            self.queuesList[Control.Queue.value].put(
                                {
                                    "Owner": Control.Owner.value,
                                    "msgID": Control.msgID.value,
                                    "msgType": Control.msgType.value,
                                    "msgValue": msg_value,
                                }
                            )
                            time.sleep(msg_value["Time"] + 0.1)
                        
                        while self.pipeRecv.poll():
                            self.pipeRecv.recv()
                 
                    else: # Lane keep and turning
                        # recv_flag = False
                        print("running")
                        speed = 40

                        self.queuesList[SpeedMotor.Queue.value].put(
                            {
                                "Owner": SpeedMotor.Owner.value,
                                "msgID": SpeedMotor.msgID.value,
                                "msgType": SpeedMotor.msgType.value,
                                "msgValue": speed,
                            }
                        )
                        
                        
                        steerAngle = 1*float(msg["value"])

                        # Turning
                        if steerAngle > 37:
                            steerAngle = 23
                        elif steerAngle < -37:
                            steerAngle = -23

                        elif 35 < steerAngle <= 37:
                            steerAngle = 18
                        elif -37 <= steerAngle < -35:
                            steerAngle = -18

                        elif 33 < steerAngle <= 35:
                            steerAngle = 15
                        elif -35 <= steerAngle < -33:
                            steerAngle = -15

                        elif 31 < steerAngle <= 33:
                            steerAngle = 10
                        elif -33 <= steerAngle < -31:
                            steerAngle = -10

                        elif 30 < steerAngle < 37:
                            steerAngle = 8
                        elif -37 < steerAngle < -30:
                            steerAngle = -8

                        elif  15 < steerAngle <= 30:
                            steerAngle = 6
                        elif -30 <= steerAngle < -15:
                            steerAngle = -6

                        self.queuesList[SteerMotor.Queue.value].put(
                            {
                                "Owner": SteerMotor.Owner.value,
                                "msgID": SteerMotor.msgID.value,
                                "msgType": SteerMotor.msgType.value,
                                "msgValue": steerAngle,
                            }
                        )
                    
                    
            except Exception as e:
                print(e)

            if self.debugger:
                self.logger.warning("VehicleCtrl is running")

    def start(self):
        super(ThreadVehicleControl, self).start()
