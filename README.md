# CivicGuardian - Community Crime Reporting App

A modern, mobile-first Progressive Web App (PWA) for community crime reporting and safety awareness.

## Features

### 🏠 **Home Dashboard**
- Live interactive map showing recent incidents
- Quick incident reporting button
- Recent reports feed with real-time updates
- Current time display

### 📍 **Interactive Map**
- Real-time incident markers with different colors by type
- Click markers to view incident details
- Automatic geolocation detection
- Responsive map controls

### 📝 **Incident Reporting**
- Comprehensive form with incident type selection
- Rich text description field
- Automatic location detection
- Media upload support (photos/videos)
- Form validation and error handling

### 👨‍💼 **Admin Dashboard**
- Real-time analytics and statistics
- Incident type breakdown charts
- Response tracking table
- Status management (Pending, In Progress, Resolved)

### 📱 **Mobile-First Design**
- Responsive design optimized for mobile devices
- Touch-friendly interface
- Bottom navigation bar
- PWA capabilities for app-like experience

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Maps**: Leaflet.js with OpenStreetMap
- **Icons**: Font Awesome 6.4.0
- **Storage**: LocalStorage for data persistence
- **PWA**: Service Worker for offline capabilities

## Installation & Setup

1. **Clone or download** the project files
2. **Open** `index.html` in a modern web browser
3. **For PWA features**: Serve from a web server (not file://)

### Local Development Server
```bash
# Using Python 3
python -m http.server 8000

# Using Node.js
npx serve .

# Using PHP
php -S localhost:8000
```

## File Structure

```
civic-guardian/
├── index.html          # Main HTML file
├── styles.css          # CSS styles and responsive design
├── script.js           # JavaScript application logic
├── sw.js              # Service Worker for PWA
├── manifest.json      # PWA manifest file
└── README.md          # This documentation
```

Note: This repository also contains a Streamlit-based Python app at `civicguardian_app.py` which can persist data into PostgreSQL when configured. The static PWA front-end (`index.html`) keeps data in LocalStorage and does not require a database.

If you want to use a managed database such as Supabase, create a database in Supabase and copy the connection URI (example below). Place it in a `.env` file as `DATABASE_URL` or put it in Streamlit Cloud Secrets.

Example Supabase URI (replace password):
```
postgresql://postgres:YOUR_PASSWORD@db.ypzycptidfpqxikjcwxy.supabase.co:5432/postgres?sslmode=require
```

## Key Features Explained

### Geolocation Integration
- Automatically detects user's current location
- Uses HTML5 Geolocation API
- Falls back to default location (NYC) if permission denied

### Data Persistence
- Reports stored in browser's LocalStorage
- Survives browser sessions
- Admin dashboard updates in real-time

### Progressive Web App
- Installable on mobile devices
- Offline functionality via Service Worker
- App-like experience with manifest.json

### Responsive Design
- Mobile-first approach
- Breakpoints for different screen sizes
- Touch-optimized interface elements

## Browser Compatibility

- **Chrome/Edge**: Full support
- **Firefox**: Full support
- **Safari**: Full support (iOS 11.3+)
- **Mobile Browsers**: Optimized for mobile use

## Security Considerations

- No sensitive data transmitted
- All data stored locally
- HTTPS recommended for production deployment
- Geolocation requires user permission

## Future Enhancements

- [ ] Backend API integration
- [ ] User authentication system
- [ ] Push notifications
- [ ] Real-time chat with authorities
- [ ] Incident verification system
- [ ] Community moderation features

## Contributing

This is a demonstration project. Feel free to fork and enhance with additional features.

## License

Open source - feel free to use and modify for your community safety initiatives.

---

**CivicGuardian** - Empowering communities through technology and collaboration.
