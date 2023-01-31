const Pos = require('../model/position.m');

class PosService {
  async createPos(data) {
    let res = await Pos.find({ timestamp: data.timestamp });
    // 防止插入重复数据
    if (res.length == 0) {
      return await Pos.create(data);
    }
  }

  async findByBatch(num) {
    return await Pos.find({ sample_batch: num });
  }
}

module.exports = new PosService();