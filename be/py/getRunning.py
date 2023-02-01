import json
import csv
import sys

class Running:
    def __init__(self):
        self.sample_batch = 0
        self.accx = []
        self.accy = []
        self.accz = []
        self.gyroscopex = []
        self.gyroscopey = []
        self.gyroscopez = []
        self.timestamp = []
        self.time_rel = []
        self.sample_time = []
        # 以上信息通过读入，并通过筛选删除与修改
        # 迈步的z轴加速度最大与最小
        self.step_max = []
        self.step_min = []
        # 迈步时刻
        self.step_time = []
        # 步数
        self.step = 0
        # 每一步的长度
        self.length = []
        # 每一次转弯的时间与角度
        self.angles = []
        # 每个定位点的位置
        self.position_x = []
        self.position_y = []
        # 每个定位点的误差
        self.error = []
        # 信息汇总
        self.inf = []

    def get_inf(self):
        inf = []
        count = 0
        for i in range(len(self.timestamp)):
            dic = {'timestamp': float(self.time_rel[i]),
                   'time_rel': float(self.timestamp[i]),
                   'gyroscopex': float(self.gyroscopex[i]),
                   'gyroscopey': float(self.gyroscopey[i]),
                   'gyroscopez': float(self.gyroscopez[i]),
                   'accx': float(self.accx[i]),
                   'accy': float(self.accy[i]),
                   'accz': float(self.accz[i]),
                   'sample_time': self.sample_time[i],
                   'sample_batch': float(self.sample_batch)}
            j = json.dumps(dic)
            count += 1
            inf.append(j)
        self.inf = inf


def getRunning(run_csv):
    min = 1e20
    dic = {}
    with open(run_csv, 'r', encoding='utf-8') as csvfile:
        # 调用csv中的DictReader函数直接获取数据为字典形式
        reader = csv.DictReader(csvfile)
        for each in reader:
            batch = each['sample_batch']
            if batch not in dic.keys() or int(each['timestamp']) < min:
                min = int(each['timestamp'])
                # print("初始时间戳发生变化: ", min)
                r = Running()
                r.sample_batch = batch
                dic[batch] = r
            else:
                r = dic[batch]
            # 将数据中需要转换类型的数据转换类型。原本全是字符串（string）
            r.time_rel.append(int(each['timestamp']))
            each['timestamp'] = (int(each['timestamp']) - min)
            r.timestamp.append(each['timestamp'])
            r.sample_time.append(each['sample_time'])

            each['accx'] = int(each['accx']) / 16384
            each['accy'] = int(each['accy']) / 16384
            each['accz'] = int(each['accz']) / 16384
            if '26' < batch < '30':
                each['accz'] = each['accz'] + 1
            r.accx.append(each['accx'])
            r.accy.append(each['accy'])
            r.accz.append(each['accz'])

            each['gyroscopex'] = int(each['gyroscopex'])
            each['gyroscopey'] = int(each['gyroscopey'])
            each['gyroscopez'] = int(each['gyroscopez'])
            r.gyroscopex.append(each['gyroscopex'])
            r.gyroscopey.append(each['gyroscopey'])
            r.gyroscopez.append(each['gyroscopez'])

    ans = []
    for i in dic.values():
        i.get_inf()
        ans.append(i.inf)

    # python列表转json
    jsonArr = json.dumps(ans, ensure_ascii=False)
    print(jsonArr)
    return ans


if __name__ == '__main__':
    # 从命令行中获取的文件名
    filename = sys.argv[1]
    getRunning('upload/{name}'.format(name = filename))

    # 测试
    # getRunning('py/running.csv')
