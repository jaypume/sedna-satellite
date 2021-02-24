
### 说明

1. 数据集和模型已经打包在容器中了
2. 输出路径需要通过换届变量指定，并且挂载对应的主机路径到容器中

### 启动命令

```shell
docker run -it -v ~/workspace/satellite/output:/root/output --env OUTPUT_FILE_PATH=/root/output swr.cn-south-1.myhuaweicloud.com/satellite/satellite:darknet
```

### 查看结果

在主机`~/workspace/satellite/output`路径下可以看到预测结果的图片生成。
