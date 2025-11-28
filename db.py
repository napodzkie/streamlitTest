# db.py
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Text,
    LargeBinary,
)
from sqlalchemy.orm import declarative_base, sessionmaker
import streamlit as st

# ensure data dir
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

DB_FILE = os.path.join(DATA_DIR, "reports.db")
DATABASE_URL = f"sqlite:///{DB_FILE}"

Base = declarative_base()


class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True)
    lat = Column(String, nullable=True)
    lng = Column(String, nullable=True)
    type = Column(String, nullable=False)
    desc = Column(Text, nullable=True)
    time = Column(String, nullable=True)        # e.g., "Just now" or user-supplied date string
    distance = Column(String, nullable=True)    # optional
    timestamp = Column(DateTime, default=datetime.utcnow)


class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    fullname = Column(String, nullable=True)
    contact = Column(String, nullable=True)
    category = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    date = Column(String, nullable=True)  # user-supplied date (string)
    photo_name = Column(String, nullable=True)
    photo_blob = Column(LargeBinary, nullable=True)  # store image bytes
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


# Engine / Session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> bool:
    """Create tables if missing."""
    try:
        Base.metadata.create_all(bind=engine)
        return True
    except Exception as e:
        # expose a helpful message in Streamlit logs
        try:
            st.error(f"Database initialization error: {e}")
        except Exception:
            pass
        return False


# -------------------------
# Reports CRUD
# -------------------------
def add_report(
    fullname: Optional[str],
    contact: Optional[str],
    category: str,
    description: str,
    latitude: Optional[float],
    longitude: Optional[float],
    date_str: Optional[str],
    photo_bytes: Optional[bytes],
    photo_name: Optional[str],
) -> int:
    sess = SessionLocal()
    try:
        r = Report(
            fullname=fullname,
            contact=contact,
            category=category,
            description=description,
            latitude=str(latitude) if latitude is not None else None,
            longitude=str(longitude) if longitude is not None else None,
            date=date_str,
            photo_blob=photo_bytes,
            photo_name=photo_name,
        )
        sess.add(r)
        sess.commit()
        sess.refresh(r)
        return r.id
    finally:
        sess.close()


def get_reports() -> List[Dict]:
    sess = SessionLocal()
    try:
        rows = sess.query(Report).all()
        out = []
        for r in rows:
            out.append(
                {
                    "id": r.id,
                    "fullname": r.fullname,
                    "contact": r.contact,
                    "category": r.category,
                    "description": r.description,
                    "latitude": float(r.latitude) if r.latitude else None,
                    "longitude": float(r.longitude) if r.longitude else None,
                    "date": r.date,
                    "photo_name": r.photo_name,
                    "photo_blob": r.photo_blob,  # bytes (may be None)
                    "timestamp": r.timestamp,
                    "status": r.status,
                }
            )
        return out
    finally:
        sess.close()


def update_report_status(report_id: int, status: str) -> bool:
    sess = SessionLocal()
    try:
        r = sess.query(Report).filter(Report.id == report_id).first()
        if not r:
            return False
        r.status = status
        sess.commit()
        return True
    finally:
        sess.close()


def delete_report(report_id: int) -> bool:
    sess = SessionLocal()
    try:
        r = sess.query(Report).filter(Report.id == report_id).first()
        if not r:
            return False
        sess.delete(r)
        sess.commit()
        return True
    finally:
        sess.close()


# -------------------------
# Incidents CRUD (derived or manual)
# -------------------------
def add_incident(
    lat: Optional[float],
    lng: Optional[float],
    type_: str,
    desc: str,
    time_str: str,
    distance: Optional[str] = None,
) -> int:
    sess = SessionLocal()
    try:
        i = Incident(
            lat=str(lat) if lat is not None else None,
            lng=str(lng) if lng is not None else None,
            type=type_,
            desc=desc,
            time=time_str,
            distance=distance,
        )
        sess.add(i)
        sess.commit()
        sess.refresh(i)
        return i.id
    finally:
        sess.close()


def get_incidents() -> List[Dict]:
    """
    Returns incidents in the same shape you provided earlier:
        id, lat, lng, type, desc, time, distance, timestamp
    """
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
                "timestamp": r.timestamp,
            }
            for r in rows
        ]
    finally:
        sess.close()


# -------------------------
# Notifications
# -------------------------
def add_notification(title: str, desc: str, time_str: str, unread: bool = True) -> int:
    sess = SessionLocal()
    try:
        n = Notification(title=title, desc=desc, time=time_str, unread="true" if unread else "false")
        sess.add(n)
        sess.commit()
        sess.refresh(n)
        return n.id
    finally:
        sess.close()


def get_notifications() -> List[Dict]:
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
                "timestamp": r.timestamp,
            }
            for r in rows
        ]
    finally:
        sess.close()


def mark_all_notifications_read() -> None:
    sess = SessionLocal()
    try:
        sess.query(Notification).filter(Notification.unread == "true").update({"unread": "false"})
        sess.commit()
    finally:
        sess.close()
