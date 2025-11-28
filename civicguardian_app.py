# civicguardian_app.py
import os
import io
import base64
from datetime import datetime, timedelta
from typing import Optional

import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
import geocoder

import db  # uses data/reports.db and functions defined in db.py

# --- Page config
st.set_page_config(page_title="CivicGuardian", page_icon="🛡️", layout="wide")

# --- Styles
st.markdown("""
<style>
    .main-header { background: linear-gradient(90deg,#1a237e,#3949ab); padding:1rem; border-radius:10px; color:white; text-align:center; margin-bottom:1.25rem; }
    .report-card { background:white; padding:1rem; border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1); margin:0.5rem 0; border-left:4px solid #1a237e; }
    .notification-item { background:#f8f9ff; padding:1rem; border-radius:10px; margin:0.5rem 0; border-left:4px solid #1a237e; }
    .notification-item.unread { background:#e3f2fd; border-left-color:#e53935; }
</style>
""", unsafe_allow_html=True)

# --- Constants and categories
DEFAULT_LAT, DEFAULT_LNG = 9.337060, 125.969800
CATEGORIES = ["theft", "vandalism", "accident", "suspicious", "hazard", "other"]
incident_colors = {'theft':'red','vandalism':'orange','accident':'blue','suspicious':'green','hazard':'yellow'}
incident_icons = {'theft':'💎','vandalism':'🎨','accident':'🚗','suspicious':'👤','hazard':'⚠️'}

# --- Init DB
DB_ENABLED = db.init_db()
if DB_ENABLED:
    st.sidebar.success("Database: connected (SQLite)")
else:
    st.sidebar.info("Database: not available — using session only")

# --- Load session-state from DB or defaults
if 'incidents' not in st.session_state:
    if DB_ENABLED:
        try:
            st.session_state.incidents = db.get_incidents() or []
        except Exception:
            st.session_state.incidents = []
    else:
        st.session_state.incidents = []

if 'reports' not in st.session_state:
    if DB_ENABLED:
        try:
            st.session_state.reports = db.get_reports() or []
        except Exception:
            st.session_state.reports = []
    else:
        st.session_state.reports = []

if 'notifications' not in st.session_state:
    if DB_ENABLED:
        try:
            st.session_state.notifications = db.get_notifications() or []
        except Exception:
            st.session_state.notifications = []
    else:
        st.session_state.notifications = []

if 'show_report_form' not in st.session_state:
    st.session_state.show_report_form = False

# --- Detect user location (approx via IP)
try:
    g = geocoder.ip('me')
    if g.ok and g.latlng:
        USER_LAT, USER_LNG = g.latlng
    else:
        USER_LAT, USER_LNG = DEFAULT_LAT, DEFAULT_LNG
except Exception:
    USER_LAT, USER_LNG = DEFAULT_LAT, DEFAULT_LNG

# --- Header
st.markdown("""
<div class="main-header">
  <h1>🛡️ CivicGuardian</h1>
  <p>Community Crime Reporting & Safety</p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar / Navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["🏠 Home","🗺️ Map","📋 Reports","🔔 Notifications","👤 Profile","📊 Admin Dashboard","🧪 Debug"])

# Provide DB download button if file exists
db_path = os.path.join("data", "reports.db")
if os.path.exists(db_path):
    with open(db_path, "rb") as f:
        st.sidebar.download_button("Download DB", f, file_name="reports.db")

# --- Helper to render image bytes stored in DB
def render_image_bytes(img_bytes: bytes, width: int = 300):
    if not img_bytes:
        return
    st.image(img_bytes, width=width)

# --- Home Page
if page == "🏠 Home":
    st.header("🏠 Home Dashboard")
    left_col, right_col = st.columns([3,1])

    with right_col:
        if st.button("🚨 EMERGENCY"):
            st.error("🚨 Emergency services have been contacted!")
            notif = {'title': 'Emergency Alert Sent', 'desc': 'Emergency services have been contacted. Stay safe.', 'time': 'Just now'}
            if DB_ENABLED:
                try:
                    db.add_notification(notif['title'], notif['desc'], notif['time'], unread=True)
                    st.session_state.notifications = db.get_notifications() or st.session_state.notifications
                except Exception:
                    st.session_state.notifications.insert(0, {**notif, 'unread': True, 'timestamp': datetime.now()})
            else:
                st.session_state.notifications.insert(0, {**notif, 'unread': True, 'timestamp': datetime.now()})
            st.experimental_rerun()

    with left_col:
        st.subheader("Live Map")
        m = folium.Map(location=[USER_LAT, USER_LNG], zoom_start=14)
        folium.Marker([USER_LAT, USER_LNG], popup="You are here", icon=folium.Icon(color="blue")).add_to(m)
        for inc in st.session_state.incidents:
            try:
                folium.Marker(
                    [float(inc['lat']), float(inc['lng'])],
                    popup=f"<b>{inc['type'].title()}</b><br>{inc.get('desc','')}<br><small>{inc.get('time','')}</small>",
                    icon=folium.Icon(color=incident_colors.get(inc['type'],'blue'))
                ).add_to(m)
            except Exception:
                pass
        st_folium(m, width=700, height=380)

    # Report form toggle + form
    if st.button("📝 REPORT INCIDENT"):
        st.session_state.show_report_form = True

    if st.session_state.show_report_form:
        st.subheader("📝 Report New Incident")
        with st.form("incident_form"):
            c1, c2 = st.columns(2)
            with c1:
                fullname = st.text_input("Full name")
                contact = st.text_input("Contact (phone or email)")
                category = st.selectbox("Category", [""] + CATEGORIES)
                latitude = st.text_input("Latitude", value=str(round(USER_LAT, 6)))
                longitude = st.text_input("Longitude", value=str(round(USER_LNG, 6)))
            with c2:
                date_input = st.date_input("Date", value=datetime.now().date())
                photo = st.file_uploader("Photo (optional)", type=["jpg", "jpeg", "png"], accept_multiple_files=False)
                description = st.text_area("Description")
            col_cancel, col_submit = st.columns(2)
            with col_cancel:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state.show_report_form = False
                    st.experimental_rerun()
            with col_submit:
                if st.form_submit_button("✅ Submit Report"):
                    # validation
                    if not category:
                        st.error("Select a category.")
                    elif not description:
                        st.error("Write a description.")
                    else:
                        # convert coords
                        try:
                            lat_val = float(latitude) if latitude else None
                            lng_val = float(longitude) if longitude else None
                        except ValueError:
                            st.error("Latitude and Longitude must be numbers.")
                            lat_val = lng_val = None

                        # photo bytes
                        photo_bytes = None
                        photo_name = None
                        if photo:
                            photo_bytes = photo.read()
                            photo_name = photo.name

                        # persist report
                        try:
                            report_id = db.add_report(
                                fullname=fullname or None,
                                contact=contact or None,
                                category=category,
                                description=description,
                                latitude=lat_val,
                                longitude=lng_val,
                                date_str=str(date_input),
                                photo_bytes=photo_bytes,
                                photo_name=photo_name,
                            )
                            # optionally also create an incident for map if coords provided
                            if lat_val is not None and lng_val is not None:
                                db.add_incident(lat_val, lng_val, category, description, "Just now", "0 miles")
                            # reload session from DB
                            st.session_state.reports = db.get_reports() or st.session_state.reports
                            st.session_state.incidents = db.get_incidents() or st.session_state.incidents
                            st.success("✅ Report submitted and saved.")
                        except Exception as e:
                            st.error(f"Failed to save report: {e}")
                            # fallback to session-only
                            rid = len(st.session_state.reports) + 1
                            st.session_state.reports.append({
                                "id": rid,
                                "fullname": fullname,
                                "contact": contact,
                                "category": category,
                                "description": description,
                                "latitude": lat_val,
                                "longitude": lng_val,
                                "date": str(date_input),
                                "photo_name": photo_name,
                                "photo_blob": photo_bytes,
                                "timestamp": datetime.now(),
                                "status": "pending",
                            })
                        finally:
                            st.session_state.show_report_form = False
                            st.experimental_rerun()

    # Recent reports preview
    st.subheader("📋 Recent Reports")
    newest = sorted(st.session_state.reports, key=lambda r: r.get("timestamp", datetime.min), reverse=True)[:5]
    for rep in newest:
        ts = rep.get("timestamp")
        ts_str = ts.strftime("%Y-%m-%d %H:%M") if isinstance(ts, datetime) else str(ts)
        st.markdown(f"<div class='report-card'><strong>{rep.get('category','')}</strong> — {rep.get('description','')}<br><small>{ts_str}</small></div>", unsafe_allow_html=True)


# --- Full Map Page ---
elif page == "🗺️ Map":
    st.header("🗺️ Full Map View")
    left, right = st.columns([1,4])
    with left:
        if st.button("🔄 Refresh"):
            st.experimental_rerun()
        radius_km = st.slider("Radius (km, filter incidents)", 1, 100, 25)
        # simple radius filter can be applied; omitted for brevity
    with right:
        m = folium.Map(location=[USER_LAT, USER_LNG], zoom_start=13)
        folium.Marker([USER_LAT, USER_LNG], popup="You are here", icon=folium.Icon(color="blue")).add_to(m)
        for inc in st.session_state.incidents:
            try:
                folium.Marker([float(inc['lat']), float(inc['lng'])], popup=f"{inc['type'].title()}: {inc.get('desc','')}", icon=folium.Icon(color=incident_colors.get(inc['type'],'blue'))).add_to(m)
            except Exception:
                pass
        st_folium(m, width=900, height=520)


# --- Reports Page (with filters and CSV export) ---
elif page == "📋 Reports":
    st.header("📋 All Reports")
    col1, col2 = st.columns([3,1])
    with col2:
        cat_filter = st.selectbox("Filter by category", ["All"] + CATEGORIES)
        start_date = st.date_input("Start date", value=(datetime.now() - timedelta(days=30)).date())
        end_date = st.date_input("End date", value=datetime.now().date())
        if st.button("Apply filters"):
            pass
        if st.button("Download CSV"):
            df = pd.DataFrame(st.session_state.reports)
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, file_name="reports.csv", mime="text/csv")

    reps = st.session_state.reports
    # apply filters
    if cat_filter != "All":
        reps = [r for r in reps if (r.get("category") == cat_filter)]
    def in_date_range(r):
        try:
            d = pd.to_datetime(r.get("date") or r.get("timestamp"))
            return (d.date() >= pd.to_datetime(start_date).date()) and (d.date() <= pd.to_datetime(end_date).date())
        except Exception:
            return True
    reps = [r for r in reps if in_date_range(r)]

    if reps:
        df = pd.DataFrame(reps)
        if "timestamp" in df.columns:
            try:
                df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                pass
        st.dataframe(df, use_container_width=True)
        # show images inline for first few
        for r in reps[:5]:
            if r.get("photo_blob"):
                st.markdown(f"**Photo for report {r['id']} ({r.get('photo_name')})**")
                st.image(r["photo_blob"], width=300)
    else:
        st.info("No reports to show for these filters.")


# --- Notifications Page ---
elif page == "🔔 Notifications":
    st.header("🔔 Notifications")
    if st.button("✅ Mark All Read"):
        if DB_ENABLED:
            db.mark_all_notifications_read()
            st.session_state.notifications = db.get_notifications() or st.session_state.notifications
        else:
            for n in st.session_state.notifications:
                n["unread"] = False
        st.experimental_rerun()
    for n in st.session_state.notifications:
        cls = "unread" if n.get("unread") else ""
        st.markdown(f"<div class='notification-item {cls}'><strong>{n.get('title')}</strong><div>{n.get('desc')}</div><small>{n.get('time')}</small></div>", unsafe_allow_html=True)


# --- Profile Page ---
elif page == "👤 Profile":
    st.header("👤 Profile")
    st.markdown("<div style='background:white;padding:1rem;border-radius:10px;'><h3>John Doe</h3><p>john.doe@example.com</p></div>", unsafe_allow_html=True)
    st.metric("Reports submitted", len(st.session_state.reports))
    pending = len([r for r in st.session_state.reports if r.get("status") == "pending"])
    resolved = len([r for r in st.session_state.reports if r.get("status") == "resolved"])
    st.metric("Pending", pending)
    st.metric("Resolved", resolved)


# --- Admin Dashboard ---
elif page == "📊 Admin Dashboard":
    st.header("📊 Admin Dashboard")
    reports_today = len([r for r in st.session_state.reports if pd.to_datetime(r.get("timestamp", datetime.now())).date() == datetime.now().date()])
    pending_count = len([r for r in st.session_state.reports if r.get("status") == "pending"])
    resolved_count = len([r for r in st.session_state.reports if r.get("status") == "resolved"])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Reports Today", reports_today)
    c2.metric("Response Rate", f"{(resolved_count/len(st.session_state.reports)*100) if st.session_state.reports else 0:.0f}%")
    c3.metric("Pending", pending_count)
    c4.metric("Resolved", resolved_count)

    if st.session_state.incidents:
        st.subheader("Incident Types")
        df_inc = pd.DataFrame(st.session_state.incidents)
        if "type" in df_inc.columns:
            fig = px.pie(df_inc, names="type", title="Incidents by Type")
            st.plotly_chart(fig, use_container_width=True)

    # Admin actions: resolve / delete
    st.subheader("Manage Reports")
    for r in sorted(st.session_state.reports, key=lambda x: x.get("timestamp", datetime.min), reverse=True)[:50]:
        cols = st.columns([6,1,1])
        cols[0].write(f"#{r['id']} — {r.get('category')} — {r.get('description')[:80]}")
        if cols[1].button("Resolve", key=f"resolve_{r['id']}"):
            db.update_report_status(r['id'], "resolved")
            st.session_state.reports = db.get_reports() or st.session_state.reports
            st.experimental_rerun()
        if cols[2].button("Delete", key=f"delete_{r['id']}"):
            db.delete_report(r['id'])
            st.session_state.reports = db.get_reports() or st.session_state.reports
            st.experimental_rerun()


# --- Debug Page ---
elif page == "🧪 Debug":
    st.header("Debug / DB")
    st.write("USER LAT/LNG:", USER_LAT, USER_LNG)
    st.write("DB_ENABLED:", DB_ENABLED)
    st.subheader("Session Incidents")
    st.write(st.session_state.incidents)
    st.subheader("Session Reports")
    st.write(st.session_state.reports)
    st.subheader("Session Notifications")
    st.write(st.session_state.notifications)
    if DB_ENABLED:
        try:
            st.write("Reports (DB):", db.get_reports())
            st.write("Incidents (DB):", db.get_incidents())
            st.write("Notifications (DB):", db.get_notifications())
        except Exception as e:
            st.error(f"DB read error: {e}")

# --- Footer
st.markdown("---")
st.markdown("<div style='text-align:center;color:#666;padding:1rem;'>🛡️ CivicGuardian - Built with Streamlit</div>", unsafe_allow_html=True)
