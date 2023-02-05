const Router = require('koa-router');
const trackCtr = require('../controller/track.ctr');
const { auth } = require('../controller/user.ctr');

const router = new Router({ prefix: '/api/track' });

// 获取直接定位路径
router.get('/pos', auth, ctx => trackCtr.getPosTrackByBatch(ctx));
// 获取pdr路径
router.get('/pdr', auth, ctx => trackCtr.getPdrTrackByBatch(ctx));

module.exports = router;
