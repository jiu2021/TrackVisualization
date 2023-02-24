const fs = require('fs');
const execSync = require('child_process').execSync;
// const exec = require('child_process').exec;
const returnRes = require('../const_res');
const { createPos } = require('../db/service/position.sv');
const { createRun } = require('../db/service/running.sv');
const { createTruth } = require('../db/service/truth.sv');
const { addPdrArr, addPosArr, addTruthArr } = require('../db/service/user.sv');
class UploadCtr {
  constructor() {
    this.file_name_arr = [];
  }

  // 接受pos文件
  uploadPos(ctx) {
    const fileTypes = ['text/csv'];
    let file = null;
    const const_res = {};
    // pos_file是文件上传时的参数名
    const { pos_file } = ctx.request.files;
    // 检查文件是否为空
    if (!pos_file) {
      return ctx.body = returnRes(400, '上传文件为空', {});
    } else {
      file = pos_file;
    }

    // 检查文件类型
    if (!fileTypes.includes(file.mimetype)) {
      // 删除非法文件
      this.file_name_arr.pop();
      this.deleteFile(file.filepath);
      return ctx.body = returnRes(400, '上传文件格式不正确', {});
    }

    // load到数据库
    this.file_name_arr.push(file.newFilename);
    console.log(this.file_name_arr);
    const_res.sample_arr = this.loadPosByPy('getPosition.py', file.newFilename);
    // 记录到用户数据
    const_res.sample_arr.length != 0 && addPosArr(const_res.sample_arr);

    // 返回响应
    const_res.filename = file.newFilename;
    return ctx.body = returnRes(200, '上传文件成功', const_res);
  }

  // 接受run文件
  uploadRun(ctx) {
    const fileTypes = ['text/csv'];
    let file = null;
    const const_res = {};
    // run_file是文件上传时的参数名
    const { run_file } = ctx.request.files;
    console.log(ctx.request.files)
    // 检查文件是否为空
    if (!run_file) {
      return ctx.body = returnRes(400, '上传文件为空', {});
    } else {
      file = run_file;
    }

    // 检查文件类型
    if (!fileTypes.includes(file.mimetype)) {
      // 删除非法文件
      this.file_name_arr.pop();
      this.deleteFile(file.filepath);
      return ctx.body = returnRes(400, '上传文件格式不正确', {});
    }

    // load到数据库
    this.file_name_arr.push(file.newFilename);
    console.log(this.file_name_arr);
    // 用于区分摆臂数据和非摆臂数据
    let { swing_arr } = ctx.request.body;
    swing_arr = JSON.parse(swing_arr)
    const_res.sample_arr = this.loadRunByPy('getRunning.py', file.newFilename, swing_arr);
    // 记录到用户数据
    const_res.sample_arr.length != 0 && addPdrArr(const_res.sample_arr);

    // 返回响应
    const_res.filename = file.newFilename;
    return ctx.body = returnRes(200, '上传文件成功', const_res);
  }

  // 接受truth文件
  uploadTruth(ctx) {
    const fileTypes = ['text/csv'];
    let file = null;
    const const_res = {};
    // truth_file是文件上传时的参数名
    const { truth_file } = ctx.request.files;
    // 检查文件是否为空
    if (!truth_file) {
      return ctx.body = returnRes(400, '上传文件为空', {});
    } else {
      file = truth_file;
    }

    // 检查文件类型
    if (!fileTypes.includes(file.mimetype)) {
      // 删除非法文件
      this.file_name_arr.pop();
      this.deleteFile(file.filepath);
      return ctx.body = returnRes(400, '上传文件格式不正确', {});
    }

    // load到数据库
    this.file_name_arr.push(file.newFilename);
    console.log(this.file_name_arr);
    // 用于记录该truth对应哪些采样批次数据
    let { sample_arr } = ctx.request.body;
    sample_arr = JSON.parse(sample_arr);
    const_res.sample_arr = [];
    for (let i of sample_arr) {
      const_res.sample_arr.push(parseInt(i));
    }
    // 记录到用户数据
    const_res.sample_arr.length != 0 && addTruthArr(const_res.sample_arr);
    this.loadTruthByPy('getGroundTruth.py', file.newFilename, sample_arr);

    // 返回响应
    const_res.filename = file.newFilename;
    return ctx.body = returnRes(200, '上传文件成功', const_res);
  }

  // 调用py脚本处理position.csv文件
  loadPosByPy(py_script, filename) {
    // 异步执行
    // exec(`python3 py/${py_script} ${filename}`, function (error, stdout) {
    //   if (error) {
    //     console.error('error: ' + error);
    //     return;
    //   }
    //   // 解析py传递的数据，并存储到数据库
    //   try {
    //     const pos_json = JSON.parse(stdout);
    //     for (let i = 0; i < pos_json.length; i++) {
    //       for (let j = 0; j < pos_json[i].length; j++) {
    //         let res = JSON.parse(pos_json[i][j]);
    //         createPos(res);
    //       }
    //     }
    //   } catch (error) {
    //     console.error(error);
    //   }
    // })
    // 同步执行
    const res = execSync(`python3 py/${py_script} ${filename}`);
    const tmp_set = new Set();
    try {
      const pos_json = JSON.parse(res.toString("utf8"));
      for (let i = 0; i < pos_json.length; i++) {
        for (let j = 0; j < pos_json[i].length; j++) {
          let res = JSON.parse(pos_json[i][j]);
          tmp_set.add(res.sample_batch)
          createPos(res);
        }
      }
    } catch (error) {
      console.error(error);
    }
    return Array.from(tmp_set);
  }

  // 调用py脚本处理running.csv文件
  loadRunByPy(py_script, filename, swing_arr) {
    // 异步执行
    // exec(`python3 py/${py_script} ${filename}`, function (error, stdout) {
    //   if (error) {
    //     console.error('error: ' + error);
    //     return;
    //   }
    //   // 解析py传递的数据，并存储到数据库
    //   try {
    //     const run_json = JSON.parse(stdout);
    //     for (let i = 0; i < run_json.length; i++) {
    //       for (let j = 0; j < run_json[i].length; j++) {
    //         let res = JSON.parse(run_json[i][j]);
    //         if (swing_arr.includes(res.sample_batch.toString())) {
    //           createRun({ ...res, isSwing: true });
    //         } else {
    //           createRun({ ...res, isSwing: false })
    //         }
    //       }
    //     }
    //   } catch (error) {
    //     console.error(error);
    //   }
    // });

    // 同步执行
    const res = execSync(`python3 py/${py_script} ${filename}`);
    const tmp_set = new Set();
    try {
      const run_json = JSON.parse(res.toString("utf8"));
      for (let i = 0; i < run_json.length; i++) {
        for (let j = 0; j < run_json[i].length; j++) {
          let res = JSON.parse(run_json[i][j]);
          tmp_set.add(res.sample_batch);
          if (swing_arr.includes(res.sample_batch.toString())) {
            createRun({ ...res, isSwing: true });
          } else {
            createRun({ ...res, isSwing: false })
          }
        }
      }
    } catch (error) {
      console.error(error);
    }
    return Array.from(tmp_set);
  }

  // 调用py脚本处理truth.csv文件
  loadTruthByPy(py_script, filename, sample_arr) {
    // 同步执行
    const res = execSync(`python3 py/${py_script} ${filename}`);
    try {
      const pos_json = JSON.parse(res.toString("utf8"));
      for (let i = 0; i < pos_json.length; i++) {
        sample_arr.forEach(e => {
          createTruth({ ...pos_json[i], sample_batch: parseInt(e) });
        });
      }
    } catch (error) {
      console.error(error);
    }
  }

  // 删除错误文件
  deleteFile(path) {
    fs.unlink(path, err => console.error(err));
  }
}

module.exports = new UploadCtr();