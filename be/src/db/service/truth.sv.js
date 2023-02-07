const Truth = require('../model/truth.m');

class TruthService {
  async createTruth(data) {
    const res = await Truth.find({ x: data.x, y: data.y, step: data.step, sample_batch: data.sample_batch });
    // 防止插入重复数据
    if (res.length == 0) {
      return await Truth.create(data);
    }
  }

  async findTruthByBatch(num) {
    return await Truth.find({ sample_batch: num }).sort({ step: 1 });
  }
}

module.exports = new TruthService();