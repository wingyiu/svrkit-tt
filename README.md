#svrkit-tt

## 1.thrift

namespace app.xxx.thf

thrift -r -out . --gen py:tornado app/account/account.thrift

## 2.运行

服务端
`python app/account/test/server.py --port=8080`

客户端
`python app/account/test/client.py`

