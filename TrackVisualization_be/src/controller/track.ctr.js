
const spawn = require('child_process').spawn;
const { findByBatch } = require('../db/service/position.sv');
const const_res = require('../const_res');
class TrackCtr {
  async getTrackByBatch(ctx) {
    const { batch } = ctx.query;
    const res = await findByBatch(parseInt(batch));
    // console.log(res);
    this.usePython(res);

    const_res.code = 200;
    const_res.result = ctx.query.batch;
    return ctx.body = const_res;
  }

  usePython(one_batch) {

    // const batch = JSON.stringify(one_batch).slice(0, 10);
    // const data = {
    //   msg: "Hello"
    // }
    const data = JSON.stringify(one_batch)
    try {
      let py = spawn('python3', ['py/getTrack.py']);
      py.stdin.write(JSON.stringify(data));
      py.stdin.end();

      py.stdout.on('data', function (res) {
        let data = res.toString();
        // 去掉首尾引号
        const newdata = data.slice(1, -2)
        console.log('res', JSON.parse(newdata));
      })
    } catch (error) {
      console.error(error)
    }

    console.log('heh')
  }
}

module.exports = new TrackCtr();