from pyecharts import options as opts
from pyecharts.globals import GeoType
from pyecharts.charts import Line3D, Scatter3D, Geo
import csv
import time


def read_csv(filename):
    """读取csv文件"""
    with open(filename, newline='') as csvfile:
        items = csv.reader(csvfile)
        next(items)  # 读取首行
        dd = []
        for item in items:
            dd.append(item)
    return dd


def write_result(filename, result):
    """将result写入csv文件"""
    outfile = open(filename, 'w', newline='', encoding='UTF-8')
    writer = csv.writer(outfile)
    writer.writerow(('timestamp', 'imsi', 'lac_id', 'cell_id', 'longitude', 'latitude'))
    for i in range(0, len(result)):
        writer.writerow((result[i][0], result[i][1], result[i][2], result[i][3], result[i][4], result[i][5]))
    outfile.close()


def clean_data():
    """数据清洗"""
    # 读取原始数据
    original_file_name = 'E:/demon/data/服创大赛-原始数据.csv'
    original = read_csv(original_file_name)
    print(len(original))

    # 保存前四列数据
    next0 = []
    for i in range(0, len(original)):
        next0.append([original[i][0], original[i][1], original[i][2], original[i][3]])
        print(next0[i])

    # 去掉为空和imsi中包含特殊字符的数据条目（‘#’,’*’,’^’）
    next1 = []
    for i in range(0, len(next0)):
        if len(next0[i][1]) == 0:
            continue
        elif len(next0[i][2]) == 0:
            continue
        elif len(next0[i][3]) == 0:
            continue
        elif next0[i][1].find("#") >= 0:
            continue
        elif next0[i][1].find("*") >= 0:
            continue
        elif next0[i][1].find("^") >= 0:
            continue
        else:
            next1.append(next0[i])
    print(len(next1))

    # 输出next1内容（调试使用）
    # for i in range(0, len(next1)):
    #     print(i, next1[i])

    # 转化时间戳
    for i in range(0, len(next1)):
        temp = int(next1[i][0])
        timestamp = float(temp / 1000)
        timearray = time.localtime(timestamp)
        next1[i][0] = time.strftime("%Y%m%d%H%M%S", timearray)

    # 去掉不是20181003的记录
    next2 = []
    for i in range(0, len(next1)):
        if next1[i][0].find("20181003") >= 0:
            next2.append(next1[i])
        else:
            continue
    print(len(next2))

    # 去除两数据源关联后经纬度为空的数据条目
    # 读取基站数据
    base_data_file = 'E:/demon/data/服创大赛-基站经纬度数据.csv'
    locate = read_csv(base_data_file)
    next3 = []
    for i in range(0, len(next2)):
        temp = next2[i][2] + "-" + next2[i][3]
        for j in range(0, len(locate)):
            if locate[j][2].find(temp) >= 0:
                next3.append((next2[i][0], next2[i][1], next2[i][2], next2[i][3], locate[j][0], locate[j][1]))
                break
            else:
                continue
    print(len(next3))

    # 排序
    result = sorted(next3)
    # 输出结果
    for i in range(0, len(result)):
        print(i, result[i][0], result[i][1], result[i][2], result[i][3], result[i][4], result[i][5])

    # 输出到文件
    outfilename = 'E:/demon/data/newdata/newData.csv'
    write_result(outfilename, result)

# clean_data()

def count_everyhour_num():
    """计算每个小时的记录数"""

    newdatafile = 'E:/demon/data/newdata/newData.csv'
    item = read_csv(newdatafile)
    print(len(item))
    hour = [0 for x in range(0, 24)]
    print(len(hour))
    for i in range(0, len(item)):
        if item[i][0][8] == '0':
            temp = int(item[i][0][9])
            hour[temp] += 1
        if item[i][0][8] == '1':
            temp = int(item[i][0][9])
            hour[temp + 10] += 1
        if item[i][0][8] == '2':
            temp = int(item[i][0][9])
            hour[temp + 20] += 1
    print(hour)
    # 输出文件
    outfilename = 'E:/demon/data/newdata/everyHour.csv'
    outfile = open(outfilename, 'w', newline='', encoding='UTF-8')
    writer = csv.writer(outfile)
    writer.writerow(('hour', 'num'))
    for i in range(0, len(hour)):
        s = (i.__str__() + '--' + (i + 1).__str__())
        writer.writerow((s, hour[i]))
    outfile.close()


def every_everypeople_num():
    """计算每一个人的记录数"""
    newdatafile = 'E:/demon/data/newdata/newData.csv'
    item = read_csv(newdatafile)
    people = []
    data = []
    for i in range(0, len(item)):
        data.append(item[i][1])
        if item[i][1] not in people:
            people.append(item[i][1])
    res_data = []
    for i in people:
        res_data.append(data.count(i))
    print(len(res_data))
    for i in range(0, len(people)):
        people[i] = (people[i], res_data[i])
    for i in range(0, len(people)):
        print(i, people[i])
    print(len(people))
    people_item = []
    for j in range(0, len(people)):
        for i in range(0, len(item)):
            if item[i][1] == people[j][0]:
                people_item.append((item[i][1], item[i][0], item[i][4], item[i][5]))
    print(len(people_item))
    for i in range(0, len(people_item)):
        print(i, people_item[i])

    # 将每一个人的记录数写入文件
    every_people_num_filename = 'E:/demon/data/newdata/people_num.csv'
    every_people_num = open(every_people_num_filename, 'w', newline='', encoding='UTF-8')
    writer = csv.writer(every_people_num)
    writer.writerow(('people_id', 'num'))
    for i in range(0, len(people)):
        writer.writerow(people[i])
    every_people_num.close()

    # 将每一个人的记录写入文件（按人员和时间顺序排列）
    every_people_item_filename = 'E:/demon/data/newdata/people_item.csv'
    every_people_item = open(every_people_item_filename, 'w', newline='', encoding='UTF-8')
    writer = csv.writer(every_people_item)
    writer.writerow(('people_id', 'timestamp', 'longitude', 'latitude'))
    for i in range(0, len(people_item)):
        writer.writerow(people_item[i])
    every_people_item.close()


def geo(base_location, staticdata, people_item):
    """绘制地图并描点"""

    city = '沈阳'
    g = Geo()
    g.add_schema(maptype=city)

    # 定义坐标对应的名称，添加到坐标库中 add_coordinate(name, lng, lat)
    # 将基站信息添加到坐标库中
    for i in range(0, len(base_location)):
        g.add_coordinate(base_location[i][2], base_location[i][0], base_location[i][1])

    # 将出行方式静态数据添加到坐标库中（地铁和公交）
    for i in range(0, len(staticdata)):
        g.add_coordinate(staticdata[i][3], staticdata[i][0], staticdata[i][1])

    # 将人员的信息记录添加到坐标库中
    for i in range(0, len(people_item)):
        g.add_coordinate(people_item[i][1], people_item[i][2], people_item[i][3])

    # 定义数据对
    data_pair = []
    # 基站
    for i in range(0, len(base_location)):
        data_pair.append((base_location[i][2], '基站'))

    for i in range(0, len(staticdata)):
        # 地铁
        if staticdata[i][2] == '地铁':
            data_pair.append((staticdata[i][3], staticdata[i][2] + staticdata[i][4] + '号线'))
        # 公交
        elif staticdata[i][2] == '公交':
            data_pair.append((staticdata[i][3], '公交'))

    # 人员记录
    for i in range(0, len(people_item)):
        data_pair.append((people_item[i][1], '人'))

    # 将数据添加到地图上
    g.add('', data_pair, type_=GeoType.EFFECT_SCATTER, symbol_size=6)
    # 设置样式
    g.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    # 自定义分段 color 可以用取色器取色
    pieces = [
        {'min': '基站', 'max': '基站', 'label': '基站', 'color': '#D94E5D'},
        {'min': '地铁1号线', 'max': '地铁1号线', 'label': '地铁1号线', 'color': '#87CEFA'},
        {'min': '地铁2号线', 'max': '地铁2号线', 'label': '地铁2号线', 'color': '#DA70D6'},
        {'min': '地铁9号线', 'max': '地铁9号线', 'label': '地铁9号线', 'color': '#32CD32'},
        {'min': '公交', 'max': '公交', 'label': '公交', 'color': '#6495ED'},
        {'min': '人', 'max': '人', 'label': '人', 'color': '#000000'}
    ]
    # is_piecewise 是否自定义分段， 变为true 才能生效
    g.set_global_opts(
        visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=pieces),
        title_opts=opts.TitleOpts(title="{}-站点分布".format(city)),
    )
    return g


def get_people_item():
    people_item_file = 'E:/demon/data/newdata/people_item.csv'
    people_item = read_csv(people_item_file)
    return people_item


def get_user_id_list(people_item):
    user_id_list = []
    for i in range(0, len(people_item)):
        if people_item[i][0] not in user_id_list:
            user_id_list.append(people_item[i][0])
    for i in range(0, len(user_id_list)):
        user_id_list[i] = (i, user_id_list[i])
    return user_id_list


def drow_effectscatter():
    """调用geo()来画散点图"""

    # 读取基站数据
    base_location_file = 'E:/demon/data/服创大赛-基站经纬度数据.csv'
    base_location = read_csv(base_location_file)
    print(len(base_location))

    # 读取出行方式静态数据
    static_data_file = 'E:/demon/data/服创大赛-出行方式静态数据.csv'
    static_data = read_csv(static_data_file)
    print(len(static_data))

    # 读取人员记录数据
    people_item = get_people_item()
    print(len(people_item))

    g = geo(base_location, static_data, people_item)
    # 渲染成html, 可用浏览器直接打开
    g.render('ShenYang.html')


def get_color():
    """计算颜色值"""
    # 分为114个颜色
    hexnum = []
    for i in range(0, 114):
        hexnum.append(str(hex(i * 0x243f6)))

    # 六位十六进制表示的颜色值
    color = []
    for i in range(0, len(hexnum)):
        if i < 8:
            if i == 0:
                color.append('#000000')
            else:
                temp = '#0'
                for j in range(2, len(hexnum[i])):
                    temp += hexnum[i][j]
                color.append(temp)
        else:
            temp = '#'
            for j in range(2, len(hexnum[i])):
                temp += hexnum[i][j]
            color.append(temp)
    return color


def get_pieces(color):
    """得到3D散点图、3D折线图的用例颜色"""
    pieces = []
    for i in range(0, len(color)):
        pieces.append({'min': i, 'max': i, 'label': i, 'color': color[i]})
    return pieces


def get_data():
    people_item = get_people_item()
    user_id_list = get_user_id_list(people_item)
    data = []
    for i in range(0, len(people_item)):
        x = float(people_item[i][2])
        y = float(people_item[i][3])
        temp = []
        for j in range(8, len(people_item[i][1])):
            temp.append(int(people_item[i][1][j]))
        z = (temp[0] * 10 + temp[1]) * 3600 + (temp[2] * 10 + temp[3]) * 60 + temp[4] * 10 + temp[5]
        for j in range(0, len(user_id_list)):
            if people_item[i][0] == user_id_list[j][1]:
                user_id = user_id_list[j][0]
        data.append([x, y, z, user_id])
    return data


def get_people(user_id_list, data):
    people = []
    for i in range(0, len(user_id_list)):
        people.append([])
        for j in range(0, len(data)):
            if data[j][3] == i:
                people[i].append(data[j])
    return people


def add(i):
    """得到114个add函数对应的的字符串"""
    return ".add(user_id_list[" + str(i) + "][0], \n" \
            "\tpeople[" + str(i) + "], \n" \
            "\txaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'), \n" \
            "\tyaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'), \n" \
            "\tzaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'), \n" \
            "\tgrid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100)," \
            "\n)"


def print_add():
    """打印输出add函数的字符串"""
    people_item = get_people_item()
    user_id_list = get_user_id_list(people_item)
    for i in range(0, len(user_id_list)):
        print(add(i))


def line3d() -> Line3D:
    people_item = get_people_item()
    user_id_list = get_user_id_list(people_item)
    data = get_data()
    people = get_people(user_id_list, data)
    color = get_color()
    pieces = get_pieces(color)
    c = (
        Line3D()
            .add(user_id_list[0][0],
                 people[0],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[1][0],
                 people[1],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[2][0],
                 people[2],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[3][0],
                 people[3],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[4][0],
                 people[4],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[5][0],
                 people[5],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[6][0],
                 people[6],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[7][0],
                 people[7],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[8][0],
                 people[8],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[9][0],
                 people[9],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[10][0],
                 people[10],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[11][0],
                 people[11],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[12][0],
                 people[12],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[13][0],
                 people[13],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[14][0],
                 people[14],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[15][0],
                 people[15],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[16][0],
                 people[16],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[17][0],
                 people[17],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[18][0],
                 people[18],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[19][0],
                 people[19],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[20][0],
                 people[20],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[21][0],
                 people[21],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[22][0],
                 people[22],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[23][0],
                 people[23],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[24][0],
                 people[24],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[25][0],
                 people[25],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[26][0],
                 people[26],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[27][0],
                 people[27],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[28][0],
                 people[28],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[29][0],
                 people[29],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[30][0],
                 people[30],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[31][0],
                 people[31],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[32][0],
                 people[32],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[33][0],
                 people[33],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[34][0],
                 people[34],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[35][0],
                 people[35],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[36][0],
                 people[36],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[37][0],
                 people[37],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[38][0],
                 people[38],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[39][0],
                 people[39],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[40][0],
                 people[40],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[41][0],
                 people[41],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[42][0],
                 people[42],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[43][0],
                 people[43],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[44][0],
                 people[44],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[45][0],
                 people[45],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[46][0],
                 people[46],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[47][0],
                 people[47],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[48][0],
                 people[48],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[49][0],
                 people[49],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[50][0],
                 people[50],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[51][0],
                 people[51],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[52][0],
                 people[52],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[53][0],
                 people[53],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[54][0],
                 people[54],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[55][0],
                 people[55],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[56][0],
                 people[56],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[57][0],
                 people[57],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[58][0],
                 people[58],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[59][0],
                 people[59],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[60][0],
                 people[60],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[61][0],
                 people[61],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[62][0],
                 people[62],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[63][0],
                 people[63],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[64][0],
                 people[64],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[65][0],
                 people[65],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[66][0],
                 people[66],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[67][0],
                 people[67],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[68][0],
                 people[68],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[69][0],
                 people[69],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[70][0],
                 people[70],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[71][0],
                 people[71],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[72][0],
                 people[72],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[73][0],
                 people[73],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[74][0],
                 people[74],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[75][0],
                 people[75],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[76][0],
                 people[76],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[77][0],
                 people[77],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[78][0],
                 people[78],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[79][0],
                 people[79],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[80][0],
                 people[80],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[81][0],
                 people[81],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[82][0],
                 people[82],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[83][0],
                 people[83],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[84][0],
                 people[84],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[85][0],
                 people[85],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[86][0],
                 people[86],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[87][0],
                 people[87],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[88][0],
                 people[88],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[89][0],
                 people[89],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[90][0],
                 people[90],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[91][0],
                 people[91],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[92][0],
                 people[92],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[93][0],
                 people[93],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[94][0],
                 people[94],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[95][0],
                 people[95],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[96][0],
                 people[96],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[97][0],
                 people[97],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[98][0],
                 people[98],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[99][0],
                 people[99],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[100][0],
                 people[100],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[101][0],
                 people[101],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[102][0],
                 people[102],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[103][0],
                 people[103],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[104][0],
                 people[104],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[105][0],
                 people[105],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[106][0],
                 people[106],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[107][0],
                 people[107],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[108][0],
                 people[108],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[109][0],
                 people[109],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[110][0],
                 people[110],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[111][0],
                 people[111],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[112][0],
                 people[112],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .add(user_id_list[113][0],
                 people[113],
                 xaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_='value', min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=pieces),
            title_opts=opts.TitleOpts(title="3D折线图"),
        )
    )
    return c


def drow_line3d():
    """调用line3d（）绘制3D折线图"""
    g = line3d()
    # 渲染成html, 可用浏览器直接打开
    g.render('line3D.html')


def scatter3d() -> Scatter3D:
    data = get_data()
    color = get_color()
    pieces = get_pieces(color)
    c = (
        Scatter3D()
            .add("",
                 data,
                 xaxis3d_opts=opts.Axis3DOpts(type_="value", min_='dataMin', max_='dataMax'),
                 yaxis3d_opts=opts.Axis3DOpts(type_="value", min_='dataMin', max_='dataMax'),
                 zaxis3d_opts=opts.Axis3DOpts(type_="value", min_='dataMin', max_='dataMax'),
                 grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
                 )
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=pieces),
            title_opts=opts.TitleOpts("3D散点图"),
        )
    )
    return c


def drow_scatter3d():
    """调用scatter3d()绘制3D散点图"""
    g = scatter3d()
    # 渲染成html, 可用浏览器直接打开
    g.render('scatter3D.html')


if __name__=="__main__":
    drow_effectscatter()
    drow_line3d()
    drow_scatter3d()
