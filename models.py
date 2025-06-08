from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class NetworkStat(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  timestamp = db.Column(db.DateTime, default=datetime.utcnow)
  host = db.Column(db.String(120), nullable=False)
  latency = db.Column(db.Float)        # in ms
  throughput = db.Column(db.Float)     # in Mbps
  bandwidth = db.Column(db.Float)      # in Mbps
