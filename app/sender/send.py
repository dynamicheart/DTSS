import os
import subprocess
filenames = ['test_data_1.json', 'test_data_2.json', 'test_data_3.json']
filenames = list(map(lambda f: os.path.join('test_data', f), filenames))

address = 'http://localhost:20080'

for filename in filenames:
  subprocess.Popen(['sender', filename, address])
