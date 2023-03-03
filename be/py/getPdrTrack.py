import csv
import matplotlib.pyplot as plt
import numpy as np
import pywt
import math
import json
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


class Running:
    def __init__(self):
        self.sample_time = []
        self.sample_batch = 0
        self.accx = []
        self.accy = []
        self.accz = []
        self.gyroscopex = []
        self.gyroscopey = []
        self.gyroscopez = []
        self.timestamp = []
        self.time_rel = []
        self.model = 1  # 记录运动模式,0为static,1为dynamic
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
        # 每一步的方向
        self.angle = []
        # 每个定位点的位置
        self.position_x = []
        self.position_y = []
        # 每个定位点的误差
        self.error = []
        self.inf = []

    def get_inf(self):
        inf = []
        count = 0
        if self.model == 1:
            step_time = [i for arr in self.step_time for i in arr]
        elif self.model == 0:
            step_time = [i[1] for i in self.step_time]
        for i in range(len(self.gyroscopex[:-1])):
            if self.timestamp[i] in step_time:
                dic = {'timestamp': float(self.time_rel[i]),
                       'time_rel': float(self.timestamp[i]),
                       'gyroscopex': float(self.gyroscopex[i]),
                       'gyroscopey': float(self.gyroscopey[i]),
                       'gyroscopez': float(self.gyroscopez[i]),
                       'accx': float(self.accx[i]),
                       'accy': float(self.accy[i]),
                       'accz': float(self.accz[i]),
                       'sample_time': self.sample_time[i],
                       'sample_batch': float(self.sample_batch),
                       'x': float(self.position_x[count]),
                       'y': float(self.position_y[count]),
                       'angle': float(self.angle[i]),
                       'length': float(self.length[count]),
                       'error': self.error[count],
                       'isSwing': float(self.model)}
                count += 1
                j = json.dumps(dic)
                inf.append(j)
        self.inf = inf

    def plot_acc(self):
        plt.figure()  # 初始化一张图
        x = self.timestamp
        plt.subplot(3, 1, 1)
        plt.plot(x, self.accx)  # 连线图,若要散点图将此句改为：plt.scatter(x,y) #散点图
        plt.subplot(3, 1, 2)
        plt.plot(x, self.accy)
        plt.subplot(3, 1, 3)
        if self.model == 0:
            if self.step_max:
                x_max = [i[0] for i in self.step_max]
                y_max = [i[1] for i in self.step_max]
                plt.scatter(x_max, y_max, c='r')
            if self.step_min:
                x_min = [i[0] for i in self.step_min]
                y_min = [i[1] for i in self.step_min]
                plt.scatter(x_min, y_min, c='g')
        plt.plot(x, self.accz)
        # plt.show()

    def plot_gyroscope(self):
        plt.figure()  # 初始化一张图
        x = self.timestamp
        plt.subplot(3, 1, 1)
        plt.plot(x, self.gyroscopex)  # 连线图,若要散点图将此句改为：plt.scatter(x,y) #散点图
        plt.subplot(3, 1, 2)
        plt.plot(x, self.gyroscopey)
        plt.subplot(3, 1, 3)
        # threshold_1 = [-150 for _ in range(len(x))]
        # threshold_2 = [-700 for _ in range(len(x))]
        # plt.plot(x, threshold_1, 'r')
        # plt.plot(x, threshold_2, 'g')
        plt.plot(x, self.gyroscopez, marker='x')
        # 以下为动态时计步显示
        if self.model == 1:
            if self.step_max:
                x_max = [i[0] for i in self.step_max]
                y_max = [i[1] for i in self.step_max]
                plt.scatter(x_max, y_max, c='r')
            if self.step_min:
                x_min = [i[0] for i in self.step_min]
                y_min = [i[1] for i in self.step_min]
                plt.scatter(x_min, y_min, c='g')
        # plt.show()

    def step_counter_dynamic(self):
        step = 0
        gyroscopez = self.gyroscopez
        mx, mn = 0, 0
        lens = len(gyroscopez)
        i = 0
        mx_index, mn_index = 0, 0
        while i < lens:
            if gyroscopez[i] > 500:
                # 开始寻找极大值，并将极小值存起来，即步数加一
                if mn < -500:
                    step += 1
                    mn = 0
                    self.step_max.append([self.timestamp[mn_index], self.gyroscopez[mn_index]])
                if gyroscopez[i] > mx:
                    mx = gyroscopez[i]
                    mx_index = i
            elif gyroscopez[i] < -500:
                if mx > 500:
                    step += 1
                    mx = 0
                    self.step_min.append([self.timestamp[mx_index], self.gyroscopez[mx_index]])
                if gyroscopez[i] < mn:
                    mn = gyroscopez[i]
                    mn_index = i
            i += 1

        step_time = []
        for index in range(len(self.step_max)):
            step_time.append([self.step_min[index][0], self.step_max[index][0]])
        self.step_time = step_time
        self.length = [0.6 for _ in range(2*len(self.step_time))]

        # if self.step_time[-1][1] > 0 and mn_index != lens - 1:
        #     step += 1
        #     self.step_time.append([self.timestamp[mn_index], self.gyroscopez[mn_index]])
        # elif self.step_time[-1][1] < 0 and mx_index != lens - 1:
        #     step += 1
        #     self.step_time.append([self.timestamp[mx_index], self.gyroscopez[mx_index]])
        self.step = step

    def step_counter_static(self):
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
        [q0, q1, q2, q3] = [1, 0, 0, 0]
        gamma, theta, phi = [], [], []
        length = len(self.timestamp)
        alpha_new = offset
        alpha = []
        bias_gyx = 0.0288
        bias_gyy = - 0.0293
        bias_gyz = - 0.0351
        bias_ax = - 0.0213
        bias_ay = - 0.3085
        bias_az = - 0.1489
        for i in range(length - 1):
            dt = (self.timestamp[i + 1] - self.timestamp[i]) / 1000
            ax, ay, az = self.accx[i] - bias_ax, self.accy[i] - bias_ay, self.accz[i] - bias_az
            if self.model == 0:
                az -= 1
            add = (ax * self.gyroscopex[i] + ay * self.gyroscopey[i] + az * self.gyroscopez[i]) * dt \
                / np.sqrt(ax ** 2 + ay ** 2 + az ** 2) * 0.1
            if self.model == 0:
                add /= 1.5
            else:
                add /= 1.3
            if self.timestamp[i] >= 5000:
                alpha_new += add

            # sign = np.sign(alpha)
            # if abs(abs(alpha) - 90) < 5:
            #     alpha = 90 * sign
            # elif abs(abs(alpha) - 180) < 20:
            #     alpha = 180 * sign
            # elif abs(abs(alpha) - 270) < 20:
            #     alpha = 270 * sign
            # elif abs(abs(alpha) - 360) < 20:
            #     alpha = 360 * sign
            # elif abs(abs(alpha) - 0) < 5:
            #     alpha = 0
            alpha.append(alpha_new)

            [gx, gy, gz] = [self.gyroscopex[i] / 1250 * 90 * np.pi / 180 - bias_gyx,
                            self.gyroscopey[i] / 1250 * 90 * np.pi / 180 - bias_gyy,
                            self.gyroscopez[i] / 1250 * 90 * np.pi / 180 - bias_gyz]
            gx = gx * dt * 0.5
            gy = gy * dt * 0.5
            gz = gz * dt * 0.5
            q0 = q0 - q1 * gx - q2 * gy - q3 * gz
            q1 = q1 + q0 * gx + q2 * gz - q3 * gy
            q2 = q2 + q0 * gy - q1 * gz + q3 * gx
            q3 = q3 + q0 * gz + q1 * gy - q2 * gx
            [q0, q1, q2, q3] = Vsqrt([q0, q1, q2, q3])
            g1 = 2 * (q1 * q3 - q0 * q2)
            g2 = 2 * (q2 * q3 + q0 * q1)
            g3 = q0 * q0 - q1 * q1 - q2 * q2 + q3 * q3
            g4 = 2 * (q1 * q2 + q0 * q3)
            g5 = q0 * q0 + q1 * q1 - q2 * q2 - q3 * q3
            gamma.append(- np.arcsin(g1) * 180 / np.pi)
            theta.append(- np.arctan2(g2, g3) * 180 / np.pi + offset)
            phi.append(- np.arctan2(g4, g5) * 180 / np.pi + offset)

        self.timestamp = self.timestamp[:-1]

        # 自由摆臂
        # if self.model == 0:
        #     self.angle = phi
        # elif self.model == 1:
        #     self.angle = theta
        # Z轴分量
        self.angle = alpha

        # plt.figure()
        # plt.scatter(self.timestamp, self.angle)
        # plt.subplot(3, 1, 1)
        # plt.scatter(self.timestamp, gamma)
        # plt.subplot(3, 1, 2)
        # plt.scatter(self.timestamp, theta)
        # time = [i for r in self.step_time for i in r]
        # if self.model == 1:
        #     for i in range(len(self.timestamp)):
        #         if self.timestamp[i] in time:
        #             plt.scatter(self.timestamp[i], theta[i], c='r')
        # plt.subplot(3, 1, 3)
        # plt.scatter(self.timestamp, phi)

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
                    invalid.append([i - offset_left, lens - 1])
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
            self.gyroscopex = np.delete(self.gyroscopex, np.s_[i[0]:i[1] + 1], 0)
            self.gyroscopey = np.delete(self.gyroscopey, np.s_[i[0]:i[1] + 1], 0)
            self.gyroscopez = np.delete(self.gyroscopez, np.s_[i[0]:i[1] + 1], 0)
            self.timestamp = np.delete(self.timestamp, np.s_[i[0]:i[1] + 1], 0)

    def pdr_position(self, init_position=(0, 0)):
        position_x = [init_position[0]]
        position_y = [init_position[1]]
        x = init_position[0]
        y = init_position[1]
        counter = 0
        if self.model == 1:
            step_time = [i for arr in self.step_time for i in arr]
        elif self.model == 0:
            step_time = [i[1] for i in self.step_time]
        for i in range(len(self.timestamp)):
            if self.timestamp[i] in step_time:
                if self.model == 0:
                    length = self.length[counter]
                else:
                    length = 0.6
                # print(self.angle[i])
                x += length * np.cos(self.angle[i] * np.pi / 180)
                y += length * np.sin(self.angle[i] * np.pi / 180)
                counter += 1
                if x > 7.647:
                    x = 7.6
                elif x < -4.653:
                    x = -4.6
                if y < -3.21:
                    y = -3.2
                elif y > 4.694:
                    y = 4.6
                position_x.append(x)
                position_y.append(y)
        self.position_x = position_x
        self.position_y = position_y


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
    plt.figure()
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


def error_rate_gt(pos_x, pos_y, gt_x, gt_y):
    error = [0 for _ in range(len(pos_x))]
    if len(pos_x) >= len(gt_x) * 2 - 1:
        for i in range(len(gt_x)):
            dis = line_magnitude(pos_x[2*i], pos_y[2*i], gt_x[i], gt_y[i])
            error[2*i] = dis
            if 2 * i + 1 < len(pos_x):
                error[2*i+1] = dis
    else:
        offset = 2 * len(gt_x) - len(pos_x) - 1
        for i in range(len(gt_x) - offset):
            dis = line_magnitude(pos_x[2*i], pos_y[2*i], gt_x[i], gt_y[i])
            error[2*i], error[2*i+1] = dis, dis
        begin = len(pos_x) - len(gt_x) + 1
        for i in range(offset):
            dis = line_magnitude(pos_x[2*begin-1+i], pos_y[2*begin-1+i], gt_x[begin+i], gt_y[begin+i])
            error[2*begin-1+i] = dis
    return error


def plot_position(r: Running, gt_x, gt_y):
    position_x = r.position_x
    position_y = r.position_y

    img = plt.imread('background.png')
    fig, ax = plt.subplots(figsize=(3, 2), dpi=200)
    ax.imshow(img, extent=[-4.5 - 0.153, 7.8 - 0.153, -3.4 - 0.506, 5.2 - 0.506])
    plt.scatter(0, 0, c='r', s=10)
    plt.plot(position_x, position_y, marker='1')
    # for i in range(len(gt_x)):
    plt.plot(gt_x, gt_y, c='r', marker='1')


def Vsqrt(l: list):
    temp = 0
    for i in l:
        temp += i * i
    recipNorm = 1 / np.sqrt(temp)
    ans = []
    for i in l:
        ans.append(i * recipNorm)
    return ans


def begin_point(p_x, p_y, k):
    # 根据position.csv中在图片所确定的坐标系内的前k个点取平均值作为PDR算法的起始点
    lens = len(p_x)
    k_points = [[], []]
    size = 0
    for i in range(lens):
        if -4.653 < p_x[i] < 7.647 and -3.906 < p_y[i] < 4.694:
            k_points[0].append(p_x[i])
            k_points[1].append(p_y[i])
            size += 1
        if size >= k:
            break
    res = [sum(k_points[0]) / size, sum(k_points[1]) / size]
    # print(res)
    return res


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
            # if each['stay'] == '1':
            #     continue
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
            each['timestamp'] = (int(each['timestamp']) - min)
            r.timestamp.append(each['timestamp'])

            each['accx'] = int(each['accx']) / 16384
            each['accy'] = int(each['accy']) / 16384
            each['accz'] = int(each['accz']) / 16384
            if '26' < batch < '30':
                each['accz'] = each['accz'] + 1
                r.model = 0
            r.accx.append(each['accx'])
            r.accy.append(each['accy'])
            r.accz.append(each['accz'])

            each['gyroscopex'] = int(each['gyroscopex'])
            each['gyroscopey'] = int(each['gyroscopey'])
            each['gyroscopez'] = int(each['gyroscopez'])
            r.gyroscopex.append(each['gyroscopex'])
            r.gyroscopey.append(each['gyroscopey'])
            r.gyroscopez.append(each['gyroscopez'])
    gt_x = [-1, -1, -1, -1, -1, -1, -0.6, 0.2, 1.2, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5]
    gt_y = [3.4, 2.2, 1, -0.2, -1.4, -2.6, -3.2, -3.2, -3.2, -2.6, -1.4, -0.2, 1, 2.2, 3.4]
    lst = ['27', '28', '29', '30', '31', '32']
    # lst = ['30', '31', '32']
    # lst = ['27', '28', '29']
    # lst = ['27']
    dic_position = csv_position(pos_csv)
    for i in lst:
        sample_batch = dic[i].sample_batch
        pos = dic_position[sample_batch]
        pos.x = denoise(pos.x)
        pos.y = denoise(pos.y)
        init_position = begin_point(dic_position[i].x, dic_position[i].y, 10)
        if dic[i].model == 0:
            dic[i].gyroscopex = denoise(dic[i].gyroscopex)
            dic[i].gyroscopey = denoise(dic[i].gyroscopey)
            dic[i].gyroscopez = denoise(dic[i].gyroscopez)
            # dic[i].plot_gyroscope()
            dic[i].invalid_time()
            dic[i].step_counter_static()
            # dic[i].plot_acc()
            # dic[i].plot_gyroscope()
            dic[i].step_length()
            dic[i].cal_angle(-90)
            dic[i].pdr_position(init_position)
            plot_position(dic[i], gt_x, gt_y)

        elif dic[i].model == 1:
            # dic[i].plot_acc()
            dic[i].step_counter_dynamic()
            # dic[i].plot_gyroscope()
            dic[i].cal_angle(-90)
            dic[i].pdr_position(init_position)
            plot_position(dic[i], gt_x, gt_y)
        dic[i].error = error_rate_gt(dic[i].position_x, dic[i].position_y, gt_x, gt_y)
        # print(dic[i].error)
        # plot_error(dic[i].error)
    plt.show()


def json_position(pos_json):
    with open(pos_json, 'r', encoding='utf-8') as jsonfile:
        json_data = json.load(jsonfile)
    return json_data


def pdr_json(json_data):
    with open(get_pdr_json, 'r', encoding='utf-8') as jsonfile:
        json_data = json.load(jsonfile)
    return int(json_data['direction']), json_data['pos_data'], json_data['run_data'], json_data['truth_data']


def json_running(get_pdr_json):
    direction, pos, run_data, truth = pdr_json(get_pdr_json)
    pos_x = [i["x"] for i in pos]
    pos_x = denoise(pos_x)
    pos_y = [i["y"] for i in pos]
    pos_y = denoise(pos_y)
    init_position = begin_point(pos_x, pos_y, 10)

    gt_x, gt_y = [], []
    for data in truth:
        gt_x.append(data['x'])
        gt_y.append(data['y'])

    run = Running()
    run.sample_batch = run_data[0]["sample_batch"]
    if not run_data[0]["isSwing"]:
        run.model = 0
    for each in run_data:
        run.gyroscopex.append(each["gyroscopex"])
        run.gyroscopey.append(each["gyroscopey"])
        run.gyroscopez.append(each["gyroscopez"])
        run.accx.append(each["accx"])
        run.accy.append(each["accy"])
        run.accz.append(each["accz"])
        run.timestamp.append(each["time_rel"])
        run.time_rel.append(each["timestamp"])
        run.sample_time.append(each["sample_time"])
    if run.model == 0:
        run.gyroscopex = denoise(run.gyroscopex)
        run.gyroscopey = denoise(run.gyroscopey)
        run.gyroscopez = denoise(run.gyroscopez)
        run.invalid_time()
        run.step_counter_static()
        run.step_length()
    elif run.model == 1:
        run.step_counter_dynamic()
    run.cal_angle(direction)
    run.pdr_position(init_position)
    run.error = error_rate_gt(run.position_x, run.position_y, gt_x, gt_y)
    run.get_inf()
    # plot_position(run)
    # plot_error(run.error)
    # plt.show()
    
    # python列表转json
    # jsonArr = json.dumps(run.inf, ensure_ascii=False)
    print(jsonArr)
    return run.inf


def main():
    a = json_running('pdr_31.json')
    # data = sys.stdin.readline()
    # csv_running('running.csv', 'position.csv')
    # json_data = json.loads(data)
    # json_running(json_data)


if __name__ == '__main__':
    main()
