const Router = require('koa-router');
const uploadCtr = require('../controller/upload.ctr');
const { auth } = require('../controller/user.ctr');

const router = new Router({ prefix: '/api' });

// 数据上传接口
router.post('/upload', auth, ctx => uploadCtr.upload(ctx));

router.get('/test', (ctx) => {
  console.log(ctx)
  return ctx.body = '<h1>test</h1>'
})

module.exports = router;
