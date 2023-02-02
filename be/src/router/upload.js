const Router = require('koa-router');

const uploadCtr = require('../controller/upload.ctr');

const router = new Router({ prefix: '/api' });

// 数据上传接口
router.post('/upload', ctx => uploadCtr.upload(ctx));

router.get('/test', (ctx) => {
  console.log(ctx)
  return ctx.body = '<h1>test</h1>'
})

module.exports = router;