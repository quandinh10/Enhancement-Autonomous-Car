@echo off
REM Execute mbed-tools compile command
mbed-tools compile -m NUCLEO_F411RE -t GCC_ARM

REM Check if compilation was successful
if %errorlevel% neq 0 (
    echo Compilation failed
    exit /b
)
