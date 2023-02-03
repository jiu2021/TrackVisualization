const User = require('../model/user.m');

class UserService {
  async verfyUserPWD(user) {
    const res = await User.findOne({ account: user.account, password: user.pwd }).exec();
    return res ? res : null;
  }
}

module.exports = new UserService();