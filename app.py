from flask import Flask, render_template, jsonify
from models import db, NetworkStat
from monitor import monitor_loop
from threading import Thread
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///network.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
  db.create_all()

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/data')
def data():
  stats = NetworkStat.query.order_by(NetworkStat.timestamp.desc()).limit(60).all()
  stats.reverse()
  return jsonify([
    {
      "timestamp": s.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
      "latency": s.latency,
      "throughput": s.throughput,
      "bandwidth": s.bandwidth
    }
    for s in stats
  ])

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 10000))
  thread = Thread(target=monitor_loop, args=(app,))
  thread.daemon = True
  thread.start()
  app.run(debug=False, host='0.0.0.0', port=port)
