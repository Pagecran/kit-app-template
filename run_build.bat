start /wait /b cmd /c repo.bat build -c > build_log.txt 2>&1
type build_log.txt
