const fs = require('fs');
const exec = require('child_process').exec;
const const_res = require('../const_res');
const { createPos } = require('../db/service/position.sv');
const { createRun } = require('../db/service/running.sv');

class UploadCtr {
  constructor() {
    this.file_name_arr = []
  }

  // 接受上传文件并存到upload目录下
  upload(ctx) {
    const fileTypes = ['text/csv'];
    let file = null;
    // pos_file, run_file是文件上传时的参数名
    const { pos_file, run_file } = ctx.request.files;
    console.log(ctx.request.files)
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
      this.loadPosByPy('getPosition.py', file.newFilename);
    } else if (file == run_file) {
      this.loadRunByPy('getRunning.py', file.newFilename);
    }

    // 返回响应
    const_res.code = 200;
    const_res.msg = '上传文件成功';
    const_res.result = file.newFilename;
    return ctx.body = const_res
  }

  // 删除错误文件
  deleteFile(path) {
    fs.unlink(path, err => console.error(err));
  }

  // 调用py脚本处理position文件
  loadPosByPy(py_script, fielname) {
    exec(`python3 py/${py_script} ${fielname}`, function (error, stdout) {
      if (error) {
        console.error('error: ' + error);
        return;
      }
      // 解析py传递的数据，并存储到数据库
      try {
        const pos_json = JSON.parse(stdout);
        for (let i = 0; i < pos_json.length; i++) {
          for (let j = 0; j < pos_json[i].length; j++) {
            createPos(JSON.parse(pos_json[i][j]));
          }
        }
      } catch (error) {
        console.error(error);
      }
    });
  }

  // 调用py脚本处理position文件
  loadRunByPy(py_script, fielname) {
    exec(`python3 py/${py_script} ${fielname}`, function (error, stdout) {
      if (error) {
        console.error('error: ' + error);
        return;
      }
      // 解析py传递的数据，并存储到数据库
      try {
        const run_json = JSON.parse(stdout);
        for (let i = 0; i < run_json.length; i++) {
          for (let j = 0; j < run_json[i].length; j++) {
            createRun(JSON.parse(run_json[i][j]));
          }
        }
      } catch (error) {
        console.error(error);
      }
    });
  }
}

module.exports = new UploadCtr();