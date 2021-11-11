
# celery安装以及所需环境安装
## windows 安装

celery参考网址
```shell
https://blog.csdn.net/cuomer/article/details/81214438
```

所需python环境，切换到项目环境下，安装celery
```shell
pip install celery
pip install redis
```

### Redis数据库安装
官网安装方法 https://redis.io/download

**windows**
```shell
下载地址：https://github.com/tporadowski/redis/releases。
```

Redis支持32位和64位。这个需要根据你系统平台的实际情况选择，我们选择下载 Redis-x64-xxx.zip压缩包到D盘，解压后，将文件夹重新命名为redis。

![Image text](https://www.runoob.com/wp-content/uploads/2014/11/3B8D633F-14CE-42E3-B174-FCCD48B11FF3.jpg)

打开一个 cmd 窗口 使用 cd 命令切换目录到 D:\redis 运行：
```shell
redis-server.exe redis.windows.conf
```

运行结果如下：

![Image text](https://www.runoob.com/wp-content/uploads/2014/11/redis-install1.png)

这时候另启一个 cmd 窗口，原来的不要关闭，不然就无法访问服务端了。
将新启动的cmd窗口，切换到自己项目的根目录（task.py）文件的上一层目录，输入:
```shell
celery -A app.celery_app.task worker --loglevel=info
```

根据设备不同，可能会出现类似错误

```shell
[2018-01-12 19:08:15,545: INFO/MainProcess] Received task: tasks.add[5d387722-5389-441b-9b01-a619b93b4702]
[2018-01-12 19:08:15,550: ERROR/MainProcess] Task handler raised error: ValueError('not enough values to unpack (expected 3, got 0)',)
Traceback (most recent call last):
  File "d:\programmingsoftware\python35\lib\site-packages\billiard\pool.py", line 358, in workloop
    result = (True, prepare_result(fun(*args, **kwargs)))
  File "d:\programmingsoftware\python35\lib\site-packages\celery\app\trace.py", line 525, in _fast_trace_task
    tasks, accept, hostname = _loc
ValueError: not enough values to unpack (expected 3, got 0)
```
如果出现如上错误，解决方法如下：
```shell
pip install eventlet
```

然后在启动worker的时候加一个参数，如下：
```shell
celery -A <mymodule>.celery_task  worker --loglevel=info -P eventlet
```
**Linux**
```bash
wget https://download.redis.io/redis-stable.tar.gz && \
tar -xvzf redis-stable.tar.gz && \
mv redis-stable/ redis && \
rm -f redis-stable.tar.gz && \
yum clean all && \
cd redis && \
make && make PREFIX=/usr/local/redis install && \
mkdir -p /usr/local/redis/conf/ && \
cp /home/redis/redis.conf  /usr/local/redis/conf/  && \
sed -i '69s/127.0.0.1/0.0.0.0/' /usr/local/redis/conf/redis.conf && \
sed -i '88s/protected-mode yes/protected-mode no/' /usr/local/redis/conf/redis.conf
```
当看到如下输出：

![Image text](https://img-blog.csdn.net/20170714134724989?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZnJlZWtpbmcxMDE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

出现celery@XXX ready时，则启动成功，随后启动我们flask接口服务，异步接口就启动成功了！





## Linux 安装

首先在项目容器下，同样安装celery，redis所需要环境
```shell
pip3 install celery
pip3 install redis
```

### 下载，解压并安装Redis

#### 下载

安装好包以后，需要安装redis数据库
输入一下命令：
```shell
curl https://download.redis.io/redis-stable.tar.gz -o redis-stable.tar.gz
```
#### 解压
下载完成后需要将压缩文件解压，输入以下命令解压到当前目录

```shell
tar -zvxf redis-stable.tar.gz
```
移动redis目录

```shell
mv /home/redis-stable /usr/local/redis
```

#### 编译

cd到/usr/local/redis目录，输入命令make执行编译命令，接下来控制台会输出各种编译过程中输出的内容。

```shell
make
```

最终效果如下：

![Image text](https://img2018.cnblogs.com/i-beta/349354/202002/349354-20200213181414604-1780484458.png)

#### 安装

输入以下命令

```shell
make PREFIX=/usr/local/redis install
```

执行结果如下图:

![Image text](https://img2018.cnblogs.com/i-beta/349354/202002/349354-20200213181518488-529232514.png)


#### 启动redis
复制配置文件到创建的配置文件目录
```bash
mkdir -p /usr/local/redis/conf/
cp /home/redis/redis.conf  /usr/local/redis/conf/  
```
添加环境变量
```bash
vim /etc/profile
```
```vim
PATH=$PATH:/usr/local/redis/bin
PATH=$PATH:/usr/local/redis/conf

```
激活环境变量
```bash
source /etc/profile
```
启动redis服务
```bash
redis-server redis.conf
```
```shell
./bin/redis-server& ./redis.conf
```
在Linux系统上，redis数据库已经下载完成，并且启动，此时，跟windows系统上的流程一样：
#### 启动celery worker
切换到项目目录下，输入
```shell
celery -A <mymodule>.celery_task  worker --loglevel=info
```
成功以后，就可以运行flask接口服务文件，异步接口就启动成功了！


# celery使用方法

## 参考网址

关于celery的使用方法可以参考一下网址：

celery
```shell
https://www.jianshu.com/p/46fe82fe474b
http://www.pythondoc.com/flask-celery/first.html
https://www.jianshu.com/p/419bf97507a5
https://www.cnblogs.com/yangjian319/p/9097171.html
https://blog.csdn.net/chen801090/article/details/100983643
https://docs.celeryproject.org/en/stable/userguide/tasks.html
https://blog.csdn.net/blackj_liuyun/article/details/79691701
https://www.jianshu.com/p/a505463ca840
http://www.bjhee.com/celery.html
```

## celery 简单介绍

```shell

Celery 是一个异步任务队列，一个Celery有三个核心组件：

Celery 客户端: 用于发布后台作业；当与 Flask 一起工作的时候，客户端与 Flask 应用一起运行。

Celery workers: 运行后台作业的进程。Celery 支持本地和远程的 workers，可以在本地服务器上启动一个单独的 worker，也可以在远程服务器上启动worker，需要拷贝代码；

消息代理: 客户端通过消息队列和 workers 进行通信，Celery 支持多种方式来实现这些队列。最常用的代理就是 RabbitMQ 和 Redis。
```

## Celery有以下优点

```shell
简单：一单熟悉了celery的工作流程后，配置和使用还是比较简单的

高可用：当任务执行失败或执行过程中发生连接中断，celery 会自动尝试重新执行任务

快速：一个单进程的celery每分钟可处理上百万个任务

灵活： 几乎celery的各个组件都可以被扩展及自定制
```
## Celery基本工作流程图

![Image text](https://img.jbzj.com/file_images/article/201907/20197891513281.png?20196892054)


###  常用的需要配置的参数

```shell
main:如果作为__main__运行，则为主模块的名称。用作自动生成的任务名称的前缀
loader:当前加载器实例。
backend:任务结果url；
amqp:AMQP对象或类名，一般不管；
log:日志对象或类名；
set_as_current:将本实例设为全局当前应用
tasks:任务注册表。
broker:使用的默认代理的URL,任务队列；
include:每个worker应该导入的模块列表，以实例创建的模块的目录作为起始路径；
```
这些参数都是celery实例化的配置，我们也可以不写，然后使用config_from_object方法加载配置；

### 创建异步任务的方法task参数

#### 方法相关的参数
```shell
exc:失败时的错误的类型；
task_id:任务的id；
args:任务函数的参数；
kwargs:键值对参数；
einfo:失败或重试时的异常详细信息；
retval:任务成功执行的返回值；
```

#### Task的一般属性

```shell
Task.name:任务名称；
Task.request：当前任务的信息；
Task.max_retries：设置重试的最大次数
Task.throws：预期错误类的可选元组，不应被视为实际错误，而是结果失败；
Task.rate_limit：设置此任务类型的速率限制
Task.time_limit：此任务的硬限时（以秒为单位）。
Task.ignore_result：不存储任务状态。默认False；
Task.store_errors_even_if_ignored：如果True，即使任务配置为忽略结果，也会存储错误。
Task.serializer：标识要使用的默认序列化方法的字符串。
Task.compression：标识要使用的默认压缩方案的字符串。默认为task_compression设置。
Task.backend：指定该任务的结果存储后端用于此任务。
Task.acks_late：如果设置True为此任务的消息将在任务执行后确认 ，而不是在执行任务之前（默认行为），即默认任务执行之前就会发送确认；
Task.track_started：如果True任务在工作人员执行任务时将其状态报告为“已启动”。默认是False；
```

#### 调用异步任务

调用异步任务有三个方法，如下：

```shell
task.delay():这是apply_async方法的别名,但接受的参数较为简单；

task.apply_async(args=[arg1, arg2], kwargs={key:value, key:value})：可以接受复杂的参数;

send_task():可以发送未被注册的异步任务，即没有被celery.task装饰的任务；
```

#### 1. app.send_task
```shell
# tasks.py
from celery import Celery
app = Celery('tasks', backend='redis://localhost', broker='pyamqp://')
def add(x,y):
    return x+y

app.send_task('tasks.add',args=[3,4])  # 参数基本和apply_async函数一样
# 但是send_task在发送的时候是不会检查tasks.add函数是否存在的，即使为空也会发送成功，所以celery执行是可能找不到该函数报错；
```

#### 2. Task.delay
delay方法是apply_async方法的简化版，不支持执行选项，只能传递任务的参数。
```shell
@app.task
def add(x, y, z=0):
    return x + y

add.delay(30,40,z=5) # 包括位置参数和关键字参数
```

#### 3. Task.apply_async
apply_async支持执行选项，它会覆盖全局的默认参数和定义该任务时指定的执行选项，本质上还是调用了send_task方法；
```shell
add.apply_async(args=[30,40], kwargs={'z':5})

# 其他参数
task_id:为任务分配唯一id，默认是uuid;
countdown : 设置该任务等待一段时间再执行，单位为s；
eta : 定义任务的开始时间；eta=time.time()+10;
expires : 设置任务时间，任务在过期时间后还没有执行则被丢弃；
retry : 如果任务失败后, 是否重试;使用true或false，默认为true
shadow：重新指定任务的名字str，覆盖其在日志中使用的任务名称；
retry_policy : {},重试策略.如下：
    max_retries : 最大重试次数, 默认为 3 次.
    interval_start : 重试等待的时间间隔秒数, 默认为 0 , 表示直接重试不等待.
    interval_step : 每次重试让重试间隔增加的秒数, 可以是数字或浮点数, 默认为 0.2
    interval_max : 重试间隔最大的秒数, 即 通过 interval_step 增大到多少秒之后, 就不在增加了, 可以是数字或者浮点数, 默认为 0.2 .

routing_key:自定义路由键；
queue：指定发送到哪个队列；
exchange：指定发送到哪个交换机；
priority：任务队列的优先级，0到255之间，对于rabbitmq来说0是最高优先级；
serializer：任务序列化方法；通常不设置；
compression：压缩方案，通常有zlib, bzip2
headers：为任务添加额外的消息；
link：任务成功执行后的回调方法；是一个signature对象；可以用作关联任务；
link_error: 任务失败后的回调方法，是一个signature对象；

# 如下
add.apply_async((2, 2), retry=True, retry_policy={
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2,
})

#自定义发布者,交换机,路由键, 队列, 优先级,序列方案和压缩方法:
task.apply_async((2,2), 
    compression='zlib',
    serialize='json',
    queue='priority.high',
    routing_key='web.add',
    priority=0,
    exchange='web_exchange')
```

#### 获取任务结果和状态

由于celery发送的都是去其他进程执行的任务，如果需要在客户端监控任务的状态，有如下方法：

```shell
r = task.apply_async()
r.ready()     # 查看任务状态，返回布尔值,  任务执行完成, 返回 True, 否则返回 False.
r.wait()      # 会阻塞等待任务完成, 返回任务执行结果，很少使用；
r.get(timeout=1)       # 获取任务执行结果，可以设置等待时间，如果超时但任务未完成返回None；
r.result      # 任务执行结果，未完成返回None；
r.state       # PENDING, START, SUCCESS，任务当前的状态
r.status      # PENDING, START, SUCCESS，任务当前的状态
r.successful  # 任务成功返回true
r.traceback  # 如果任务抛出了一个异常，可以获取原始的回溯信息
```
但是一般业务中很少用到，因为获取任务执行的结果需要阻塞，celery使用场景一般是不关心结果的。