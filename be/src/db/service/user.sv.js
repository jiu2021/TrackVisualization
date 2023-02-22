const User = require('../model/user.m');

class UserService {
  async verfyUserPWD(user) {
    const res = await User.findOne({ account: user.account, password: user.pwd }).exec();
    return res ? res : null;
  }

  async addTruthArr(arr) {
    return await User.updateOne({ account: '10371037' }, { truth_arr: arr });
  }

  async addPosArr(arr) {
    return await User.updateOne({ account: '10371037' }, { pos_arr: arr });
  }

  async addPdrArr(arr) {
    return await User.updateOne({ account: '10371037' }, { pdr_arr: arr });
  }
}

module.exports = new UserService();