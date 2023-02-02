const Router = require('koa-router');

const trackCtr = require('../controller/track.ctr');

const router = new Router({ prefix: '/api/track' });

// 获取直接定位路径
router.get('/pos', ctx => trackCtr.getPosTrackByBatch(ctx));

// 获取pdr路径
router.get('/pdr', ctx => trackCtr.getPdrTrackByBatch(ctx));
module.exports = router;
