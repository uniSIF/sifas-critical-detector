cd "%~dp0"
call .\env\Scripts\activate
python src/extract.py %1
pause