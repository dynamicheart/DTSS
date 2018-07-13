import time
import os
import json
import logging

from kazoo.client import KazooClient

logging.basicConfig(level=logging.DEBUG)

init_rate_table = [
    { 'currency': 'RMB', 'init_rate': 2.0 },
    { 'currency': 'USD', 'init_rate': 12.0 },
    { 'currency': 'JPY', 'init_rate': 0.5 },
    { 'currency': 'EUR', 'init_rate': 6.0 }
    ]

def init():
    zk_hosts = os.environ['RATER_ZK_HOSTS']
    zk = KazooClient(hosts=zk_hosts)
    zk.start()

    if zk.exists('/rate_table'):
        zk.delete('/rate_table', recursive=True)

    zk.stop()

def run(idx):
    zk_hosts = os.environ['RATER_ZK_HOSTS']
    run_time = int(os.environ['RATER_RUN_TIME'])
    currency_name = init_rate_table[idx]['currency']
    exchange_rate = init_rate_table[idx]['init_rate']

    zk = KazooClient(hosts=zk_hosts)
    zk.start()

    minute_cnt = 0
    while minute_cnt <= run_time:
        # Create a new rate table if not exists
        if not zk.exists('/rate_table/' + str(minute_cnt)):
            list_lock = zk.Lock('/rate_table/list_lock', 'list_lock')
            with list_lock:
                if not zk.exists('/rate_table/' + str(minute_cnt)):
                    raw_rate_table = json.dumps({'RMB': -1, 'USD': -1, 'JPY': -1, 'EUR': -1})
                    zk.create('/rate_table/' + str(minute_cnt), bytes(raw_rate_table), makepath=True)

        # Update rate table 
        table_lock = zk.Lock('/rate_table/lock/' + str(minute_cnt), 'table_lock' + str(minute_cnt))  
        with table_lock:
            byte_rate_table, stat = zk.get('/rate_table/' + str(minute_cnt))
            rate_table = json.loads(str(byte_rate_table))
            rate_table[currency_name] = exchange_rate

            raw_rate_table = json.dumps(rate_table)
            zk.set('/rate_table/' + str(minute_cnt), bytes(raw_rate_table))

        exchange_rate += 0.1
        minute_cnt += 1

        #time.sleep(60)

    zk.stop()

if __name__ == '__main__':
    init()

    pid_list = []
    for i in range(4):
        pid = os.fork()
        if pid == 0:
            run(i)
        else:
            pid_list.append(pid)

    for pid in pid_list:
        os.waitpid(pid, 0)

