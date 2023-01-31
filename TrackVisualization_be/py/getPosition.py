import csv
import matplotlib.pyplot as plt
import json
import numpy as np
import sys


class Position:
    def __init__(self):
        self.sample_batch = 0
        self.x = []
        self.y = []
        self.z = []
        self.timestamp = []
        self.time_rel = []
        self.error = []
        self.sample_time = []
        self.inf = []
        self.error= []

    def get_inf(self):
        for i in range(len(self.x)):
            dic = {'x': float(self.x[i]), 'y': float(self.y[i]),'z':float(self.z[i]),
                   'time_rel': float(self.timestamp[i]),
                   'timestamp': float(self.time_rel[i]),
                   'sample_batch': float(self.sample_batch),
                   'sample_time': self.sample_time[i]}
            j = json.dumps(dic)
            self.inf.append(j)


def csv_position(pos_csv):
    dic = {}
    with open(pos_csv, 'r', encoding='utf-8') as csvfile:
        # 调用csv中的DictReader函数直接获取数据为字典形式
        reader = csv.DictReader(csvfile)
        # 创建一个counts计数一下 看自己一共添加的数据条数
        counts = 0
        min = 1e20
        for each in reader:
            if each['sample_batch'] not in dic.keys():
                min = int(each['timestamp'])
                p = Position()
                dic[each['sample_batch']] = p
            else:
                p = dic[each['sample_batch']]
            # 将数据中需要转换类型的数据转换类型。原本全是字符串（string）
            each['x'] = float(each['x'])
            each['y'] = float(each['y'])
            each['z'] = float(each['z'])
            p.x.append(each['x'])
            p.y.append(each['y'])
            p.z.append(each['z'])
            p.sample_time.append(each['sample_time'])
            p.time_rel.append(each['timestamp'])
            each['timestamp'] = int(each['timestamp']) - min
            p.timestamp.append(each['timestamp'])
            p.sample_batch = each['sample_batch']
    gt = [[-1, 3.4, -1, -3.2], [-1, -3.2, 1.5, -3.2], [1.5, -3.2, 1.5, 3.4]]
    lst = ['27', '28', '29', '30', '31', '32']
    for i in lst:
        dic[i].error = error_rate(dic[i].x, dic[i].y, gt)
    # print(dic['27'].x)
    # print(dic['27'].y)
    # plot_xy(dic['27'])

    # for value in dic.values():
    #     plot_xy(value)
    # plt.show()
    return dic


def line_magnitude(x1, y1, x2, y2):
    lineMagnitude = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return lineMagnitude


def point_to_line_distance(point, line):
    px, py = point
    x1, y1, x2, y2 = line
    line = line_magnitude(x1, y1, x2, y2)
    if line == 0:
        # print('两点重合')
        return line_magnitude(px, py, x1, y1)
    else:
        ul = (px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)
        u = ul/(line ** 2)
        if u <= 0 or u > 1:
            ix = line_magnitude(px, py, x1, y1)
            iy = line_magnitude(px, py, x2, y2)
            if ix >= iy:
                return iy
            else:
                return ix
        else:
            ix = x1 + u * (x2 - x1)
            iy = y1 + u * (y2 - y1)
            distance = line_magnitude(px, py, ix, iy)
            return distance


def plot_error(error_distance):
    maximum = max(error_distance)
    point = np.linspace(0, np.ceil(maximum), 200)
    total = len(error_distance)
    lst = []
    for i in point:
        res = np.sum(error_distance <= i)
        lst.append(res / total)
    plt.plot(point, lst)
    plt.xlabel('Localization Error/m')
    plt.ylabel('CDF')
    # plt.show()


def error_rate(pos_x, pos_y, gt):
    # ground truth 的输入形式是[[start_x1, start_y1, stop_x1, stop_y1]...[start_xn, start_yn, stop_xn, stop_yn]]
    error_distance = []
    for i in range(len(pos_x)):
        distance = []
        for gt_line in gt:
            res = point_to_line_distance([pos_x[i], pos_y[i]], gt_line)
            distance.append(res)
        minimum = min(distance)
        error_distance.append(minimum)

    ave_error = sum(error_distance) / len(error_distance)
    # print(ave_error)
    # plt.figure()
    # plot_error(error_distance)
    return error_distance


def plot_xy(p: Position):
    fig, ax = plt.subplots(figsize=(4, 3), dpi=200)  # 初始化一张图
    img = plt.imread('background.png')

    ax.imshow(img, extent=[-4.5 - 0.153, 7.8 - 0.153, -3.4 - 0.506, 5.2 - 0.506])
    plt.scatter(p.x, p.y, s=10)  # 散点图

    # plt.subplots(figsize=(4, 3), dpi=200)
    # plt.subplot(2, 1, 1)
    # plt.plot(p.timestamp, p.x)
    # plt.subplot(2, 1, 2)
    # plt.plot(p.timestamp, p.y)  # 连线图


def getPosition(pos_csv):
    dic = csv_position(pos_csv)
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
    getPosition('upload/{name}'.format(name = filename))

    # 测试用
    # filename = "position.csv"
    # getPosition('py/{name}'.format(name = filename))
