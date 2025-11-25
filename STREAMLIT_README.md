# CivicGuardian - Streamlit Version

A community-driven crime reporting and safety app built with Streamlit.

## Features

- 🏠 **Home Dashboard** - Overview with live map and recent reports
- 🗺️ **Interactive Map** - Full-screen map with incident markers
- 📋 **Reports Management** - View and filter all incident reports
- 🔔 **Notifications** - Real-time alerts and updates
- 👤 **User Profile** - Personal stats and settings
- 📊 **Admin Dashboard** - Analytics and incident management
- 🚨 **Emergency Button** - Quick emergency services contact

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Start

1. **Run the automated installer:**
   ```bash
   # Windows (Command Prompt)
   run_streamlit_app.bat
   
   # Windows (PowerShell)
   .\run_streamlit_app.ps1
   ```

2. **Or install manually:**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Run the app
   streamlit run civicguardian_app.py
   ```

3. **Open your browser to:** `http://localhost:8501`

## Database (PostgreSQL) integration

This Streamlit app can persist incidents, reports and notifications to a PostgreSQL database when configured.

1. Start a local Postgres instance (Docker example):

```powershell
# runs a local postgres DB exposed on port 5432
docker run --name civicguardian-postgres -e POSTGRES_PASSWORD=changeme -e POSTGRES_USER=postgres -e POSTGRES_DB=civicguardian -p 5432:5432 -d postgres:15
```

2. Create a `.env` in the project root or set the `DATABASE_URL` environment variable. Example `.env`:

```
DATABASE_URL=postgresql://postgres:changeme@localhost:5432/civicguardian
```

3. If you're deploying to Streamlit Cloud you should use Streamlit Secrets instead of a `.env` file. In the Streamlit app settings add the DATABASE_URL secret (replace the placeholder password):

```toml
# In Streamlit Cloud: App -> Settings -> Secrets
DATABASE_URL = "postgresql://postgres:YOUR_REAL_PASSWORD@db.ypzycptidfpqxikjcwxy.supabase.co:5432/postgres?sslmode=require"
```

The app code already looks for a `DATABASE_URL` env var and will also read `st.secrets['DATABASE_URL']` when running on Streamlit Cloud.

4. The app will pick up the `.env` automatically (via python-dotenv) or read Streamlit secrets, and create the required tables on first run.

4. Run the app normally:

```powershell
pip install -r requirements.txt
streamlit run civicguardian_app.py
```

If your environment doesn't have Docker, install PostgreSQL locally and set `DATABASE_URL` accordingly.

## Features Overview
## Features Overview

### 🏠 Home Page
- Live interactive map with incident markers
- Emergency button for immediate help
- Recent incident reports
- Quick incident reporting form

### 🗺️ Map Page
- Full-screen interactive map
- All incident markers with details
- Map controls (refresh, center location)
- Click markers for incident details

### 📋 Reports Page
- Complete list of all incidents
- Filter by incident type
- Detailed incident information
- Real-time updates

### 🔔 Notifications Page
- Real-time alerts and updates
- Mark notifications as read
- Emergency alerts
- System notifications

### 👤 Profile Page
- User information and stats
- Personal incident reports
- Settings and preferences
- Help and support options

### 📊 Admin Dashboard
- Incident analytics and statistics
- Response rate tracking
- Incident type distribution charts
- Complete incident management table

## Data Structure

The app maintains the following data structures:

- **Incidents**: Sample incident data with location, type, and details
- **Reports**: User-submitted incident reports
- **Notifications**: System alerts and updates

## Customization

You can easily customize the app by modifying:

- **Incident types** in the `incident_colors` and `incident_icons` dictionaries
- **Sample data** in the session state initialization
- **Styling** in the custom CSS section
- **Map location** by changing the default coordinates

## Technical Details

- **Framework**: Streamlit
- **Maps**: Folium with OpenStreetMap
- **Charts**: Plotly
- **Data**: Pandas DataFrames
- **State Management**: Streamlit Session State

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port with `streamlit run civicguardian_app.py --server.port 8502`

2. **Package installation fails**: Try `pip install --upgrade pip` first

3. **Map not loading**: Check your internet connection (requires OpenStreetMap tiles)

4. **Browser not opening**: Manually navigate to `http://localhost:8501`

## Support

For issues or questions:
- Check the Streamlit documentation
- Review the code comments
- Test with different browsers

## Version

- **Current Version**: 2.1.0
- **Last Updated**: 2024
- **Framework**: Streamlit
