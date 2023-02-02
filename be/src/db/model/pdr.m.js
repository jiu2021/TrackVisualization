const Schema = require('../index');
const mongoose = require('mongoose');
// 创建pdr模型
const PdrSchema = new Schema({
  x: {
    type: Number
  },
  y: {
    type: Number
  },
  length: {
    type: Number
  },
  angle: {
    type: Number
  },
  error: {
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
  gyroscopex: {
    type: Number
  },
  gyroscopey: {
    type: Number
  },
  gyroscopez: {
    type: Number
  },
  accx: {
    type: Number
  },
  accy: {
    type: Number
  },
  accz: {
    type: Number
  },
  isSwing: {
    type: Boolean,
    default: false
  }
})

let pdrModle = mongoose.model('pdr', PdrSchema);
// 导出数据表
module.exports = pdrModle;