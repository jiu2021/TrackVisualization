
// const { writeFile } = require('fs');
const spawnSync = require('child_process').spawnSync;
const { findPosByBatch } = require('../db/service/position.sv');
const { findPdrByBatch, createPdr } = require('../db/service/pdr.sv');
const { findRunByBatch } = require('../db/service/running.sv');
const const_res = require('../const_res');
class TrackCtr {
  async getPosTrackByBatch(ctx) {
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

    const pos_track = this.getPosTrackByPy(res);

    const_res.code = pos_track.length != 0 ? 200 : 400;
    const_res.result = pos_track;
    return ctx.body = const_res;
  }

  getPosTrackByPy(pos_data) {
    const data_to_py = JSON.stringify(pos_data);
    try {
      // 异步方法
      // const py = spawn('python3', ['py/getPosTrack.py']);
      // py.stdin.write(JSON.stringify(data_to_py));
      // py.stdin.end();
      // // 从py接收数据
      // let data_from_py;
      // py.stdout.on('data', function (res) {
      //   data_from_py += res.toString();
      //   // console.log('读取中:', res.toString())
      // });
      // py.stdout.on('end', function () {
      //   // 去掉首尾引号,首部有个undefined
      //   data_from_py = data_from_py.slice(9, -1);
      //   //console.log(data_from_py)
      //   console.log(JSON.parse(data_from_py));
      // });

      // 同步方法
      const py = spawnSync('python3', ['py/getPosTrack.py'], { input: data_to_py });
      return JSON.parse(py.stdout.toString('utf-8'));
    } catch (error) {
      console.error(error);
      return [];
    }
  }

  async getPdrTrackByBatch(ctx) {
    let { batch } = ctx.query;
    batch = parseInt(batch);
    try {
      const res = await findPdrByBatch(batch);
      if (res.length == 0) {
        // 新创建pdr路径数据
        const run_data = await findRunByBatch(batch);
        const pos_data = await findPosByBatch(batch);
        // 调用py
        const_res.result = this.getPdrTrackByPy(pos_data, run_data);
      } else {
        // @ts-ignore
        const_res.result = res;
      }
    } catch (error) {
      console.log(error);
      const_res.code = 400;
      const_res.msg = '生成pdr路径失败';
      return ctx.body = const_res;
    }

    const_res.code = 200;
    const_res.msg = '生成pdr路径成功';
    return ctx.body = const_res;
  }

  getPdrTrackByPy(pos_data, run_data) {
    const data = {
      pos_data,
      run_data
    };
    const data_to_py = JSON.stringify(data);
    try {
      // 同步方法
      const py = spawnSync('python3', ['py/getPdrTrack.py'], { input: data_to_py });
      const pdr_res = JSON.parse(py.stdout.toString('utf-8'));
      pdr_res.forEach(pdr => {
        createPdr(pdr);
      });
      return pdr_res;
    } catch (error) {
      console.error(error);
      return [];
    }
  }
}

module.exports = new TrackCtr();