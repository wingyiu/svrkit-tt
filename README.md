#svrkit-tt

## 1.自动生产

先创建service目录,假设服务名为account,则目录为app.account

````
$cd svrkit-tt
$python svrkit/autogen.py account
````

## 2.运行

服务端
`python app/account/test/server.py --port=8080`

客户端
`python app/account/test/client.py`

