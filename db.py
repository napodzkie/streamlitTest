# db.py
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from typing import List, Dict, Optional

# -----------------------------
# Database URL from Streamlit Secrets
# -----------------------------
try:
    DATABASE_URL = st.secrets["database"]["url"]
except Exception:
    DATABASE_URL = None

# Ensure SSL for Supabase
if DATABASE_URL and "supabase.co" in DATABASE_URL and "sslmode" not in DATABASE_URL:
    if "?" in DATABASE_URL:
        DATABASE_URL += "&sslmode=require"
    else:
        DATABASE_URL += "?sslmode=require"

# -----------------------------
# SQLAlchemy Base
# -----------------------------
Base = declarative_base()

# -----------------------------
# Tables
# -----------------------------
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

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    desc = Column(Text, nullable=True)
    time = Column(String, nullable=True)
    unread = Column(String, default="true")
    timestamp = Column(DateTime, default=datetime.utcnow)

# -----------------------------
# Engine and Session
# -----------------------------
def _engine_and_session():
    if not DATABASE_URL:
        return None, None
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return engine, SessionLocal

# -----------------------------
# DB Initialization
# -----------------------------
def init_db() -> bool:
    engine, _ = _engine_and_session()
    if not engine:
        st.error("DATABASE_URL not found in secrets!")
        return False
    try:
        Base.metadata.create_all(bind=engine)
        return True
    except Exception as e:
        st.error(f"Database initialization error: {e}")
        return False

# -----------------------------
# CRUD Functions
# -----------------------------
def get_incidents() -> List[Dict]:
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

def get_reports() -> List[Dict]:
    engine, SessionLocal = _engine_and_session()
    if not engine:
        return []
    sess = SessionLocal()
    try:
        rows = sess.query(Report).all()
        return [
            {
                "id": r.id,
                "type": r.type,
                "description": r.description,
                "location": r.location,
                "timestamp": r.timestamp,
                "status": r.status
            }
            for r in rows
        ]
    finally:
        sess.close()

def get_notifications() -> List[Dict]:
    engine, SessionLocal = _engine_and_session()
    if not engine:
        return []
    sess = SessionLocal()
    try:
        rows = sess.query(Notification).all()
        return [
            {
                "id": r.id,
                "title": r.title,
                "desc": r.desc,
                "time": r.time,
                "unread": True if r.unread == "true" else False,
                "timestamp": r.timestamp
            }
            for r in rows
        ]
    finally:
        sess.close()

def add_incident(lat: Optional[float], lng: Optional[float], type_: str, desc: str, time_str: str, distance: str) -> int:
    engine, SessionLocal = _engine_and_session()
    if not engine:
        raise RuntimeError("DATABASE_URL not configured!")
    sess = SessionLocal()
    try:
        i = Incident(
            lat=str(lat) if lat is not None else None,
            lng=str(lng) if lng is not None else None,
            type=type_,
            desc=desc,
            time=time_str,
            distance=distance
        )
        sess.add(i)
        sess.commit()
        sess.refresh(i)
        return i.id
    finally:
        sess.close()

def add_report(type_: str, description: str, location: Optional[str] = None) -> int:
    engine, SessionLocal = _engine_and_session()
    if not engine:
        raise RuntimeError("DATABASE_URL not configured!")
    sess = SessionLocal()
    try:
        r = Report(type=type_, description=description, location=location)
        sess.add(r)
        sess.commit()
        sess.refresh(r)
        return r.id
    finally:
        sess.close()

def add_notification(title: str, desc: str, time_str: str, unread: bool = True) -> int:
    engine, SessionLocal = _engine_and_session()
    if not engine:
        raise RuntimeError("DATABASE_URL not configured!")
    sess = SessionLocal()
    try:
        n = Notification(title=title, desc=desc, time=time_str, unread="true" if unread else "false")
        sess.add(n)
        sess.commit()
        sess.refresh(n)
        return n.id
    finally:
        sess.close()

def mark_all_notifications_read():
    engine, SessionLocal = _engine_and_session()
    if not engine:
        raise RuntimeError("DATABASE_URL not configured!")
    sess = SessionLocal()
    try:
        sess.query(Notification).filter(Notification.unread == "true").update({"unread": "false"})
        sess.commit()
    finally:
        sess.close()
