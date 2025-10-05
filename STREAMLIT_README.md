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
