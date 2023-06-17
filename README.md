# Htu_CatchClassScript
是否因为土豆服务器根本打不开网页，显示出来课都没了，只得卑微求课，或者含泪买课。

如果人力不行，那就试试代码吧´･ᴗ･`
## First step:(准备工作)
登陆教务系统官网
按键盘的F12键
选择上方的网络(NetWork)
找到welcomePage(没有看见就刷新一下页面)，
往下拉，找到你的user-agent以及cookies复制下来，要的是:右边的一串
## Second step: （这是在显示可选课表后进行时间排查）
记住选课页面的总页数
打开ifChoose，将复制到的user-agent粘贴到user-agent中
然后run，
粘贴useragent，再粘贴cookies，再输入选课页数，
输入0可以排查课程是否冲突，并且以文档的形式保存到crouse.txt和result.txt中，之后运行writeAll可以将课程和是否冲突写入Excel
，选课就输入课程前面的序号。

下面就是等待时间了

___________
因为代码写的有点💩，还在优化加功能，目前就先放一个简易版本的集成包(用来抢公共选修课的)，萌新，轻喷
