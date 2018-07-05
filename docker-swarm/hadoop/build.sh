#!/bin/bash
PREFIX=registry-vpc.cn-hongkong.aliyuncs.com
NS=vinx13
function build() {
  DIR=$1
  IMAGE_NAME=$NS/$2
  NAME=$PREFIX/$IMAGE_NAME
  cd $DIR
  docker build . -t $IMAGE_NAME
  docker tag $IMAGE_NAME $NAME
  docker push $NAME
  cd -
}
build base hadoop-base
build namenode hadoop-namenode
build datanode hadoop-datanode
build resourcemanager resource-manager
build spark spark
