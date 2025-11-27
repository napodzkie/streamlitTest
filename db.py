import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Read DB URL from Streamlit secrets
try:
    DATABASE_URL = st.secrets["database"]["url"]
except Exception:
    DATABASE_URL = None

Base = declarative_base()

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True)
    lat = Column(String, nullable=True)
    lng = Column(String, nullable=True)
    type = Column(String, nullable=False)
    desc = Column(Text, nullable=True)
    time = Column(String, nullable=True)
    distance = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Add Report and Notification classes similarly

def _engine_and_session():
    if not DATABASE_URL:
        return None, None
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return engine, SessionLocal

def init_db():
    engine, _ = _engine_and_session()
    if not engine:
        return False
    try:
        Base.metadata.create_all(bind=engine)
        return True
    except Exception as e:
        st.error(f"DB init error: {e}")
        return False

def get_incidents():
    engine, SessionLocal = _engine_and_session()
    if not engine:
        return []
    sess = SessionLocal()
    try:
        rows = sess.query(Incident).all()
        return [
            {
                "id": r.id,
                "lat": float(r.lat) if r.lat else None,
                "lng": float(r.lng) if r.lng else None,
                "type": r.type,
                "desc": r.desc,
                "time": r.time,
                "distance": r.distance,
                "timestamp": r.timestamp
            }
            for r in rows
        ]
    finally:
        sess.close()
