@echo off
REM Build script for Windows

echo Building Mycket for Windows...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Build with PyInstaller
echo Building application...
pyinstaller --noconfirm ^
    --name "Mycket" ^
    --windowed ^
    --onefile ^
    --icon="" ^
    --add-data "src;src" ^
    --hidden-import "PyQt6" ^
    --hidden-import "sqlalchemy.ext.declarative" ^
    src\main.py

echo Build complete! Application is in dist\Mycket.exe
pause
