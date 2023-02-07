import csv
import json
import sys

class GroundTruth:
    def __init__(self):
        self.step = []
        self.x = []
        self.y = []
        self.inf = []

    def get_inf(self):
        for i in range(len(self.x)):
            dic = {'step': float(self.step[i]), 'x': float(self.x[i]), 'y': float(self.y[i])}
            # j = json.dumps(dic)
            self.inf.append(dic)


def getGroundTruth(ground_truth_csv):
    with open(ground_truth_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        g = GroundTruth()
        for each in reader:
            g.step.append(each['step'])
            g.x.append(each['x'])
            g.y.append(each['y'])

    g.get_inf()
    return g.inf


if __name__ == '__main__':
    # 测试
    # a = getGroundTruth('py/ground_truth.csv')
    # 从命令行中获取的文件名
    filename = sys.argv[1]
    a = getGroundTruth('upload/{name}'.format(name = filename))
    # python列表转json
    jsonArr = json.dumps(a, ensure_ascii=False)
    print(jsonArr)
