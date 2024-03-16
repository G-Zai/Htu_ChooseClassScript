#vision: 1.0.1;
#@author: Loading


import json
import time
import requests
import xlwt
from concurrent.futures import ThreadPoolExecutor



havebreak = False

menuuUrl = 'https://jwc.htu.edu.cn/new/student/xsxk/xklx/01/kxkc'
crouseUrl = 'https://jwc.htu.edu.cn/new/student/xsxk/xklx/01/add'


#选课菜单：
def _viewCrouse_():
    response = requests.post(
        url=menuuUrl,
        cookies=cookies,
        headers=headers,
            data={
        'page': '1',
        'rows': '20',
        'sort': 'kcrwdm',
        'order': 'asc',
        }
    )
    res = json.loads(response.text)
    total = res['total']
    number = 0
    crouse = [1] * total
    for page in range(1, allpage+1):
        data = {
            'page': page,
            'rows': '20',
            'sort': 'kcrwdm',
            'order': 'asc',
        }
        response = requests.post(
            url=menuuUrl,
            cookies=cookies,
            headers=headers,
            data=data
        )
        page += 1
        res = json.loads(response.text)

        rows = res['rows']
        total = res['total']
        file_write = open("crouse.txt", mode='w')


        for line in rows:
            kcrwdm=line['kcrwdm']#课程id
            jxbmc=line['jxbmc']#教学班:
            jxbrs=line['jxbrs']#已选人数
            #kcdlmc=line['kcdlmc']#课程类型
            kcmc=line['kcmc']# 课程名称
            pkrs=line['pkrs']#总人数
            teaxm=line['teaxm']#教师
            xf=line['xf']
            kcflmc=line['kcflmc']#课程分类
            #xmmc=line['xmmc']#
            #zxs=line['zxs']#学分
            #将课程id 存放到crouse中
            crouse[number] = [kcrwdm, kcmc, kcflmc]
            number += 1
            print(number, kcmc, kcflmc, teaxm, jxbmc, xf)
            f.write(str(number)+','+kcmc+','+kcflmc+','+teaxm+','+jxbmc+','+str(xf)+'\n')

    choose = input("请输入要选的课程（输入序号，多个数字用,隔开）,若要查看课程是否冲突，输入0(切勿在选课时查看)：")
    global havebreak
    times = 0
    ky = [[0] for i in range(0, total)]
    if choose == '0':
        for ii in range(0, total):
            kc = crouse[ii][0]
            mc = crouse[ii][1]
            kcf = crouse[ii][2]
            ky[times] = [kc, mc, kcf]
            times += 1
        havebreak = True
        for k in ky:
            kcrwdm = k[0]
            mc = k[1]
            kcf = k[2]
            task(kcrwdm, mc)
    else:
        chooseNumbers = choose.split(',')
        num = len(chooseNumbers)
        ky = [[0] for i in range(num)]
        times = 0
        for chooseNumber in chooseNumbers:
            kc = crouse[int(chooseNumber) - 1][0]
            mc = crouse[int(chooseNumber) - 1][1]
            kcf = crouse[int(chooseNumber) - 1][2]
            ky[times] = [kc, mc, kcf]
            times += 1
        with ThreadPoolExecutor(8) as t:
            for k in ky:
                kcrwdm = k[0]
                mc = k[1]
                kcf = k[2]
                t.submit(task, kcrwdm, mc)





#抢课：
def task(kcrwdm,kcmc):
    crouseData = {
        'kcrwdm': kcrwdm,
        'kcmc': kcmc,
        'qz': '-1',
        'hlct': '0',
    }

    while True:
        response = requests.post(
            url=crouseUrl,
            cookies=cookies,
            headers=headers,
            data=crouseData,
        )
        res = json.loads(response.text)
        b.write(res['message']+'\n')
        code = res['code']  # 选课成功参数
        localtime = time.asctime(time.localtime(time.time()))
        if code == 0:
            print(localtime+"选择成功!")
            callback()
            break
        else:
            print(res['message'])
            if havebreak:
                break





# 选择类型：此功能未实现。
def menu():

    pass


# 请选择登录方式（因存在js加密，账号密码登录功能未实现）
def login():
    model= '1'
    if model == '1':
        cook = input('请输入cookie：')

        cooks = cook.split('=')
        co = cooks[0]
        okies = cooks[1]
        cooki = {
            co: okies
        }
    return cooki

# 已选课程
def callback():#classes
    haveUrl = 'https://jwc.htu.edu.cn/new/student/xsxk/xklx/01/yxkc'
    haveData={
        'sort': 'kcrwdm',
        'order': 'asc'
    }
    rspo=requests.post(
        url=haveUrl,
        headers=headers,
        data=haveData,
        cookies=cookies
    )
    res = json.loads(rspo.text)

    rows = res['rows']
    total = res['total']
    for cls in rows:
        kcmc = cls['kcmc']  # 课程名称
        teaxm = cls['teaxm']  # 教师
        xmmc = cls['xmmc']  # 课程内容
        print(kcmc, xmmc, teaxm)

# 将课程写入excel
def writeex():
    f1 = open("crouse.txt", "r", encoding='utf-8')
    b1 = open("result.txt", "r", encoding='utf-8')
    ex = xlwt.Workbook(encoding='utf-8')
    li = ex.add_sheet('first')
    li.write(0, 0, '序号')
    li.write(0, 1, ' 课程名称')
    li.write(0, 2, '课程类型')
    li.write(0, 3, '教师')
    li.write(0, 4, '教学班')
    li.write(0, 5, '学分')
    li.write(0, 6, '结果')
    row = 1
    col = 0
    rows = 1
    for lines in f1:
        sp = lines.split(',')
        for i in sp:
            li.write(row, col, i)
            col += 1
        row += 1
        col = 0
    for rest in b1:
        re = rest.split('\n ')
        for j in re:
            li.write(rows, 6, j)
            rows += 1
    ex.save('总课表.xls')
    f1.close()
    b1.close()


if __name__=="__main__":
    useragent = input('请输入useragent:')
    headers = {
        'authority': 'jwc.htu.edu.cn',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://jwc.htu.edu.cn',
        'referer': 'https://jwc.htu.edu.cn/new/student/xsxk/xklx/01',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': useragent,
        'x-requested-with': 'XMLHttpRequest',
    }

    cookies = login()
    allpage = int(input("请输入课程总页数："))
    f = open("crouse.txt", 'w', encoding='utf-8')
    b = open("result.txt", 'w', encoding='utf-8')
    _viewCrouse_()
    f.close()
    b.close()
    if havebreak:
        writeex()




