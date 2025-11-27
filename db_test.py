import streamlit as st
import db

st.set_page_config(page_title="DB Test", page_icon="🛠️")

st.title("🛠️ SQLite Database Test")

# Initialize DB
if db.init_db():
    st.success("✅ Database initialized successfully!")
else:
    st.error("❌ Failed to initialize database.")

# Test adding a sample incident
st.subheader("Add Sample Incident")
if st.button("➕ Add Incident"):
    incident_id = db.add_incident(
        lat=40.7128,
        lng=-74.0060,
        type_="theft",
        desc="Test incident",
        time_str="Just now",
        distance="0.5 miles"
    )
    st.write(f"Added Incident ID: {incident_id}")

# Test fetching incidents
st.subheader("Incidents Table")
try:
    incidents = db.get_incidents()
    if incidents:
        for i in incidents[:5]:  # show first 5 incidents
            st.write(i)
    else:
        st.info("No incidents found in the database.")
except Exception as e:
    st.error(f"Error fetching incidents: {e}")

# Test adding a sample report
st.subheader("Add Sample Report")
if st.button("➕ Add Report"):
    report_id = db.add_report(
        type_="vandalism",
        description="Test report",
        location="Test location"
    )
    st.write(f"Added Report ID: {report_id}")

# Test fetching reports
st.subheader("Reports Table")
try:
    reports = db.get_reports()
    if reports:
        for r in reports[:5]:  # show first 5 reports
            st.write(r)
    else:
        st.info("No reports found in the database.")
except Exception as e:
    st.error(f"Error fetching reports: {e}")
