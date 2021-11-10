Basic Project Structure
# 项目环境
## 克隆整个项目
```bash
git clone https://github.com/NanZhang1991/ai-framework.git
```

## 运行环境
### redis installation
from source code 
Download, extract and compile Redis with:
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
Adding environment variables
```bash
vim /etc/profile
```
```vim
PATH=$PATH:/usr/local/redis/bin
```
激活环境变量
```
source /etc/profile
```

**ai-frameword(项目根目录) 目录下**
### python 环境
```bash
pip install -r requirements.txt
```

## start celery
linux
```bash
celery -A app.celery_app.task worker --loglevel=info
```
# service
## 启动服务
```bash
python server.py
```
## 测试
```bash
python -m unittest
```
## 后台启动
```
nohup python3 server.py >/dev/null 2>&1 &
```

# Docker部署
## 构建镜像
```bash
docker build -t forp/ai-framework:base .
# 若代码更新则不使用缓存
docker build -t forp/ai-framework:base . --no-cache
```
## 运行容器
```bash
docker run --gpus all -itd --restart=unless-stopped --name="ai-framework" -e PROFILES_ACTIVE="test" forp/ai-framework:base
## 若不使用gpu则去掉--gpus all 参数
```
默认部署环境为**开发环境**
deploy_config文件夹下用于存放develop test product 环境的配置文件
通过 修改参数-e PROFILES_ACTIVE 变量值 在运行env/run.sh 脚本时重新配置app/config/deploy.json文件


# service
## Task_start
### Service request
**psot**: ip:8000/api/task_start </bar>
**parameters**: file,
**input_json**
### Service response
```json
{"code":200,
 "data":"xxxx",
 "msg":"success"}
```
## Task_status
### Service request
**get** ip:8000/api/task_status </bar>
**parameters**: id 
### Service response
```json
{"code":200,
 "data":"xxxx",
 "msg":"success"}
```
 
# 代码行数统计
```bash
python count_lines.py
```
# 把所有代码写入word
```bash
python write_code_word.py
```