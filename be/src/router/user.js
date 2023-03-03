const Router = require('koa-router');
const userCtr = require('../controller/user.ctr');
const { auth } = require('../controller/user.ctr');

const router = new Router({ prefix: '/api/user' });
// 用户登录
router.post('/login', ctx => userCtr.login(ctx));
// 用户数据
router.get('/data', auth, ctx => userCtr.userInfo(ctx));

module.exports = router;
