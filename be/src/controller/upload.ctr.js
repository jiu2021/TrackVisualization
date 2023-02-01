const fs = require('fs');
const execSync = require('child_process').execSync;
// const exec = require('child_process').exec;
const const_res = require('../const_res');
const { createPos } = require('../db/service/position.sv');
const { createRun } = require('../db/service/running.sv');

class UploadCtr {
  constructor() {
    this.file_name_arr = [];
  }

  // 接受上传文件并存到upload目录下
  upload(ctx) {
    const fileTypes = ['text/csv'];
    let file = null;
    // pos_file, run_file是文件上传时的参数名
    const { pos_file, run_file } = ctx.request.files;
    // 检查文件是否为空
    if (!pos_file && !run_file) {
      const_res.msg = '上传文件为空';
      return ctx.body = const_res;
    } else if (pos_file && !run_file) {
      file = pos_file;
    } else if (!pos_file && run_file) {
      file = run_file;
    }

    // 检查文件类型
    if (!fileTypes.includes(file.mimetype)) {
      // 删除非法文件
      this.file_name_arr.pop();
      this.deleteFile(file.filepath);
      const_res.msg = '上传文件格式不正确';
      return ctx.body = const_res;
    }

    // load到数据库
    this.file_name_arr.push(file.newFilename);
    console.log(this.file_name_arr);
    if (file == pos_file) {
      const_res.sample_arr = this.loadPosByPy('getPosition.py', file.newFilename);
    } else if (file == run_file) {
      // 用于区分摆臂数据和非摆臂数据
      const { swing_arr } = ctx.request.body;
      const_res.sample_arr = this.loadRunByPy('getRunning.py', file.newFilename, swing_arr);
    }

    // 返回响应
    const_res.code = 200;
    const_res.msg = '上传文件成功';
    const_res.result = file.newFilename;
    return ctx.body = const_res
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
          tmp_set.add(res.sample_batch)
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

  // 删除错误文件
  deleteFile(path) {
    fs.unlink(path, err => console.error(err));
  }
}

module.exports = new UploadCtr();