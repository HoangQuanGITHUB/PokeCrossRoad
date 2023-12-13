set SHIM_MCCOMPAT=0x800000001
chcp 65001
set PYTHONIOENCODING=utf-8

call "python\python.exe" "src\main.pyc" > "log.txt" 2>&1