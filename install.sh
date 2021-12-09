image_name="forp/ai-framework:base"
contains_name="ai-framework" 
port="8000:8000"

#如果容器存在删除
export contains_name

if [[ -n $(docker ps | grep $contains_name) ]];then
	echo "$contains_name has been installed, older versions will be uninstalled"
    docker rm -f $contains_name
fi

#如果镜像存在，则删除
export image_name

docker inspect $image_name --format='{{.LogPath}}' 2> /dev/nul
if [ $? -eq 0 ];then
    echo "$image_name is existed,we will remove it!!!"
    docker rmi $image_name
else
    echo "$image_name is not existed!!!"
fi

## 构建镜像
# docker build -t $image_name .
docker build -t $image_name . --no-cache
# 运行容器 
docker run --gpus all -itd --restart=unless-stopped --name=$contains_name -e PROFILES_ACTIVE="dev" -p $port $image_name \
&& echo "Finish  $contains_name installation"
