%启动mongodb_server%
echo mongodb_server.bat 程序内容如下
echo cd C:\Program Files\MongoDB\Server\3.4\bin
echo mongod.exe --dbpath C:\MongoDB\data\db
echo mongo.exe
echo pause
echo 启动mongodb_server.bat程序

Set ws = CreateObject("Wscript.Shell")
ws.run "cmd \C:\Users\Acer\Desktop\import_scripy\mongodb_server.bat",vbhide
