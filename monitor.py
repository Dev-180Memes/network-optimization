import subprocess
import time
import threading
import speedtest
from models import db, NetworkStat
from datetime import datetime

def ping_latency(host):
  try:
    output = subprocess.check_output(['ping', '-c', '1', host], stderr=subprocess.DEVNULL).decode()
    for line in output.splitlines():
      if "time=" in line:
        return float(line.split("time=")[-1].split()[0])
  except:
    return None

def get_bandwidth():
  try:
    s = speedtest.Speedtest()
    s.get_best_server()
    download_speed = s.download() / 1e6  # Convert to Mbps
    return round(download_speed, 2)
  except:
    return None

def get_throughput():
  try:
    # Simulate throughput via localhost iperf3 test
    result = subprocess.check_output(["iperf3", "-c", "localhost", "-t", "2"], stderr=subprocess.DEVNULL).decode()
    for line in result.splitlines():
      if "sender" in line and "Mbits/sec" in line:
        return float(line.split()[-2])
  except:
    return None

def monitor_loop(app, host='8.8.8.8'):
  while True:
    with app.app_context():
      latency = ping_latency(host)
      bandwidth = get_bandwidth()
      throughput = get_throughput()

      stat = NetworkStat(
        host=host,
        latency=latency,
        bandwidth=bandwidth,
        throughput=throughput
      )
      db.session.add(stat)
      db.session.commit()
      time.sleep(60)  # every minute
