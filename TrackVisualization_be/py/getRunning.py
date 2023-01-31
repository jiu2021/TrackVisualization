import csv
import matplotlib.pyplot as plt
import numpy as np
import pywt
import math
import json


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
        self.error = []


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

    def get_inf(self, offset):
        inf = []
        step_time = [i[1] for i in self.step_time]
        count = 0
        angle = offset
        for i in range(len(self.timestamp)):
            if self.timestamp[i] in step_time:
                time = self.timestamp[i]
                length = len(self.angles)
                for j in range(1, length + 1):
                    if time > self.angles[length - j][0]:
                        angle = self.angles[length - j][1]
                        break
                dic = {'x': float(self.position_x[count]), 'y': float(self.position_y[count]),
                       'time_rel': float(self.timestamp[i]), 'timestamp': float(self.time_rel[i]),
                       'gyroscopex': float(self.gyroscopex[i]), 'gyroscopey': float(self.gyroscopey[i]),
                       'gyroscopez': float(self.gyroscopez[i]),
                       'accx': float(self.accx[i]), 'accy': float(self.accy[i]), 'accz': float(self.accz[i]),
                       'angle': float(angle), 'length': float(self.length[count]),
                       'sample_time': self.sample_time[i], 'sample_batch': float(self.sample_batch)}
                j = json.dumps(dic)
                count += 1
                inf.append(j)
        self.inf = inf

    def plot_acc(self):
        plt.figure()  # 初始化一张图
        x = self.timestamp
        plt.subplot(4, 1, 1)
        plt.plot(x, self.accx)  # 连线图,若要散点图将此句改为：plt.scatter(x,y) #散点图
        plt.subplot(4, 1, 2)
        plt.plot(x, self.accy)
        plt.subplot(4, 1, 3)
        # print(self.step_max)
        if self.step_max:
            x_max = [i[0] for i in self.step_max]
            y_max = [i[1] for i in self.step_max]
            plt.scatter(x_max, y_max, c='r')
        if self.step_min:
            x_min = [i[0] for i in self.step_min]
            y_min = [i[1] for i in self.step_min]
            plt.scatter(x_min, y_min, c='g')
        plt.plot(x, self.accz)
        plt.subplot(4, 1, 4)
        if self.length:
            # print(self.length)
            time = [i[0] for i in self.step_time]
            plt.scatter(time, self.length)
        plt.show()

    def plot_gyroscope(self):
        plt.figure()  # 初始化一张图
        x = self.timestamp
        plt.subplot(3, 1, 1)
        plt.plot(x, self.gyroscopex)  # 连线图,若要散点图将此句改为：plt.scatter(x,y) #散点图
        plt.subplot(3, 1, 2)
        plt.plot(x, self.gyroscopey)
        plt.subplot(3, 1, 3)
        threshold_1 = [-150 for _ in range(len(x))]
        threshold_2 = [-700 for _ in range(len(x))]
        plt.plot(x, threshold_1, 'r')
        plt.plot(x, threshold_2, 'g')
        plt.plot(x, self.gyroscopez, marker='x')

    def step_counter(self):
        step = 0
        threshold_value = 0.05
        threshold_time = 50
        accz = self.accz
        timestamp = self.timestamp
        mx, mn = [], []
        pre_index = 0

        for index, value in enumerate(accz):
            if index == 0:
                continue
            if value > 0 and (value - accz[index - 1]) > threshold_value \
                    and (timestamp[index] - timestamp[index - 1]) > threshold_time:
                while index < len(accz) - 1 and accz[index] < accz[index + 1]:
                    index += 1

                # 在波峰的前temp个值中找波谷
                temp = 4
                if temp < index:
                    l = accz[index - temp: index]
                    # i = accz.index(min(l))
                    accz = np.array(accz)
                    i = np.where(accz == min(l))[0][0]
                    if pre_index >= i or [timestamp[i], accz[i]] in mn:
                        last = mx.pop()
                        if accz[index] > last[1]:
                            mx.append([timestamp[index], accz[index]])
                            pre_index = index
                        else:
                            mx.append(last)
                    else:
                        step += 1
                        pre_index = index
                        mx.append([timestamp[index], accz[index]])
                        mn.append([timestamp[i], accz[i]])

        # print("原有数据：" + str(len(accz)) + "条")
        # print("检测到波峰：" + str(len(mx)) + '个')
        # print("检测到波谷：" + str(len(mn)) + '个')
        self.step_max = mx
        self.step_min = mn
        self.step = step
        step_time = []
        for index in range(len(mx)):
            step_time.append([mn[index][0], mx[index][0]])
        self.step_time = step_time

    def step_length(self):
        length = []
        K = 0.5
        g = 9.8
        l = len(self.step_max)
        for index in range(l):
            res = K * (self.step_max[index][1] * g - self.step_min[index][1] * g) ** 0.25
            length.append(res)
        self.length = length

    def cal_angle(self, offset):
        length = len(self.gyroscopez)
        begin, end = 0, 0
        i = 0
        angle = offset
        angles = []
        flag = 0

        while i < length:
            if self.gyroscopez[i] < -700:
                flag = 1
                for j in range(1, i):
                    if self.gyroscopez[i - j] >= -150:
                        begin = i - j + 1
                        break
                for j in range(1, length - i):
                    if self.gyroscopez[i + j] >= -150:
                        end = i + j - 1
                        break
                if end < begin:
                    end = len(self.gyroscopez) - 1
                angle_add = 0
                for j in range(begin, end + 1):
                    angle_add += (self.gyroscopez[j] + self.gyroscopez[j - 1]) * \
                             (self.timestamp[j] - self.timestamp[j - 1]) / 2000
                angle_add = - angle_add / 1250 * 90
                sign = np.sign(angle_add)
                if abs(abs(angle_add) - 90) < 12:
                    angle_add = 90 * sign
                elif abs(abs(angle_add) - 180) < 30:
                    angle_add = 180 * sign
                elif abs(abs(angle_add) - 270) < 30:
                    angle_add = 270 * sign
                elif abs(abs(angle_add) - 360) < 30:
                    angle_add = 360 * sign
                elif abs(abs(angle_add) - 0) < 12:
                    angle_add = 0
                angle += angle_add
                # print(angle_add)
                angle %= 360
                # print(self.timestamp[begin], self.timestamp[end], angle)
                angles.append([self.timestamp[(begin+end)//2], angle])

            if flag == 1:
                i = end
                flag = 0
            i += 1
        # print(angles)
        self.angles = angles
        return angles

    def pdr_position(self, offset=0, init_position=(0, 0)):
        position_x = [init_position[0]]
        position_y = [init_position[1]]
        x = init_position[0]
        y = init_position[1]
        angle = offset
        angles = self.cal_angle(offset)

        for i in range(self.step):
            time = self.step_time[i][1]
            length = len(angles)
            for j in range(1, length + 1):
                if time > angles[length - j][0]:
                    angle = angles[length - j][1]
                    break
            x += self.length[i] * np.cos(angle * np.pi / 180)
            y += self.length[i] * np.sin(angle * np.pi / 180)

            if x > 7.647:
                x = 7.6
            elif x < -4.653:
                x = -4.6
            if y < -3.906:
                y = -3.906
            elif y > 4.694:
                y = 4.6

            position_x.append(x)
            position_y.append(y)

        self.position_x = position_x
        self.position_y = position_y
        # position = []
        # for i in range(len(position_x)):
        #     position.append([position_x[i],position_y[i]])
        # for i in position:
        #     print(i)

    def invalid_time(self):
        invalid = []
        lens = len(self.gyroscopex)
        mean_x = abs(sum(self.gyroscopex) / lens) + 10
        mean_y = abs(sum(self.gyroscopey) / lens) + 10
        i = 0
        while i < lens - 1:
            if abs(self.gyroscopex[i]) > 200:
                # 此时运动状态不是水平移动
                offset_left = 1
                while i > offset_left and abs(self.gyroscopex[i - offset_left]) >= mean_x:
                    offset_left += 1
                offset_right = 1
                while i + offset_right < lens - 2 and abs(self.gyroscopex[i + offset_right]) >= mean_x:
                    offset_right += 1
                if i == lens - 1:
                    invalid.append([i - offset_left, lens-1])
                else:
                    invalid.append([i - offset_left, i + offset_right])
                i += offset_right
            elif abs(self.gyroscopey[i]) > 150:
                # 此时运动状态不是水平移动
                offset_left = 1
                while i > offset_left and abs(self.gyroscopey[i - offset_left]) >= mean_y:
                    offset_left += 1
                offset_right = 1
                while i + offset_right < lens - 1 and abs(self.gyroscopey[i + offset_right]) >= mean_y:
                    offset_right += 1
                if i == lens - 1:
                    invalid.append([i - offset_left, lens - 1])
                else:
                    invalid.append([i - offset_left, i + offset_right])
                i += offset_right
            else:
                i += 1
        # print(invalid)
        for i in invalid:
            self.accx = np.delete(self.accx, np.s_[i[0]:i[1] + 1], 0)
            self.accy = np.delete(self.accy, np.s_[i[0]:i[1] + 1], 0)
            self.accz = np.delete(self.accz, np.s_[i[0]:i[1] + 1], 0)
            self.gyroscopex = np.delete(self.gyroscopex, np.s_[i[0]:i[1]+1], 0)
            self.gyroscopey = np.delete(self.gyroscopey, np.s_[i[0]:i[1]+1], 0)
            self.gyroscopez = np.delete(self.gyroscopez, np.s_[i[0]:i[1]+1], 0)
            self.timestamp = np.delete(self.timestamp, np.s_[i[0]:i[1]+1], 0)
            self.time_rel = np.delete(self.time_rel, np.s_[i[0]:i[1]+1], 0)
            self.sample_time = np.delete(self.sample_time, np.s_[i[0]:i[1]+1], 0)


def denoise(data):
    def sgn(num):
        if num > 0:
            return 1.0
        elif num == 0:
            return 0.0
        else:
            return -1.0

    w = pywt.Wavelet('sym8')
    [ca3, cd3, cd2, cd1] = pywt.wavedec(data, w, level=3)  # 分解波

    length1 = len(cd1)
    length0 = len(data)

    Cd1 = np.array(cd1)
    abs_cd1 = np.abs(Cd1)
    median_cd1 = np.median(abs_cd1)

    sigma = (1.0 / 0.6745) * median_cd1
    lamda = sigma * math.sqrt(2.0 * math.log(float(length0), math.e))
    # print(lamda)
    usecoeffs = [ca3]

    # 软硬阈值折中的方法
    a = 0.2

    for k in range(length1):
        if abs(cd1[k]) >= lamda + 700:
            cd1[k] = sgn(cd1[k]) * (abs(cd1[k]) - a * lamda)
        else:
            cd1[k] = 0.0

    length2 = len(cd2)
    for k in range(length2):
        if abs(cd2[k]) >= lamda + 700:
            cd2[k] = sgn(cd2[k]) * (abs(cd2[k]) - a * lamda)
        else:
            cd2[k] = 0.0

    length3 = len(cd3)
    for k in range(length3):
        if abs(cd3[k]) >= lamda + 700:
            cd3[k] = sgn(cd3[k]) * (abs(cd3[k]) - a * lamda)
        else:
            cd3[k] = 0.0

    usecoeffs.append(cd3)
    usecoeffs.append(cd2)
    usecoeffs.append(cd1)
    recoeffs = pywt.waverec(usecoeffs, w)

    return recoeffs[:len(data)]


def plot_position(r: Running, p: Position):
    position_x = r.position_x
    position_y = r.position_y

    img = plt.imread('background.png')
    fig, ax = plt.subplots(figsize=(4, 3), dpi=200)
    ax.imshow(img, extent=[-4.5 - 0.153, 7.8 - 0.153, -3.4 - 0.506, 5.2 - 0.506])
    plt.scatter(0, 0, c='r', s=10)
    plt.plot(position_x, position_y, marker='1')

    x = p.x
    y = p.y

    plt.scatter(x, y, c='g', s=10, marker='p')

    gt_x = [[-1, -1], [-1, 1.5], [1.5, 1.5]]
    gt_y = [[3.4, -3.2], [-3.2, -3.2], [-3.2, 3.4]]
    for i in range(len(gt_x)):
        plt.plot(gt_x[i], gt_y[i], c='r')

    # plt.subplots(figsize=(4, 3), dpi=200)
    # plt.subplot(3, 1, 1)
    # t1 = r.timestamp
    # plt.plot(t1, r.gyroscopez)
    # plt.subplot(3, 1, 2)
    # t2 = pos.timestamp
    # plt.scatter(t2, x, s=10)
    # plt.subplot(3, 1, 3)
    # plt.scatter(t2, y, s=10)

    # plt.show()


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


def begin_point(p: Position, k):
    # 根据position.csv中在图片所确定的坐标系内的前k个点取平均值作为PDR算法的起始点
    lens = len(p.x)
    k_points = [[], []]
    size = 0
    for i in range(lens):
        if -4.653 < p.x[i] < 7.647 and -3.906 < p.y[i] < 4.694:
            k_points[0].append(p.x[i])
            k_points[1].append(p.y[i])
            size += 1
        if size >= k:
            break
    res = [sum(k_points[0]) / size, sum(k_points[1]) / size]
    # print(res)
    return res


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
    return dic


def csv_running(run_csv, pos_csv):
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

    lst = ['27', '28', '29']
    for i in lst:
        dic[i].gyroscopex = denoise(dic[i].gyroscopex)
        dic[i].gyroscopey = denoise(dic[i].gyroscopey)
        dic[i].gyroscopez = denoise(dic[i].gyroscopez)
        # acc 不能进行降噪，不然没法识别步数

    for value in dic.values():
        value.step_counter()
        value.step_length()

    gt = [[-1, 3.4, -1, -3.2], [-1, -3.2, 1.5, -3.2], [1.5, -3.2, 1.5, 3.4]]
    dic_position = csv_position(pos_csv)
    ans = []
    for i in lst:
        sample_batch = dic[i].sample_batch
        pos = dic_position[sample_batch]
        pos.x = denoise(pos.x)
        pos.y = denoise(pos.y)
        init_position = begin_point(dic_position[i], 10)
        # dic[i].plot_gyroscope()
        dic[i].invalid_time()
        # dic[i].plot_gyroscope()
        # dic[i].plot_acc()
        dic[i].pdr_position(offset=-90, init_position=init_position)
        # plot_position(dic[i], pos)
        error = error_rate(dic[i].position_x, dic[i].position_y, gt)
        dic[i].error = error

        error = error_rate(pos.x, pos.y, gt)
        pos.error = error

        dic[i].get_inf(-90)
        ans.append(dic[i].inf)
        # plt.show()
    return ans


def main():
    ans = csv_running('py/running.csv', 'py/position.csv')
    # python列表转json
    jsonArr = json.dumps(ans, ensure_ascii=False)
    print(jsonArr)
    return ans


if __name__ == '__main__':
    main()
