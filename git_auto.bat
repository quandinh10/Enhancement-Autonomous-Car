@echo off
setlocal

REM Prompt user for file name
set /p file="Enter file name (or path): "
if "%file%"=="" (
    echo File name cannot be empty. Exiting...
    exit /b 1
)

REM Check if the file exists
if not exist "%file%" (
    echo File does not exist. Exiting...
    exit /b 1
)

REM Add the file to the Git staging area
git add "%file%"
if errorlevel 1 (
    echo Failed to add file to staging area. Exiting...
    exit /b 1
)

REM Prompt user for commit message
set /p commit_msg="Enter commit message: "
if "%commit_msg%"=="" (
    echo Commit message cannot be empty. Exiting...
    exit /b 1
)

REM Commit changes
git commit -m "%commit_msg%"
if errorlevel 1 (
    echo Failed to commit changes. Exiting...
    exit /b 1
)

REM Push changes to the current branch
git push origin HEAD
if errorlevel 1 (
    echo Failed to push changes to the branch. Exiting...
    exit /b 1
)

echo Changes successfully committed and pushed to the branch.
exit /b 0
