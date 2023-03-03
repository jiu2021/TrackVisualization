const path = require('path');
const Koa = require('koa');
const { koaBody } = require('koa-body')
const KoaStatic = require('koa-static');

const uploadRouter = require('./src/router/upload');
const trackRouter = require('./src/router/track');
const userRouter = require('./src/router/user');
// const errHandler = require('./errHandler');

const app = new Koa();

// 处理post文件上传
app.use(koaBody({
  multipart: true,
  formidable: {
    //不建议使用相对路径
    uploadDir: path.join(__dirname, './upload'),
    keepExtensions: true,
  },
}));

app.use(KoaStatic(path.join(__dirname, './upload')));

// app.use(parameter(app));

// 注册路由
app.use(uploadRouter.routes());
app.use(trackRouter.routes());
app.use(userRouter.routes());

// 导入配置文件
require('dotenv').config();

// //  统一错误处理
// app.on('error', errHandler);

// app.use(ctx => ctx.body = "<h1>Hello TrackVisualization</h1>");

const port = 8000;
app.listen(port, () => {
  console.log(`服务启动成功，http://localhost:${port}`);
})


module.exports = app;