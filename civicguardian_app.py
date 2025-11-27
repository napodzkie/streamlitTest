import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import db

# Page configuration
st.set_page_config(
    page_title="CivicGuardian - Community Crime Reporting",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1a237e, #3949ab);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .report-card, .notification-item {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .notification-item.unread {
        background: #e3f2fd;
        border-left: 4px solid #e53935;
    }
</style>
""", unsafe_allow_html=True)

# Incident mappings
incident_colors = {'theft':'red','vandalism':'orange','accident':'blue','suspicious':'green','hazard':'yellow'}
incident_icons = {'theft':'💎','vandalism':'🎨','accident':'🚗','suspicious':'👤','hazard':'⚠️'}

# Initialize DB
DB_ENABLED = db.init_db()

# Load session state
if 'incidents' not in st.session_state:
    if DB_ENABLED:
        try:
            st.session_state.incidents = db.get_incidents() or []
        except:
            st.session_state.incidents = []
    else:
        st.session_state.incidents = [
            {'id': 1, 'lat': 40.7128, 'lng': -74.0060, 'type':'theft','desc':'Car break-in','time':'15 min ago','distance':'0.5 miles','timestamp':datetime.now()-timedelta(minutes=15)},
            {'id': 2, 'lat': 40.7180, 'lng': -74.0100, 'type':'vandalism','desc':'Graffiti on building','time':'2 hours ago','distance':'0.8 miles','timestamp':datetime.now()-timedelta(hours=2)},
            {'id': 3, 'lat': 40.7080, 'lng': -74.0050, 'type':'accident','desc':'Two-car collision','time':'5 hours ago','distance':'1.2 miles','timestamp':datetime.now()-timedelta(hours=5)},
            {'id': 4, 'lat': 40.7150, 'lng': -74.0150, 'type':'suspicious','desc':'Suspicious person','time':'1 day ago','distance':'0.3 miles','timestamp':datetime.now()-timedelta(days=1)},
            {'id': 5, 'lat': 40.7100, 'lng': -74.0080, 'type':'hazard','desc':'Fallen tree blocking road','time':'2 days ago','distance':'0.7 miles','timestamp':datetime.now()-timedelta(days=2)}
        ]

if 'reports' not in st.session_state:
    if DB_ENABLED:
        try:
            st.session_state.reports = db.get_reports() or []
        except:
            st.session_state.reports = []
    else:
        st.session_state.reports = []

if 'notifications' not in st.session_state:
    if DB_ENABLED:
        try:
            st.session_state.notifications = db.get_notifications() or []
        except:
            st.session_state.notifications = []
    else:
        st.session_state.notifications = [
            {'id':1,'title':'New Incident','desc':'Traffic accident reported','time':'2 min ago','unread':True,'timestamp':datetime.now()-timedelta(minutes=2)}
        ]

# Main header
st.markdown("""
<div class="main-header">
    <h1>🛡️ CivicGuardian</h1>
    <p>Community Crime Reporting & Safety App</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["🏠 Home","🗺️ Map","📋 Reports","🔔 Notifications","👤 Profile","📊 Admin Dashboard"])
st.sidebar.success("Database: connected" if DB_ENABLED else "Database: in-memory only")

# Home Page
if page=="🏠 Home":
    st.header("🏠 Home Dashboard")
    col1,col2 = st.columns([3,1])
    with col2:
        if st.button("🚨 EMERGENCY"):
            emergency_notification = {'id':len(st.session_state.notifications)+1,'title':'Emergency Alert','desc':'Services contacted','time':'Just now','unread':True,'timestamp':datetime.now()}
            if DB_ENABLED:
                try:
                    db.add_notification(emergency_notification['title'],emergency_notification['desc'],emergency_notification['time'],True)
                except: pass
            st.session_state.notifications.insert(0,emergency_notification)
            st.rerun()
    # Map
    m = folium.Map(location=[40.7128,-74.0060],zoom_start=13)
    for incident in st.session_state.incidents:
        folium.Marker([incident['lat'],incident['lng']],
            popup=f"<b>{incident['type'].upper()}</b><br>{incident['desc']}<br><small>{incident['time']}</small>",
            icon=folium.Icon(color=incident_colors.get(incident['type'],'blue'),icon='info-sign')).add_to(m)
    st_folium(m,width=700,height=300)

    # Report form
    if st.button("📝 REPORT INCIDENT"):
        st.session_state.show_report_form = True
    if st.session_state.get('show_report_form',False):
        st.subheader("📝 Report New Incident")
        with st.form("incident_form"):
            col1,col2=st.columns(2)
            with col1:
                incident_type = st.selectbox("Incident Type", ["","theft","vandalism","accident","suspicious","hazard","other"])
            with col2:
                location = st.text_input("Location","Enter location")
            description = st.text_area("Description","Details about the incident")
            if st.form_submit_button("✅ Submit Report"):
                if incident_type and description:
                    report_id = None
                    if DB_ENABLED:
                        try:
                            report_id = db.add_report(incident_type,description,location or "Current Location")
                            st.session_state.reports = db.get_reports() or []
                        except: pass
                    else:
                        report_id = len(st.session_state.reports)+1
                        st.session_state.reports.append({'id':report_id,'type':incident_type,'description':description,'location':location or "Current Location",'timestamp':datetime.now(),'status':'pending'})
                    st.session_state.show_report_form=False
                    st.success("✅ Incident reported successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")

# Map Page
elif page=="🗺️ Map":
    st.header("🗺️ Full Map View")
    m = folium.Map(location=[9.337060,125.969800],zoom_start=13)
    for incident in st.session_state.incidents:
        folium.Marker([incident['lat'],incident['lng']],
            popup=f"<b>{incident['type'].upper()}</b><br>{incident['desc']}<br><small>{incident['time']}</small>",
            icon=folium.Icon(color=incident_colors.get(incident['type'],'blue'),icon='info-sign')).add_to(m)
    st_folium(m,width=800,height=500)

# Reports Page
elif page=="📋 Reports":
    st.header("📋 All Reports")
    for incident in st.session_state.incidents:
        st.markdown(f"""
        <div class="report-card">
            <h4>{incident_icons.get(incident['type'],'📋')} {incident['type'].title()}</h4>
            <p>{incident['desc']}</p>
            <small>⏰ {incident['time']} | 📍 {incident['distance']} away</small>
        </div>
        """,unsafe_allow_html=True)

# Notifications Page
elif page=="🔔 Notifications":
    st.header("🔔 Notifications")
    if st.button("✅ Mark All Read"):
        if DB_ENABLED:
            try: db.mark_all_notifications_read()
            except: pass
        for n in st.session_state.notifications: n['unread']=False
        st.rerun()
    for n in st.session_state.notifications:
        cls="unread" if n['unread'] else ""
        st.markdown(f"<div class='notification-item {cls}'><h4>{n['title']}</h4><p>{n['desc']}</p><small>⏰ {n['time']}</small></div>",unsafe_allow_html=True)

# Profile Page
elif page=="👤 Profile":
    st.header("👤 Profile")
    st.markdown("<div style='background:white;padding:1rem;border-radius:10px;text-align:center;'><h3>John Doe</h3><p>john.doe@example.com</p></div>",unsafe_allow_html=True)

# Admin Dashboard
elif page=="📊 Admin Dashboard":
    st.header("📊 Admin Dashboard")
    reports_today=len([r for r in st.session_state.reports if r['timestamp'].date()==datetime.now().date()])
    pending_count=len([r for r in st.session_state.reports if r.get('status')=='pending'])
    resolved_count=len([r for r in st.session_state.reports if r.get('status')=='resolved'])
    response_rate=(resolved_count/len(st.session_state.reports)*100) if st.session_state.reports else 0
    col1,col2,col3,col4=st.columns(4)
    col1.metric("📋 Reports Today",reports_today)
    col2.metric("📈 Response Rate",f"{response_rate:.0f}%")
    col3.metric("⏳ Pending",pending_count)
    col4.metric("✅ Resolved",resolved_count)
    # Incident pie
    incident_types={}
    for inc in st.session_state.incidents: incident_types[inc['type']]=incident_types.get(inc['type'],0)+1
    if incident_types:
        fig=px.pie(values=list(incident_types.values()),names=list(incident_types.keys()),title="Distribution of Incident Types")
        st.plotly_chart(fig,use_container_width=True)

# Footer
st.markdown("---")
st.markdown("<div style='text-align:center;color:#666;padding:1rem;'><p>🛡️ CivicGuardian App</p></div>",unsafe_allow_html=True)
