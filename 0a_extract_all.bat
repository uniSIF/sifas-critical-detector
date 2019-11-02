cd "%~dp0"
call .\env\Scripts\activate
python src/extract_all.py %1
pause