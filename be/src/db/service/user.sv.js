const User = require('../model/user.m');

class UserService {
  async verfyUserPWD(user) {
    const res = await User.findOne({ account: user.account, password: user.pwd }).exec();
    return res ? res : null;
  }

  async getInfo() {
    return await User.findOne({ account: '10371037' }).exec();
  }
  async addTruthArr(arr) {
    if (arr.length == 0) return;
    const res = await User.findOne({ account: '10371037' }).exec();
    const new_arr = res?.truth_arr.length != 0 ? [...res?.truth_arr, ...arr] : [...arr];
    console.log(new_arr)
    const set = new Set(new_arr);
    return await User.updateOne({ account: '10371037' }, { truth_arr: Array.from(set) });
  }

  async addPosArr(arr) {
    if (arr.length == 0) return;
    const res = await User.findOne({ account: '10371037' }).exec();
    const new_arr = res?.pos_arr.length != 0 ? [...res?.pos_arr, ...arr] : [...arr];
    const set = new Set(new_arr);
    return await User.updateOne({ account: '10371037' }, { pos_arr: Array.from(set) });
  }

  async addPdrArr(arr) {
    if (arr.length == 0) return;
    const res = await User.findOne({ account: '10371037' }).exec();
    const new_arr = res?.pdr_arr.length != 0 ? [...res?.pdr_arr, ...arr] : [...arr];
    const set = new Set(new_arr);
    return await User.updateOne({ account: '10371037' }, { pdr_arr: Array.from(set) });
  }
}

module.exports = new UserService();