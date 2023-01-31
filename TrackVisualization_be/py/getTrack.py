import sys
import json

if __name__ == '__main__':
    # 从标准输入中获取json数据
    data = sys.stdin.readline().replace("\\","")
    print(data)
    # data = lines[0].replace("\\","")
    # data = json.loads(lines)
    # a = 'hello'
    # b = 'msg'
    # print(a)
    # sys.stdout.flush()
    # a = '[{"_id":"63d7e513791ebb7294749d2a","x":-1.41510141699826,"y":4.298218355249162,"z":0.8,"timestamp":0,"sample_batch":28,"sample_time":"2022-10-24,15:00:44","__v":0},{"_id":"63d880a1aa701aa9146aca7d","x":-1.41510141699826,"y":4.298218355249162,"z":0.8,"timestamp":0,"sample_batch":28,"sample_time":"2022-10-24,15:00:44","__v":0}]'
    # b = json.loads(a)
    # print(b[0],b[0]['_id'])