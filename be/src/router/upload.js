const Router = require('koa-router');
const uploadCtr = require('../controller/upload.ctr');
const { auth } = require('../controller/user.ctr');

const router = new Router({ prefix: '/api/upload' });

// pos上传接口
router.post('/pos', auth, ctx => uploadCtr.uploadPos(ctx));
// pos上传接口
router.post('/run', auth, ctx => uploadCtr.uploadRun(ctx));
// pos上传接口
router.post('/truth', auth, ctx => uploadCtr.uploadTruth(ctx));

router.get('/test', (ctx) => {
  console.log(ctx)
  return ctx.body = '<h1>test</h1>'
})

module.exports = router;
