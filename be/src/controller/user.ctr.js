const jwt = require('jsonwebtoken');
const returnRes = require('../const_res');
const { verfyUserPWD } = require('../db/service/user.sv');

class UserController {
  // 用户登陆
  async login(ctx) {
    const { account, pwd } = ctx.request.body;
    //获取用户信息
    try {
      //剔除密码信息
      // @ts-ignore
      // eslint-disable-next-line no-unused-vars
      const { password, ...res } = await verfyUserPWD({ account, pwd });
      const data = {
        // @ts-ignore
        username: res._doc.username,
        token: jwt.sign(res, `${process.env.JWT_SECRET}`, { expiresIn: '1d' })
      }
      console.log(data)
      return ctx.body = returnRes(200, '用户登录成功', data);
    } catch (err) {
      console.error('用户登录失败', err);
      return ctx.body = returnRes(400, '用户登失败', {});
    }
  }

  // token鉴权
  async auth(ctx, next) {
    const { authorization = '' } = ctx.request.header;
    const token = authorization.replace('Bearer ', '');
    try {
      const user = jwt.verify(token, `${process.env.JWT_SECRET}`);
      ctx.state.user = user;
      // @ts-ignore
      if (!user._doc.isAdmin) {
        console.error('权限不足');
        return ctx.body = returnRes(400, '权限不足', {});
      }
    } catch (err) {
      console.error('无效的token', err);
      return ctx.body = returnRes(400, '无效的token', {});
    }

    await next();
  }
}

module.exports = new UserController();