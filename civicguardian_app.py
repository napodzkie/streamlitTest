import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json
import folium
from streamlit_folium import st_folium
import time
import db

# Page configuration
st.set_page_config(
    page_title="CivicGuardian - Community Crime Reporting",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to match the original design
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
    
    .emergency-btn {
        background: #e53935;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: none;
        font-weight: bold;
        cursor: pointer;
    }
    
    .report-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 4px solid #1a237e;
    }
    
    .stat-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .notification-item {
        background: #f8f9ff;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #1a237e;
    }
    
    .notification-item.unread {
        background: #e3f2fd;
        border-left-color: #e53935;
    }
</style>
""", unsafe_allow_html=True)

# Shared incident mappings (used across all pages)
incident_colors = {
    'theft': 'red',
    'vandalism': 'orange',
    'accident': 'blue',
    'suspicious': 'green',
    'hazard': 'yellow'
}

# Icons for textual/UI display (emojis are fine for Streamlit markup)
incident_icons = {
    'theft': '💎',
    'vandalism': '🎨',
    'accident': '🚗',
    'suspicious': '👤',
    'hazard': '⚠️'
}

# Initialize session state
DB_ENABLED = db.init_db()

if 'incidents' not in st.session_state:
    # Load incidents from DB when available, otherwise fall back to sample data
    if DB_ENABLED:
        try:
            st.session_state.incidents = db.get_incidents() or []
        except Exception as e:
            st.warning(f"Warning: failed to load incidents from DB: {e}")
            st.session_state.incidents = []
    else:
        st.session_state.incidents = [
        {'id': 1, 'lat': 40.7128, 'lng': -74.0060, 'type': 'theft', 'desc': 'Car break-in', 'time': '15 min ago', 'distance': '0.5 miles', 'timestamp': datetime.now() - timedelta(minutes=15)},
        {'id': 2, 'lat': 40.7180, 'lng': -74.0100, 'type': 'vandalism', 'desc': 'Graffiti on building', 'time': '2 hours ago', 'distance': '0.8 miles', 'timestamp': datetime.now() - timedelta(hours=2)},
        {'id': 3, 'lat': 40.7080, 'lng': -74.0050, 'type': 'accident', 'desc': 'Two-car collision', 'time': '5 hours ago', 'distance': '1.2 miles', 'timestamp': datetime.now() - timedelta(hours=5)},
        {'id': 4, 'lat': 40.7150, 'lng': -74.0150, 'type': 'suspicious', 'desc': 'Suspicious person', 'time': '1 day ago', 'distance': '0.3 miles', 'timestamp': datetime.now() - timedelta(days=1)},
        {'id': 5, 'lat': 40.7100, 'lng': -74.0080, 'type': 'hazard', 'desc': 'Fallen tree blocking road', 'time': '2 days ago', 'distance': '0.7 miles', 'timestamp': datetime.now() - timedelta(days=2)}
    ]

if 'reports' not in st.session_state:
    # Load persisted reports from DB if enabled
    if DB_ENABLED:
        try:
            st.session_state.reports = db.get_reports() or []
        except Exception as e:
            st.warning(f"Warning: failed to load reports from DB: {e}")
            st.session_state.reports = []
    else:
        st.session_state.reports = []

if 'notifications' not in st.session_state:
    if DB_ENABLED:
        try:
            st.session_state.notifications = db.get_notifications() or []
        except Exception as e:
            st.warning(f"Warning: failed to load notifications from DB: {e}")
            st.session_state.notifications = []
    else:
        st.session_state.notifications = [
        {'id': 1, 'title': 'New Incident Near You', 'desc': 'A traffic accident was reported 0.3 miles from your location.', 'time': '2 minutes ago', 'unread': True, 'timestamp': datetime.now() - timedelta(minutes=2)},
        {'id': 2, 'title': 'Report Resolved', 'desc': 'Your report #1256 has been resolved by local authorities.', 'time': '1 hour ago', 'unread': False, 'timestamp': datetime.now() - timedelta(hours=1)},
        {'id': 3, 'title': 'App Update Available', 'desc': 'Update to version 2.1.0 is now available with new features.', 'time': '3 hours ago', 'unread': False, 'timestamp': datetime.now() - timedelta(hours=3)},
        {'id': 4, 'title': 'Emergency Alert', 'desc': 'Police activity reported in your area. Please avoid the area if possible.', 'time': '30 minutes ago', 'unread': True, 'timestamp': datetime.now() - timedelta(minutes=30)}
    ]

# Main header
st.markdown("""
<div class="main-header">
    <h1>🛡️ CivicGuardian</h1>
    <p>Community Crime Reporting & Safety App</p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["🏠 Home", "🗺️ Map", "📋 Reports", "🔔 Notifications", "👤 Profile", "📊 Admin Dashboard"])

# Show DB status in the sidebar so developers can see whether persistence is enabled
if DB_ENABLED:
    st.sidebar.success("Database: connected")
else:
    st.sidebar.info("Database: not configured (using in-memory session state)")

# Home Page
if page == "🏠 Home":
    st.header("🏠 Home Dashboard")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Live Map")
    with col2:
        if st.button("🚨 EMERGENCY", key="emergency_btn", help="Click in case of emergency"):
            st.error("🚨 Emergency services have been contacted! Help is on the way!")
            # Add emergency notification
            emergency_notification = {
                'id': len(st.session_state.notifications) + 1,
                'title': 'Emergency Alert Sent',
                'desc': 'Emergency services have been contacted. Stay safe and follow instructions.',
                'time': 'Just now',
                'unread': True,
                'timestamp': datetime.now()
            }
            # Persist notification to DB if enabled
            if DB_ENABLED:
                try:
                    db.add_notification(emergency_notification['title'], emergency_notification['desc'], emergency_notification['time'], unread=True)
                except Exception as e:
                    st.warning(f"Warning: failed to persist notification: {e}")
            st.session_state.notifications.insert(0, emergency_notification)
            st.rerun()
    
    # Map
    m = folium.Map(location=[40.7128, -74.0060], zoom_start=13)
    
    # Add incident markers
    for incident in st.session_state.incidents:
        folium.Marker(
            [incident['lat'], incident['lng']],
            popup=f"<b>{incident['type'].upper()}</b><br>{incident['desc']}<br><small>{incident['time']}</small>",
            # Folium Icon requires a valid icon string (e.g., 'info-sign'); emojis are not supported here
            icon=folium.Icon(color=incident_colors.get(incident['type'], 'blue'), icon='info-sign')
        ).add_to(m)
    
    st_folium(m, width=700, height=300)
    
    # Report Incident Button
    if st.button("📝 REPORT INCIDENT", key="report_btn", use_container_width=True):
        st.session_state.show_report_form = True
    
    if st.session_state.get('show_report_form', False):
        st.subheader("📝 Report New Incident")
        
        with st.form("incident_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                incident_type = st.selectbox("Incident Type", ["", "theft", "vandalism", "accident", "suspicious", "hazard", "other"])
            
            with col2:
                location = st.text_input("Location", placeholder="Enter location or use current")
            
            description = st.text_area("Description", placeholder="Provide details about the incident...")
            
            uploaded_files = st.file_uploader("Upload Media (Optional)", accept_multiple_files=True, type=['jpg', 'jpeg', 'png', 'mp4'])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state.show_report_form = False
                    st.rerun()
            
            with col2:
                if st.form_submit_button("✅ Submit Report"):
                    if incident_type and description:
                        # Persist to DB when available, otherwise append to session
                        if DB_ENABLED:
                            try:
                                report_id = db.add_report(incident_type, description, location or 'Current Location')
                                # reload reports
                                st.session_state.reports = db.get_reports() or []
                            except Exception as e:
                                st.error(f"Failed to save report to DB: {e}")
                                report_id = None
                        else:
                            report_id = len(st.session_state.reports) + 1

                        new_report = {
                            'id': report_id,
                            'type': incident_type,
                            'description': description,
                            'location': location or 'Current Location',
                            'timestamp': datetime.now(),
                            'status': 'pending'
                        }

                        if not DB_ENABLED:
                            st.session_state.reports.append(new_report)

                        st.session_state.show_report_form = False
                        st.success("✅ Incident reported successfully!")
                        st.rerun()
                    else:
                        st.error("Please fill in all required fields.")
    
    # Recent Reports
    st.subheader("📋 Recent Reports")
    
    for incident in st.session_state.incidents[:3]:
        with st.container():
            st.markdown(f"""
            <div class="report-card">
                <h4>{incident_icons.get(incident['type'], '📋')} {incident['type'].title()}</h4>
                <p>{incident['desc']}</p>
                <small>⏰ {incident['time']} | 📍 {incident['distance']} away</small>
            </div>
            """, unsafe_allow_html=True)

# Map Page
elif page == "🗺️ Map":
    st.header("🗺️ Full Map View")
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("🔄 Refresh Map"):
            st.rerun()
        
        if st.button("📍 Center on Location"):
            st.info("📍 Centered on your location")
    
    with col2:
        # Full map
        m = folium.Map(location=[9.337060, 125.969800], zoom_start=13)
        
        # Add all incident markers
        for incident in st.session_state.incidents:
            folium.Marker(
                [incident['lat'], incident['lng']],
                popup=f"<b>{incident['type'].upper()}</b><br>{incident['desc']}<br><small>{incident['time']}</small>",
                icon=folium.Icon(color=incident_colors.get(incident['type'], 'blue'), icon='info-sign')
            ).add_to(m)
        
        st_folium(m, width=800, height=500)

# Reports Page
elif page == "📋 Reports":
    st.header("📋 All Reports")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        filter_type = st.selectbox("Filter by Type", ["All", "theft", "vandalism", "accident", "suspicious", "hazard"])
    
    with col1:
        st.write(f"Showing {len(st.session_state.incidents)} reports")
    
    # Filter incidents
    filtered_incidents = st.session_state.incidents
    if filter_type != "All":
        filtered_incidents = [inc for inc in st.session_state.incidents if inc['type'] == filter_type]
    
    # Display filtered reports
    for incident in filtered_incidents:
        with st.container():
            st.markdown(f"""
            <div class="report-card">
                <h4>{incident_icons.get(incident['type'], '📋')} {incident['type'].title()}</h4>
                <p>{incident['desc']}</p>
                <small>⏰ {incident['time']} | 📍 {incident['distance']} away</small>
            </div>
            """, unsafe_allow_html=True)

# Notifications Page
elif page == "🔔 Notifications":
    st.header("🔔 Notifications")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("✅ Mark All Read"):
            # Persist to DB if enabled
            if DB_ENABLED:
                try:
                    db.mark_all_notifications_read()
                except Exception as e:
                    st.warning(f"Warning: failed to mark all notifications read in DB: {e}")

            for notification in st.session_state.notifications:
                notification['unread'] = False
            st.success("All notifications marked as read!")
            st.rerun()
    
    with col1:
        unread_count = sum(1 for n in st.session_state.notifications if n['unread'])
        st.write(f"You have {unread_count} unread notifications")
    
    # Display notifications
    for notification in st.session_state.notifications:
        unread_class = "unread" if notification['unread'] else ""
        st.markdown(f"""
        <div class="notification-item {unread_class}">
            <h4>{notification['title']}</h4>
            <p>{notification['desc']}</p>
            <small>⏰ {notification['time']}</small>
        </div>
        """, unsafe_allow_html=True)

# Profile Page
elif page == "👤 Profile":
    st.header("👤 Profile")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style="text-align: center; background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="width: 80px; height: 80px; border-radius: 50%; background: #1a237e; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center; font-size: 2rem; color: white;">👤</div>
            <h3>John Doe</h3>
            <p>john.doe@example.com</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("📊 Your Stats")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📋 Reports", len(st.session_state.reports))
        
        with col2:
            resolved = len([r for r in st.session_state.reports if r.get('status') == 'resolved'])
            st.metric("✅ Resolved", resolved)
        
        with col3:
            pending = len([r for r in st.session_state.reports if r.get('status') == 'pending'])
            st.metric("⏳ Pending", pending)
    
    st.subheader("⚙️ Settings")
    
    if st.button("✏️ Edit Profile"):
        st.info("Edit profile feature coming soon!")
    
    if st.button("⚙️ Settings"):
        st.info("Settings feature coming soon!")
    
    if st.button("❓ Help & Support"):
        st.info("Help & Support feature coming soon!")
    
    if st.button("ℹ️ About"):
        st.info("CivicGuardian v2.1.0\nCommunity Crime Reporting App\n\nBuilt with ❤️ for community safety")
    
    if st.button("🚪 Logout"):
        st.warning("Logged out successfully!")

# Admin Dashboard Page
elif page == "📊 Admin Dashboard":
    st.header("📊 Admin Dashboard")
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    reports_today = len([r for r in st.session_state.reports if r['timestamp'].date() == datetime.now().date()])
    pending_count = len([r for r in st.session_state.reports if r.get('status') == 'pending'])
    resolved_count = len([r for r in st.session_state.reports if r.get('status') == 'resolved'])
    response_rate = (resolved_count / len(st.session_state.reports) * 100) if st.session_state.reports else 0
    
    with col1:
        st.metric("📋 Reports Today", reports_today)
    
    with col2:
        st.metric("📈 Response Rate", f"{response_rate:.0f}%")
    
    with col3:
        st.metric("⏳ Pending", pending_count)
    
    with col4:
        st.metric("✅ Resolved", resolved_count)
    
    # Incident types chart
    st.subheader("📊 Incident Types")
    
    incident_types = {}
    for incident in st.session_state.incidents:
        incident_types[incident['type']] = incident_types.get(incident['type'], 0) + 1
    
    if incident_types:
        fig = px.pie(
            values=list(incident_types.values()),
            names=list(incident_types.keys()),
            title="Distribution of Incident Types"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Response tracker table
    st.subheader("📋 Response Tracker")
    
    if st.session_state.reports:
        df = pd.DataFrame(st.session_state.reports)
        df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        df = df.rename(columns={
            'id': 'ID',
            'type': 'Type',
            'description': 'Description',
            'location': 'Location',
            'status': 'Status',
            'timestamp': 'Time'
        })
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No reports submitted yet.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🛡️ CivicGuardian - Community Crime Reporting App</p>
    <p>Built with Streamlit | Version 2.1.0</p>
</div>
""", unsafe_allow_html=True)
