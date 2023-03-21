# CD to ftpserver directory, run gcov for json file, then unzip

cd ../../Source/Release/
gcov ftpserv.c --json-format  
gzip -df ftpserv.gcov.json.gz