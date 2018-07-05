import time
import os

from kazoo.client import KazooClient

zk_hosts = os.environ['RATER_ZK_HOSTS']
currency_name = os.environ['RATER_CURRENCY_NAME']
exchange_rate = float(os.environ['RATER_INIT_EXCHANGE_RATE'])
run_time = int(os.environ['RATER_RUN_TIME'])

zk = KazooClient(hosts=zk_hosts)
zk.start()

if zk.exists('/' + currency_name):
    zk.delete('/' + currency_name, recursive=True)

minute_cnt = 0
while minute_cnt <= run_time:
    # The node path format is currency_name/minute
    zk.create('/' + currency_name + '/' + str(minute_cnt), bytes(exchange_rate), makepath=True)
    exchange_rate *= 0.1
    minute_cnt += 1

    time.sleep(60)

zk.stop()
