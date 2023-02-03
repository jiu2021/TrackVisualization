module.exports = function returnRes(code, msg, res) {
  return {
    code,
    msg,
    data: res
  }
}