const Router = require('koa-router');
const userCtr = require('../controller/user.ctr');

const router = new Router({ prefix: '/api/user' });

// 用户登陆
router.post('/login', ctx => userCtr.login(ctx));

module.exports = router;
