FROM vinx13/hadoop-base

EXPOSE 50075 8042

COPY entrypoint.sh entrypoint.sh
RUN chmod 755 entrypoint.sh

ENTRYPOINT ./entrypoint.sh
