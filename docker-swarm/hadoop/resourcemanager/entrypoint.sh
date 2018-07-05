#!/bin/sh
export HADOOP_PREFIX=/usr/local/hadoop
echo 'Starting sshd...'
service ssh start
echo 'Starting yarn...'
$HADOOP_PREFIX/sbin/start-yarn.sh
echo 'Starting history server...'
$HADOOP_PREFIX/sbin/mr-jobhistory-daemon.sh start historyserver
$HADOOP_PREFIX/sbin/yarn-daemon.sh start timelineserver
bash
