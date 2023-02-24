export function getCDF(gt_length, err_arr) {
  var gt_len = gt_length;
  // var error = [0.2900153248482196, 0.2900153248482196, 0.2900153248482196, 0.2900153248482196, 0.2900153248482196, 0.2900153248482196, 0.19871911260363492, 0.19871911260363492, 0.3630188597772237, 0.3630188597772237, 0.9456954569689642, 0.9456954569689642, 0.7835864020561948, 0.7835864020561948, 0.49134427015033505, 0.49134427015033505, 0.5019919936824768, 0.5019919936824768, 0.5753210023174802, 0.5753210023174802, 0.7046403700930479, 0.7046403700930479, 0.6701967480449608, 0.6701967480449608, 0.7455682911735355, 0.7370511802826432, 1.0052871310658569]; // 计算所得的30个点的误差 
  var error = err_arr;
  var pos_len = error.length;
  var error_gt = [];
  if (pos_len >= gt_len * 2 - 1) {
    for (let i = 0; i < gt_len; i++) {
      // error_gt[i] = error[2*i];
      error_gt.push(error[2 * i]);
    }
  }
  else {
    var offset = 2 * gt_len - pos_len - 1
    for (let i = 0; i < gt_len - offset; i++) {
      // error_gt[i] = error[2*i]
      error_gt.push(error[2 * i]);
    }
    var begin = pos_len - gt_len + 1
    for (let i = 0; i < offset; i++) {
      // error_gt[begin+i] = error[2*begin-1+i]
      error_gt.push(error[2 * begin - 1 + i]);
    }
  }
  var err_average = error_gt.reduce((prev, current, index, arr) => {
    return prev + current;
  });
  err_average = err_average / error_gt.length;

  // console.log(error_gt)
  var max = Math.max.apply(Math, error_gt);
  // console.log(max)
  var value = []
  var cdf_y = []

  for (let i = 0; i < 200; i++) {
    let thr = (max + 0.1) / 200 * i;
    value.push(thr)
    let num = 0
    error_gt.forEach(item => {
      item <= thr ? num++ : '';
    })
    cdf_y.push(num);
  }
  // x 轴
  // console.log(value);
  // // y 轴
  // console.log(cdf_y);
  var cdf = []
  for (let i = 0; i < value.length; i++) {
    cdf.push({ x: value[i], y: cdf_y[i] / gt_length });
  }
  console.log(cdf, err_average)
  return { cdf: cdf, avg: err_average };
}