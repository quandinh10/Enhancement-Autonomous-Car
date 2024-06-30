@echo off

python3 threadTrafficSigns.py

timeout 10

python3 threadLaneFollowing.py

exit