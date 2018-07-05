FROM vinx13/hadoop-base

EXPOSE 50070 8088 8188 19888 10200

COPY entrypoint.sh entrypoint.sh
RUN chmod 755 entrypoint.sh
RUN /usr/local/hadoop/bin/hdfs namenode -format
ENTRYPOINT ./entrypoint.sh
