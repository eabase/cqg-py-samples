call protoc.exe --python_out=..\webapi WebAPI\webapi_1.proto
call protoc.exe --python_out=..\webapi WebAPI\metadata_1.proto
call protoc.exe --python_out=..\webapi WebAPI\rules_1.proto
call protoc.exe --python_out=..\ common\shared_1.proto
call protoc.exe --python_out=..\ common\decimal.proto
call protoc.exe --python_out=..\ common\timestamp.proto