
// const { writeFile } = require('fs');
const spawn = require('child_process').spawn;
const { findPosByBatch } = require('../db/service/position.sv');
const const_res = require('../const_res');
class TrackCtr {
  async getTrackByBatch(ctx) {
    const { batch } = ctx.query;
    const res = await findPosByBatch(parseInt(batch));

    // console.log(res)
    // const path = './run_29.json';
    // writeFile(path, JSON.stringify(res), (error) => {
    //   if (error) {
    //     console.log('An error has occurred ', error);
    //     return;
    //   }
    //   console.log('Data written successfully to disk');
    // });

    this.getPosTrackByPy(res);

    const_res.code = 200;
    const_res.result = ctx.query.batch;
    return ctx.body = const_res;
  }

  getPosTrackByPy(one_batch) {
    const data_to_py = JSON.stringify(one_batch)
    try {
      // 发数据给py
      const py = spawn('python3', ['py/getPosTrack.py']);
      py.stdin.write(JSON.stringify(data_to_py));
      py.stdin.end();
      // 从py接收数据
      let data_from_py;
      py.stdout.on('data', function (res) {
        data_from_py += res.toString();
        // console.log('读取中:', res.toString())
      });
      py.stdout.on('end', function () {
        // 去掉首尾引号,首部有个undefined
        data_from_py = data_from_py.slice(9, -1);
        //console.log(data_from_py)
        console.log(JSON.parse(data_from_py));
      });
    } catch (error) {
      console.error(error)
    }
  }
}

module.exports = new TrackCtr();