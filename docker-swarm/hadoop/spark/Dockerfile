FROM vinx13/hadoop-base

MAINTAINER WuweiLin <wuwei.lin@outlook.com>

WORKDIR /opt

RUN wget https://mirrors.aliyun.com/apache/spark/spark-2.3.1/spark-2.3.1-bin-hadoop2.7.tgz && tar xzf spark-2.3.1-bin-hadoop2.7.tgz && mv spark-2.3.1-bin-hadoop2.7 spark && rm spark-2.3.1-bin-hadoop2.7.tgz

WORKDIR /opt/spark
ENV SPARK_HOME /opt/spark
COPY spark-defaults.conf $SPARK_HOME/conf/spark-defaults.conf

ENTRYPOINT ["/bin/bash"]

EXPOSE 4040
