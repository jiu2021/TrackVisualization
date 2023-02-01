const Router = require('koa-router');

const trackCtr = require('../controller/track.ctr');

const router = new Router();

// 数据上传接口
router.get('/track', ctx => trackCtr.getTrackByBatch(ctx));

module.exports = router;
