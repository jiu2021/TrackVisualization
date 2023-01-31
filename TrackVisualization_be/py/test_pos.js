let exec = require('child_process').exec;

execCmd();

//该方法用于命令行执行python命令 类似于:  python py_test.py arg1
//这样在python中就可以接受传递过去的参数
function execCmd() {
  exec('python3 py/getPosition.py', function (error, stdout) {
    if (error) {
      console.error('error: ' + error);
      return;
    }
    const res = JSON.parse(stdout);
    console.log(res)
    // console.log('receive: ' + stdout.split("#")[0] + ": " + stdout.split("#")[1]);

    // //将返回的json数据解析,判断是都执行下一步
    // let json = JSON.parse(stdsout.split("#")[1]);
    // console.log(json.msg);
  });
}