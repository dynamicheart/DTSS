#!/bin/sh
export HADOOP_PREFIX=/usr/local/hadoop
echo 'Starting sshd...'
service ssh start
echo 'Starting dfs...'
$HADOOP_PREFIX/sbin/start-dfs.sh
bash
