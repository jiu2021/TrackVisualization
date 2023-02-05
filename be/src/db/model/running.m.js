const Schema = require('../index');
const mongoose = require('mongoose');
// 创建running模型
const RunSchema = new Schema({
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

let runModle = mongoose.model('runs', RunSchema);
// 导出数据表
module.exports = runModle;