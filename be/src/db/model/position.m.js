const Schema = require('../index');
const mongoose = require('mongoose');
// 创建position模型
const PosSchema = new Schema({
  x: {
    type: Number
  },
  y: {
    type: Number
  },
  z: {
    type: Number
  },
  timestamp: {
    type: Number
  },
  time_rel: {
    type: Number
  },
  sample_batch: {
    type: Number
  },
  sample_time: {
    type: String
  },
})

let posModle = mongoose.model('pos', PosSchema);
// 导出数据表
module.exports = posModle;