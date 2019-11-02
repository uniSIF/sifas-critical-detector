@echo off
echo Building the virtual environment.
python -m venv env
call .\env\Scripts\activate.bat
pip install opencv-python

pause