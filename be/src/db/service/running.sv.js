const Run = require('../model/running.m');

class RunService {
  async createRun(data) {
    const res = await Run.find({ timestamp: data.timestamp });
    // 防止插入重复数据
    if (res.length == 0) {
      return await Run.create(data);
    }
  }

  async findRunByBatch(num) {
    return await Run.find({ sample_batch: num }).sort({ time_rel: 1 });
  }
}

module.exports = new RunService();