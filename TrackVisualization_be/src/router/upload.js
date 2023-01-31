const Router = require('koa-router');

const uploadCtr = require('../controller/upload.ctr');

const router = new Router();

// 数据上传接口
router.post('/upload', ctx => uploadCtr.upload(ctx));

router.get('/test', (ctx) => {
  console.log(ctx)
})

module.exports = router;
