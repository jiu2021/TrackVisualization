const Run = require('../model/running.m');

class RunService {
  async createRun(data) {
    let res = await Run.find({ timestamp: data.timestamp });
    // 防止插入重复数据
    if (res.length == 0) {
      return await Run.create(data);
    }
  }

  async findByBatch(num) {
    return await Run.find({ sample_batch: num });
  }
}

module.exports = new RunService();