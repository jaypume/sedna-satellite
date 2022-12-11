# 基于Sedna边云协同的卫星遥感农田面积统计


## 0.环境说明

**边侧**：
```
硬件： 树莓派 3B+
规格:                                                                                                                                                                                         
 OS: Raspbian 10 buster                                                                                                                                                                                 
 Kernel: armv7l Linux 5.10.11-v7+                                                                                                                                                                       
 CPU: ARMv7 rev 4 (v7l) @ 4x 800MHz                                                                                                                                                            
```
系统软件：
[2020-08-20-raspios-buster-armhf-full.img](http://mirrors4.hit.edu.cn/raspberry-pi-os-images/raspios_full_armhf/images/raspios_full_armhf-2020-08-24/)

**云端虚拟机**：  
- 具备网络连接
- 具备推理能力
- 不限架构



**使用到的测试集：**
- DOTA数据集： https://captain-whu.github.io/DOTA/dataset.html  
- 其他相关数据集：https://sites.google.com/view/zhouwx/dataset


## 1.烧录镜像

参考烧录步骤：https://stepneverstop.github.io/burn-system2raspberry-in-macos.html

1. format disk卡
2. 开始烧录
```
diskutil unmountDisk /dev/disk2
sudo dd if=～/Downloads/2020-08-20-raspios-buster-armhf-full.img of=/dev/disk2 bs=4m;sync
```

## 2. 树莓派安装Docker
参考[这里](https://yeasy.gitbook.io/docker_practice/install/raspberry-pi)在树莓派上安装Docker。


提示找不到模板，可以参考[这里](https://blog.csdn.net/xuancuo8078/article/details/113180636)解决。


## 3. 构建边侧推理镜像

```
docker build -f build/darknet.Dockerfile . \
-t swr.cn-south-1.myhuaweicloud.com/satellite/satellite:darknet \
--build-arg HTTP_PROXY=http://192.168.2.1:7890  \
--build-arg HTTPS_PROXY=http://192.168.2.1:7890
```
注意：
- 把其中的镜像名称修改为自己的镜像名称。
- build不成功的话通常可能是代理原因，build成功的话可以省略代理配置。

## 4. 验证边侧推理镜像

```
docker run -it \
-v ~/workspace/satellite/output:/root/output \
-v ~/workspace/satellite/script:/root/script \
-e OUTPUT_FILE_PATH=/root/output \
-e SCRIPT_FILE_PATH=/root/script \
-e COMMAND_LINE=tiny \
swr.cn-south-1.myhuaweicloud.com/satellite/satellite:darknet
```

参数说明：
- OUTPUT_FILE_PATH： 输出结果的路径
- SCRIPT_FILE_PATH： 被注入的实际推理脚本路径，构建的镜像中只是个基本运行框架。
- COMMAND_LINE： tiny表示使用tiny yolov3模型进行推理


yolov3-tiny相关主页：https://pjreddie.com/darknet/yolo/

本样例中使用的yolov3-tiny.weights预训练模型文件可以从[这里](https://pjreddie.com/media/files/yolov3-tiny.weights)下载，放置在本仓库目录./models下即可。














