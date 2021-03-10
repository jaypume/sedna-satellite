
### 说明

1. 数据集和模型已经打包在容器中了
2. 输出路径需要通过环境变量指定，并且挂载对应的主机路径到容器中
3. 需要提前在树莓派上安装好docker

### 启动命令

```shell
docker run -it \
      -v ~/workspace/satellite/output:/root/output \
      -v ~/workspace/satellite/script:/root/script \
      -e OUTPUT_FILE_PATH=/root/output \
      -e SCRIPT_FILE_PATH=/root/script \
      swr.cn-south-1.myhuaweicloud.com/satellite/satellite:darknet
```

### 查看结果

在主机`~/workspace/satellite/output`路径下可以看到预测结果的图片生成。


### 脚本覆盖

把新的推理脚本放到主机路径的 `~/workspace/satellite/script`（根据卫星给定的路径，并且在docker启动命令中做对应的修改），

推理脚本约束：

- 名称为 *inference.py*
- 包含一个无参方法 *run()*
- 可以不提供覆盖脚本，这种情况会调用镜像中的yolov2_dota模型  