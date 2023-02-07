const Schema = require('../index');
const mongoose = require('mongoose');
// 创建用户模型
const truthSchema = new Schema({
  step: {
    type: Number
  },
  x: {
    type: Number
  },
  y: {
    type: Number
  },
  sample_batch: {
    type: Number
  }
})

var truthModle = mongoose.model('truths', truthSchema);
// 导出数据表
module.exports = truthModle;