import streamlit as st
import db

st.set_page_config(page_title="DB Test", page_icon="🛠️")

st.title("🛠️ Database Connection Test")

# Initialize DB
if db.init_db():
    st.success("✅ Database connected successfully!")
else:
    st.error("❌ Database connection failed. Check your secrets and DATABASE_URL.")

# Test fetching incidents
if db.init_db():
    try:
        incidents = db.get_incidents()
        st.subheader("Incidents Table")
        if incidents:
            for i in incidents[:5]:  # show first 5 incidents
                st.write(i)
        else:
            st.info("No incidents found in the database.")
    except Exception as e:
        st.error(f"Error fetching incidents: {e}")

# Test fetching reports
if db.init_db():
    try:
        reports = db.get_reports()
        st.subheader("Reports Table")
        if reports:
            for r in reports[:5]:  # show first 5 reports
                st.write(r)
        else:
            st.info("No reports found in the database.")
    except Exception as e:
        st.error(f"Error fetching reports: {e}")
