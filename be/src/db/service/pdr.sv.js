const Pdr = require('../model/pdr.m');

class PdrService {
  async createPdr(data) {
    const res = await Pdr.find({ timestamp: data.timestamp });
    // 防止插入重复数据
    if (res.length == 0) {
      return await Pdr.create(data);
    }
  }

  async findPdrByBatch(num) {
    return await Pdr.find({ sample_batch: num }).sort({ time_rel: 1 });
  }
}

module.exports = new PdrService();