from multiprocessing import Queue, Event
from processLaneFollowing import processLaneFollowing
from processTrafficSigns import processTrafficSigns
import logging

queueList = {
    "Critical": Queue(),
    "Warning": Queue(),
    "General": Queue(),
    "Config": Queue(),
}
logging = logging.getLogger()

allProcesses = list()

LaneFollowing = True
TrafficSigns = True


if LaneFollowing:
    processLaneFollowing = processLaneFollowing(queueList, logging)
    allProcesses.append(processLaneFollowing)


if processTrafficSigns:
    processTrafficSigns = processTrafficSigns(queueList, logging)
    allProcesses.append(processTrafficSigns)

for process in allProcesses:
    process.daemon = True
    process.start()



blocker = Event()
try:
    blocker.wait()
except KeyboardInterrupt:
    print("\nCatching a KeyboardInterruption exception! Shutdown all processes.\n")
    for proc in allProcesses:
        print("Process stopped", proc)
        proc.stop()
        proc.join()