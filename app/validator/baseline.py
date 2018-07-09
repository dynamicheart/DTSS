import json
from datetime import datetime

base_rate_table = {
    'RMB': 2.0,
    'USD': 12.0,
    'JPY': 0.5,
    'EUR': 6.0
}

start_time = datetime.strptime('2018-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

# Reading test data
with open('./test_data/test_data_0.json') as f:
  data0 = json.load(f)
with open('./test_data/test_data_1.json') as f:
  data1 = json.load(f)
with open('./test_data/test_data_2.json') as f:
  data2 = json.load(f)

results = {}
def process_order(order):
    time_str = order['time'][:-3]
    order_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
    time_diff = order_time - start_time
    minute_diff = int(time_diff.total_seconds() / 60)

    src_expend = float(order['value']);
    dst_income = order['value'] * \
        (base_rate_table[order['src_name']] + (0.1 * minute_diff)) / \
        (base_rate_table[order['dst_name']] + (0.1 * minute_diff))

    src_key = order['src_name'] + str(minute_diff) 
    if src_key in results:
        results[src_key]['expend'] += src_expend
    else:
        results[src_key] = {
            'name': order['src_name'],
            'income': 0.0,
            'expend': src_expend,
            'time': order_time.strftime('%Y-%m-%d %H:%M')
        }

    dst_key = order['dst_name'] + str(minute_diff) 
    if dst_key in results:
        results[dst_key]['income'] += dst_income
    else:
        results[dst_key] = {
            'name': order['dst_name'],
            'income': dst_income,
            'expend': 0.0,
            'time': order_time.strftime('%Y-%m-%d %H:%M')
        }

# Order processing
for i, order in enumerate(data0):
    process_order(order)
for i, order in enumerate(data1):
    process_order(order)
for i, order in enumerate(data2):
    process_order(order)

# Show resultss
for result in results.values():
    print(result)
