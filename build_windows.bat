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

REM Check if icon exists, if not skip icon parameter
if exist "icon.ico" (
    set ICON_PARAM=--icon "icon.ico"
) else (
    echo Warning: icon.ico not found, building without custom icon
    set ICON_PARAM=
)

pyinstaller --noconfirm ^
    --name "Mycket" ^
    --windowed ^
    --onefile ^
    --paths "src" ^
    %ICON_PARAM% ^
    --hidden-import "database" ^
    --hidden-import "database.models" ^
    --hidden-import "ui" ^
    --hidden-import "ui.main_window" ^
    --hidden-import "ui.time_tracker" ^
    --hidden-import "ui.services_panel" ^
    --hidden-import "ui.reports_panel" ^
    --hidden-import "PyQt6" ^
    --hidden-import "PyQt6.QtCore" ^
    --hidden-import "PyQt6.QtWidgets" ^
    --hidden-import "PyQt6.QtGui" ^
    --hidden-import "sqlalchemy.ext.declarative" ^
    src\main.py

echo Build complete! Application is in dist\Mycket.exe
pause
