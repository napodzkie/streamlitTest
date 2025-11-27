import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Try loading secrets safely
def load_database_url():
    # 1. Streamlit Cloud secrets
    try:
        if "database" in st.secrets:
            return st.secrets["database"]["url"]
    except:
        pass

    # 2. Environment variable (local dev)
    env_url = os.environ.get("DATABASE_URL")
    if env_url:
        return env_url

    return None

DATABASE_URL = load_database_url()
print("LOADED DATABASE_URL:", DATABASE_URL)

# Ensure SSL for Supabase
if DATABASE_URL and "supabase.co" in DATABASE_URL and "sslmode" not in DATABASE_URL:
    if "?" in DATABASE_URL:
        DATABASE_URL += "&sslmode=require"
    else:
        DATABASE_URL += "?sslmode=require"

Base = declarative_base()



class Incident(Base):
    __tablename__ = 'incidents'

    id = Column(Integer, primary_key=True)
    lat = Column(String, nullable=True)
    lng = Column(String, nullable=True)
    type = Column(String, nullable=False)
    desc = Column(Text, nullable=True)
    time = Column(String, nullable=True)
    distance = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='pending')


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    desc = Column(Text, nullable=True)
    time = Column(String, nullable=True)
    unread = Column(String, default='true')
    timestamp = Column(DateTime, default=datetime.utcnow)


def _engine_and_session():
    """Return (engine, Session) if DATABASE_URL exists, otherwise (None, None)."""
    if not DATABASE_URL:
        return None, None

    # Use moderate pooling that works well on cloud hosts; enable pre_ping to avoid stale connections.
    engine = create_engine(
        DATABASE_URL,
        future=True,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        connect_args={"sslmode": "require"}
    )
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return engine, SessionLocal


def init_db():
    engine, _ = _engine_and_session()
    if engine is None:
        return False
    Base.metadata.create_all(bind=engine)
    return True


def get_incidents() -> List[Dict]:
    engine, SessionLocal = _engine_and_session()
    if engine is None:
        return []
    sess = SessionLocal()
    try:
        rows = sess.query(Incident).all()
        return [
            {
                'id': r.id,
                'lat': float(r.lat) if r.lat else None,
                'lng': float(r.lng) if r.lng else None,
                'type': r.type,
                'desc': r.desc,
                'time': r.time,
                'distance': r.distance,
                'timestamp': r.timestamp
            }
            for r in rows
        ]
    finally:
        sess.close()


def get_reports() -> List[Dict]:
    engine, SessionLocal = _engine_and_session()
    if engine is None:
        return []
    sess = SessionLocal()
    try:
        rows = sess.query(Report).all()
        return [
            {
                'id': r.id,
                'type': r.type,
                'description': r.description,
                'location': r.location,
                'timestamp': r.timestamp,
                'status': r.status
            }
            for r in rows
        ]
    finally:
        sess.close()


def add_report(type_: str, description: str, location: Optional[str] = None) -> int:
    engine, SessionLocal = _engine_and_session()
    if engine is None:
        raise RuntimeError('DATABASE_URL not configured')
    sess = SessionLocal()
    try:
        r = Report(type=type_, description=description, location=location)
        sess.add(r)
        sess.commit()
        sess.refresh(r)
        return r.id
    finally:
        sess.close()


def add_incident(lat: Optional[float], lng: Optional[float], type_: str, desc: str, time_str: str, distance: str):
    engine, SessionLocal = _engine_and_session()
    if engine is None:
        raise RuntimeError('DATABASE_URL not configured')
    sess = SessionLocal()
    try:
        i = Incident(lat=str(lat) if lat is not None else None, lng=str(lng) if lng is not None else None,
                     type=type_, desc=desc, time=time_str, distance=distance)
        sess.add(i)
        sess.commit()
        sess.refresh(i)
        return i.id
    finally:
        sess.close()


def get_notifications() -> List[Dict]:
    engine, SessionLocal = _engine_and_session()
    if engine is None:
        return []
    sess = SessionLocal()
    try:
        rows = sess.query(Notification).all()
        return [
            {
                'id': r.id,
                'title': r.title,
                'desc': r.desc,
                'time': r.time,
                'unread': True if r.unread == 'true' else False,
                'timestamp': r.timestamp
            }
            for r in rows
        ]
    finally:
        sess.close()


def add_notification(title: str, desc: str, time_str: str, unread: bool = True):
    engine, SessionLocal = _engine_and_session()
    if engine is None:
        raise RuntimeError('DATABASE_URL not configured')
    sess = SessionLocal()
    try:
        n = Notification(title=title, desc=desc, time=time_str, unread='true' if unread else 'false')
        sess.add(n)
        sess.commit()
        sess.refresh(n)
        return n.id
    finally:
        sess.close()


def mark_all_notifications_read():
    engine, SessionLocal = _engine_and_session()
    if engine is None:
        raise RuntimeError('DATABASE_URL not configured')
    sess = SessionLocal()
    try:
        sess.query(Notification).filter(Notification.unread == 'true').update({'unread': 'false'})
        sess.commit()
    finally:
        sess.close()
