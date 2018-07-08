FROM vinx13/hadoop-base

EXPOSE 8032 8088 8188 19888 10200

COPY entrypoint.sh entrypoint.sh
COPY yarn-site.xml $HADOOP_CONF_DIR/yarn-site.xml
RUN chmod 755 entrypoint.sh
ENTRYPOINT ./entrypoint.sh
