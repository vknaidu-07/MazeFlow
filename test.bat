@echo off
set "PATH=C:\Users\kushw\AppData\Local\Programs\Python\Python312;C:\Users\kushw\AppData\Local\Programs\Python\Python312\Scripts;%PATH%"
python -m pytest -q %*
