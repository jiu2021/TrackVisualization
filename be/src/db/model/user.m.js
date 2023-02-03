const Schema = require('../index');
const mongoose = require('mongoose');
// 创建用户模型
const userSchema = new Schema({
  username: {
    type: String,
    maxlength: 10,
    minlength: 2,
    required: true,
  },
  password: {
    type: String,
    required: true,
  },
  account: {
    type: String,
    required: true
  },
  isAdmin: {
    type: Boolean,
    required: true,
    default: false
  }
})

var userModle = mongoose.model('users', userSchema);
// 导出数据表
module.exports = userModle;