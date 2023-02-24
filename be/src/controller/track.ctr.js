
// const { writeFile } = require('fs');
const spawnSync = require('child_process').spawnSync;
const { findPosByBatch } = require('../db/service/position.sv');
const { findPdrByBatch, createPdr } = require('../db/service/pdr.sv');
const { findRunByBatch } = require('../db/service/running.sv');
const { findTruthByBatch } = require('../db/service/truth.sv');

const returnRes = require('../const_res');
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
    return ctx.body = returnRes(200, '获取定位路径成功', pos_track)
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
    let { batch, direction } = ctx.query;
    batch = parseInt(batch);
    direction = parseInt(direction);
    let result;
    try {
      const res = await findPdrByBatch(batch);
      if (res.length == 0) {
        // 新创建pdr路径数据
        const run_data = await findRunByBatch(batch);
        const pos_data = await findPosByBatch(batch);
        const truth_data = await findTruthByBatch(batch);
        // 调用py
        result = this.getPdrTrackByPy(direction, pos_data, run_data, truth_data);
      } else {
        result = res;
      }
    } catch (error) {
      console.log(error);
      return ctx.body = returnRes(400, '生成pdr路径失败', {});
    }

    return ctx.body = returnRes(200, '生成pdr路径成功', result);
  }

  getPdrTrackByPy(direction, pos_data, run_data, truth_data) {
    const data_to_py = JSON.stringify({
      direction,
      pos_data,
      run_data,
      truth_data,
    });

    try {
      // 同步方法
      const py = spawnSync('python3', ['py/getPdrTrack.py'], { input: data_to_py });
      const pdr_res = JSON.parse(py.stdout.toString('utf-8'));
      const new_pdr = [];
      pdr_res.forEach(pdr => {
        pdr = JSON.parse(pdr);
        new_pdr.push(pdr);
        createPdr(pdr);
      });
      return new_pdr;
    } catch (error) {
      console.error(error);
      return [];
    }
  }

  async getTruthTrackByBatch(ctx) {
    const { batch } = ctx.query;
    const res = await findTruthByBatch(parseInt(batch));
    if (res.length == 0) {
      return ctx.body = returnRes(400, '未找到真实路径', []);
    }
    return ctx.body = returnRes(200, '获取真实路径成功', res)
  }
}

module.exports = new TrackCtr();