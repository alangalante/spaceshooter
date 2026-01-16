@echo off
set VENV_DIR=venv

if not exist %VENV_DIR% (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
    echo Installing dependencies...
    call %VENV_DIR%\Scripts\activate
    pip install -r requirements.txt
) else (
    call %VENV_DIR%\Scripts\activate
)

echo Starting Space Shooter...
python main.py
pause
