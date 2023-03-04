# TrackVisualization
### 环境准备：

```
node@v18.0.0
npm@9.3.0
Python@3.11.1
```

安装mongodb数据库，运⾏端⼝27017，新建名为TRACK的数据库，初始化⼀张⽤户数据表:

```json
{
 "account": "xxxxxxxx",
 "isAdmin": true,
 "password": "xxxxxxxxx",
 "username": "xxx",
 "truth_arr": [],
 "pdr_arr": [],
 "pos_arr": []
}
```

### 启动后端

```
// 在项目根目录终端下依次输入
cd be 
npm install // ⾸次使⽤时需要 
npm run dev 
```

后端项⽬运⾏成功时终端会输出：

```
服务启动成功，http://localhost:8000 
数据库连接成功……
```

### 启动前端

```
// 在项目根目录终端下依次输入
cd fe 
npm install // ⾸次使⽤时需要 
npm run serve
```

前端项⽬启动成功终端会提示部署地址：

```
App running at: 
Local: http://localhost:8888/ 
Network: http: //10.10.221.99:8888/
```

若⼀切正常，打开前端服务部署地址，会出现系统⻚⾯。
