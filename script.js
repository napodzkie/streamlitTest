// CivicGuardian App JavaScript
class CivicGuardianApp {
    constructor() {
        this.map = null;
        this.mapFull = null;
        this.currentLocation = null;
        this.incidents = [];
        this.reports = [];
        this.notifications = [];
        this.currentScreen = 'home';
        this.init();
    }

    init() {
        this.updateTime();
        setInterval(() => this.updateTime(), 60000);
        
        this.setupEventListeners();
        this.loadStoredData();
        this.loadSampleData();
        this.loadNotifications();
        
        // Initialize maps after a short delay to ensure DOM is ready
        setTimeout(() => {
            this.initializeMap();
            this.showScreen('home');
        }, 100);
    }

    updateTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        const timeElement = document.getElementById('current-time');
        if (timeElement) {
            timeElement.textContent = timeString;
        }
    }

    initializeMap() {
        // Initialize home map with default location (NYC)
        const mapElement = document.getElementById('map');
        if (mapElement) {
            this.map = L.map('map').setView([40.7128, -74.0060], 13);
            
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(this.map);
        }

        // Initialize full map for map screen
        const mapFullElement = document.getElementById('map-full');
        if (mapFullElement) {
            this.mapFull = L.map('map-full').setView([40.7128, -74.0060], 13);
            
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(this.mapFull);
        }

        // Try to get user's current location
        this.getCurrentLocation();
    }

    getCurrentLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    this.currentLocation = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    };
                    if (this.map) {
                        this.map.setView([this.currentLocation.lat, this.currentLocation.lng], 15);
                        this.addLocationMarker(this.map);
                    }
                    if (this.mapFull) {
                        this.mapFull.setView([this.currentLocation.lat, this.currentLocation.lng], 15);
                        this.addLocationMarker(this.mapFull);
                    }
                },
                (error) => {
                    console.log('Geolocation error:', error);
                    // Keep default NYC location
                },
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 300000
                }
            );
        }
    }

    addLocationMarker(mapInstance) {
        if (this.currentLocation && mapInstance) {
            L.marker([this.currentLocation.lat, this.currentLocation.lng])
                .addTo(mapInstance)
                .bindPopup('Your Location')
                .openPopup();
        }
    }

    loadSampleData() {
        // Sample incidents data
        this.incidents = [
            {id: 1, lat: 40.7128, lng: -74.0060, type: 'theft', desc: 'Car break-in', time: '15 min ago', distance: '0.5 miles'},
            {id: 2, lat: 40.7180, lng: -74.0100, type: 'vandalism', desc: 'Graffiti on building', time: '2 hours ago', distance: '0.8 miles'},
            {id: 3, lat: 40.7080, lng: -74.0050, type: 'accident', desc: 'Two-car collision', time: '5 hours ago', distance: '1.2 miles'},
            {id: 4, lat: 40.7150, lng: -74.0150, type: 'suspicious', desc: 'Suspicious person', time: '1 day ago', distance: '0.3 miles'},
            {id: 5, lat: 40.7100, lng: -74.0080, type: 'hazard', desc: 'Fallen tree blocking road', time: '2 days ago', distance: '0.7 miles'}
        ];

        this.addIncidentsToMap();
        this.updateReportsList();
        this.updateFullReportsList();
    }

    loadNotifications() {
        this.notifications = [
            {
                id: 1,
                title: 'New Incident Near You',
                desc: 'A traffic accident was reported 0.3 miles from your location.',
                time: '2 minutes ago',
                icon: 'fas fa-exclamation-triangle',
                unread: true
            },
            {
                id: 2,
                title: 'Report Resolved',
                desc: 'Your report #1256 has been resolved by local authorities.',
                time: '1 hour ago',
                icon: 'fas fa-check-circle',
                unread: false
            },
            {
                id: 3,
                title: 'App Update Available',
                desc: 'Update to version 2.1.0 is now available with new features.',
                time: '3 hours ago',
                icon: 'fas fa-info-circle',
                unread: false
            },
            {
                id: 4,
                title: 'Emergency Alert',
                desc: 'Police activity reported in your area. Please avoid the area if possible.',
                time: '30 minutes ago',
                icon: 'fas fa-shield-alt',
                unread: true
            }
        ];
    }

    addIncidentsToMap() {
        if (!this.map) return;

        const incidentTypes = {
            'theft': {color: '#e53935', icon: 'fa-gem'},
            'vandalism': {color: '#ff9800', icon: 'fa-spray-can'},
            'accident': {color: '#1e88e5', icon: 'fa-car-crash'},
            'suspicious': {color: '#43a047', icon: 'fa-user-secret'},
            'hazard': {color: '#fdd835', icon: 'fa-exclamation-triangle'}
        };

        this.incidents.forEach(incident => {
            const typeInfo = incidentTypes[incident.type];
            if (typeInfo) {
                const marker = L.marker([incident.lat, incident.lng]).addTo(this.map);
                marker.bindPopup(`
                    <div>
                        <strong>${incident.type.toUpperCase()}</strong><br>
                        ${incident.desc}<br>
                        <small>${incident.time}</small>
                    </div>
                `);
            }
        });
    }

    updateReportsList() {
        const reportsList = document.getElementById('reports-list');
        if (!reportsList) return;

        reportsList.innerHTML = '';
        
        this.incidents.slice(0, 3).forEach(incident => {
            const reportCard = this.createReportCard(incident);
            reportsList.appendChild(reportCard);
        });
    }

    createReportCard(incident) {
        const card = document.createElement('div');
        card.className = 'report-card';
        
        const icons = {
            'theft': 'fa-gem',
            'vandalism': 'fa-spray-can',
            'accident': 'fa-car-crash',
            'suspicious': 'fa-user-secret',
            'hazard': 'fa-exclamation-triangle'
        };

        const colors = {
            'theft': '#e53935',
            'vandalism': '#ff9800',
            'accident': '#1e88e5',
            'suspicious': '#43a047',
            'hazard': '#fdd835'
        };

        card.innerHTML = `
            <div class="report-type">
                <i class="fas ${icons[incident.type]}" style="color: ${colors[incident.type]};"></i> 
                ${incident.type.charAt(0).toUpperCase() + incident.type.slice(1)}
            </div>
            <div class="report-desc">${incident.desc}</div>
            <div class="report-meta">
                <span>${incident.time}</span>
                <span>${incident.distance} away</span>
            </div>
        `;

        card.addEventListener('click', () => {
            if (this.map) {
                this.map.setView([incident.lat, incident.lng], 16);
            }
        });

        return card;
    }

    setupEventListeners() {
        // Report incident button
        const reportBtn = document.getElementById('report-incident-btn');
        if (reportBtn) {
            reportBtn.addEventListener('click', () => this.showScreen('report'));
        }

        // Emergency button
        const emergencyBtn = document.getElementById('emergency-btn');
        if (emergencyBtn) {
            emergencyBtn.addEventListener('click', () => this.handleEmergency());
        }

        // Form buttons
        const cancelBtn = document.getElementById('cancel-report');
        if (cancelBtn) {
            cancelBtn.addEventListener('click', () => this.showScreen('home'));
        }

        const submitBtn = document.getElementById('submit-report');
        if (submitBtn) {
            submitBtn.addEventListener('click', (e) => this.handleFormSubmit(e));
        }

        // Admin toggle
        const adminToggle = document.getElementById('admin-toggle');
        if (adminToggle) {
            adminToggle.addEventListener('click', () => this.toggleAdmin());
        }

        // Notification bell
        const notificationBell = document.querySelector('.nav-icons .fa-bell');
        if (notificationBell) {
            notificationBell.addEventListener('click', () => this.showScreen('notifications'));
        }

        // Map controls
        const refreshMapBtn = document.getElementById('refresh-map');
        if (refreshMapBtn) {
            refreshMapBtn.addEventListener('click', () => this.updateFullMap());
        }

        const centerLocationBtn = document.getElementById('center-location');
        if (centerLocationBtn) {
            centerLocationBtn.addEventListener('click', () => this.centerMapOnLocation());
        }

        // Mark all notifications as read
        const markAllReadBtn = document.getElementById('mark-all-read');
        if (markAllReadBtn) {
            markAllReadBtn.addEventListener('click', () => this.markAllNotificationsRead());
        }

        // Bottom navigation
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', () => {
                const screen = item.dataset.screen;
                this.showScreen(screen);
            });
        });

        // Location button
        const locationBtn = document.getElementById('get-location-btn');
        if (locationBtn) {
            locationBtn.addEventListener('click', () => this.useCurrentLocation());
        }

        // File upload
        const uploadArea = document.getElementById('upload-area');
        const fileInput = document.getElementById('media-upload');
        if (uploadArea && fileInput) {
            uploadArea.addEventListener('click', () => fileInput.click());
            fileInput.addEventListener('change', (e) => this.handleFileUpload(e));
        }

        // Form validation
        const form = document.getElementById('incident-form');
        if (form) {
            form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }

        // Profile menu items
        const profileMenuItems = document.querySelectorAll('.profile-menu-item');
        profileMenuItems.forEach(item => {
            item.addEventListener('click', () => {
                const action = item.id;
                this.handleProfileAction(action);
            });
        });

        // Filter button
        const filterBtn = document.getElementById('filter-reports');
        if (filterBtn) {
            filterBtn.addEventListener('click', () => this.showFilterOptions());
        }
    }

    handleEmergency() {
        // Show emergency confirmation
        if (confirm('Are you in immediate danger? This will contact emergency services.')) {
            this.showMessage('Emergency services have been contacted. Help is on the way!', 'error');
            
            // Add emergency notification
            const emergencyNotification = {
                id: Date.now(),
                title: 'Emergency Alert Sent',
                desc: 'Emergency services have been contacted. Stay safe and follow instructions.',
                time: 'Just now',
                icon: 'fas fa-exclamation-triangle',
                unread: true
            };
            
            this.notifications.unshift(emergencyNotification);
            this.updateNotificationsList();
        }
    }

    showScreen(screen) {
        const homeScreen = document.getElementById('home-screen');
        const mapScreen = document.getElementById('map-screen');
        const reportsScreen = document.getElementById('reports-screen');
        const profileScreen = document.getElementById('profile-screen');
        const notificationsScreen = document.getElementById('notifications-screen');
        const reportForm = document.getElementById('report-form');
        const adminDashboard = document.getElementById('admin-dashboard');
        const navItems = document.querySelectorAll('.nav-item');

        // Hide all screens
        [homeScreen, mapScreen, reportsScreen, profileScreen, notificationsScreen, reportForm, adminDashboard].forEach(screenEl => {
            if (screenEl) {
                screenEl.style.display = 'none';
                screenEl.classList.remove('active');
            }
        });

        // Show selected screen
        switch(screen) {
            case 'home':
                if (homeScreen) {
                    homeScreen.style.display = 'flex';
                    homeScreen.classList.add('active');
                    // Ensure map is properly sized
                    setTimeout(() => {
                        if (this.map) {
                            this.map.invalidateSize();
                        }
                    }, 100);
                }
                break;
            case 'map':
                if (mapScreen) {
                    mapScreen.style.display = 'flex';
                    mapScreen.classList.add('active');
                    this.updateFullMap();
                    // Ensure map is properly sized
                    setTimeout(() => {
                        if (this.mapFull) {
                            this.mapFull.invalidateSize();
                        }
                    }, 100);
                }
                break;
            case 'reports':
                if (reportsScreen) {
                    reportsScreen.style.display = 'flex';
                    reportsScreen.classList.add('active');
                    this.updateFullReportsList();
                }
                break;
            case 'profile':
                if (profileScreen) {
                    profileScreen.style.display = 'flex';
                    profileScreen.classList.add('active');
                    this.updateProfileStats();
                }
                break;
            case 'notifications':
                if (notificationsScreen) {
                    notificationsScreen.style.display = 'flex';
                    notificationsScreen.classList.add('active');
                    this.updateNotificationsList();
                }
                break;
            case 'report':
                if (reportForm) {
                    reportForm.style.display = 'flex';
                    reportForm.classList.add('active');
                }
                break;
            case 'admin':
                if (adminDashboard) {
                    adminDashboard.style.display = 'flex';
                    adminDashboard.classList.add('active');
                    this.updateAdminDashboard();
                }
                break;
        }

        this.currentScreen = screen;

        // Update navigation
        navItems.forEach(item => {
            if (item.dataset.screen === screen) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }

    toggleAdmin() {
        const adminDashboard = document.getElementById('admin-dashboard');
        if (adminDashboard && adminDashboard.style.display === 'flex') {
            this.showScreen('home');
        } else {
            this.showScreen('admin');
        }
    }

    useCurrentLocation() {
        const locationInput = document.getElementById('incident-location');
        if (this.currentLocation) {
            locationInput.value = `${this.currentLocation.lat.toFixed(4)}, ${this.currentLocation.lng.toFixed(4)}`;
        } else {
            this.getCurrentLocation();
            setTimeout(() => {
                if (this.currentLocation) {
                    locationInput.value = `${this.currentLocation.lat.toFixed(4)}, ${this.currentLocation.lng.toFixed(4)}`;
                }
            }, 2000);
        }
    }

    handleFileUpload(event) {
        const files = Array.from(event.target.files);
        const uploadedFilesDiv = document.getElementById('uploaded-files');
        
        if (files.length > 0) {
            uploadedFilesDiv.style.display = 'block';
            uploadedFilesDiv.innerHTML = '';
            
            files.forEach(file => {
                const fileDiv = document.createElement('div');
                fileDiv.className = 'uploaded-file';
                fileDiv.innerHTML = `
                    <div>
                        <i class="fas fa-file"></i>
                        ${file.name} (${this.formatFileSize(file.size)})
                    </div>
                    <button type="button" class="remove-file" onclick="this.parentElement.remove()">
                        <i class="fas fa-times"></i>
                    </button>
                `;
                uploadedFilesDiv.appendChild(fileDiv);
            });
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    handleFormSubmit(event) {
        event.preventDefault();
        
        const form = event.target;
        const formData = new FormData(form);
        
        const incidentType = document.getElementById('incident-type').value;
        const description = document.getElementById('incident-description').value;
        const location = document.getElementById('incident-location').value;

        if (!incidentType || !description) {
            this.showMessage('Please fill in all required fields.', 'error');
            return;
        }

        // Show loading state
        const submitBtn = document.getElementById('submit-report');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Submitting...';
        submitBtn.disabled = true;

        // Simulate API call
        setTimeout(() => {
            const newReport = {
                id: Date.now(),
                type: incidentType,
                description: description,
                location: location || 'Current Location',
                timestamp: new Date().toISOString(),
                status: 'pending'
            };

            this.reports.push(newReport);
            this.saveStoredData();
            this.updateAdminDashboard();
            
            this.showMessage('Incident reported successfully!', 'success');
            this.showScreen('home');
            
            // Reset form
            form.reset();
            document.getElementById('uploaded-files').style.display = 'none';
            
            // Reset button
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }, 1500);
    }

    showMessage(message, type) {
        // Remove existing messages
        const existingMessages = document.querySelectorAll('.message');
        existingMessages.forEach(msg => msg.remove());

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = message;

        const container = document.querySelector('.container');
        const header = document.querySelector('header');
        container.insertBefore(messageDiv, header.nextSibling);

        // Auto remove after 5 seconds
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }

    updateAdminDashboard() {
        // Update stats
        const reportsToday = this.reports.filter(report => {
            const today = new Date().toDateString();
            return new Date(report.timestamp).toDateString() === today;
        }).length;

        const pendingCount = this.reports.filter(report => report.status === 'pending').length;
        const resolvedCount = this.reports.filter(report => report.status === 'resolved').length;
        const responseRate = this.reports.length > 0 ? Math.round((resolvedCount / this.reports.length) * 100) : 0;

        const reportsTodayEl = document.getElementById('reports-today');
        const pendingCountEl = document.getElementById('pending-count');
        const resolvedCountEl = document.getElementById('resolved-count');
        const responseRateEl = document.getElementById('response-rate');

        if (reportsTodayEl) reportsTodayEl.textContent = reportsToday;
        if (pendingCountEl) pendingCountEl.textContent = pendingCount;
        if (resolvedCountEl) resolvedCountEl.textContent = resolvedCount;
        if (responseRateEl) responseRateEl.textContent = responseRate + '%';

        // Update incidents table
        this.updateIncidentsTable();
    }

    updateIncidentsTable() {
        const tableBody = document.getElementById('incidents-table-body');
        if (!tableBody) return;

        tableBody.innerHTML = '';
        
        this.reports.slice(-10).reverse().forEach(report => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>#${report.id}</td>
                <td>${report.type.charAt(0).toUpperCase() + report.type.slice(1)}</td>
                <td>${report.location}</td>
                <td><span class="status-badge status-${report.status}">${report.status}</span></td>
                <td><button class="btn btn-primary" style="padding: 5px 10px; font-size: 0.8rem;" onclick="app.viewReport(${report.id})">View</button></td>
            `;
            tableBody.appendChild(row);
        });
    }

    viewReport(reportId) {
        const report = this.reports.find(r => r.id === reportId);
        if (report) {
            alert(`Report Details:\n\nType: ${report.type}\nDescription: ${report.description}\nLocation: ${report.location}\nStatus: ${report.status}\nTime: ${new Date(report.timestamp).toLocaleString()}`);
        }
    }

    updateFullMap() {
        if (this.mapFull) {
            // Clear existing markers
            this.mapFull.eachLayer(layer => {
                if (layer instanceof L.Marker) {
                    this.mapFull.removeLayer(layer);
                }
            });
            
            // Add incidents to full map
            this.addIncidentsToFullMap();
            
            // Add user location if available
            if (this.currentLocation) {
                L.marker([this.currentLocation.lat, this.currentLocation.lng])
                    .addTo(this.mapFull)
                    .bindPopup('Your Location')
                    .openPopup();
            }
        }
    }

    addIncidentsToFullMap() {
        if (!this.mapFull) return;

        const incidentTypes = {
            'theft': {color: '#e53935', icon: 'fa-gem'},
            'vandalism': {color: '#ff9800', icon: 'fa-spray-can'},
            'accident': {color: '#1e88e5', icon: 'fa-car-crash'},
            'suspicious': {color: '#43a047', icon: 'fa-user-secret'},
            'hazard': {color: '#fdd835', icon: 'fa-exclamation-triangle'}
        };

        this.incidents.forEach(incident => {
            const typeInfo = incidentTypes[incident.type];
            if (typeInfo) {
                const marker = L.marker([incident.lat, incident.lng]).addTo(this.mapFull);
                marker.bindPopup(`
                    <div>
                        <strong>${incident.type.toUpperCase()}</strong><br>
                        ${incident.desc}<br>
                        <small>${incident.time}</small>
                    </div>
                `);
            }
        });
    }

    updateFullReportsList() {
        const reportsListFull = document.getElementById('reports-list-full');
        if (!reportsListFull) return;

        reportsListFull.innerHTML = '';
        
        this.incidents.forEach(incident => {
            const reportCard = this.createReportCard(incident);
            reportsListFull.appendChild(reportCard);
        });
    }

    updateNotificationsList() {
        const notificationsList = document.getElementById('notifications-list');
        if (!notificationsList) return;

        notificationsList.innerHTML = '';
        
        this.notifications.forEach(notification => {
            const notificationItem = document.createElement('div');
            notificationItem.className = `notification-item ${notification.unread ? 'unread' : ''}`;
            notificationItem.innerHTML = `
                <div class="notification-icon">
                    <i class="${notification.icon}"></i>
                </div>
                <div class="notification-content">
                    <div class="notification-title">${notification.title}</div>
                    <div class="notification-desc">${notification.desc}</div>
                    <div class="notification-time">${notification.time}</div>
                </div>
            `;
            notificationsList.appendChild(notificationItem);
        });
    }

    updateProfileStats() {
        const totalReports = this.reports.length;
        const resolvedReports = this.reports.filter(report => report.status === 'resolved').length;
        const pendingReports = this.reports.filter(report => report.status === 'pending').length;

        const totalEl = document.querySelector('.profile-stat-value');
        const resolvedEl = document.querySelectorAll('.profile-stat-value')[1];
        const pendingEl = document.querySelectorAll('.profile-stat-value')[2];

        if (totalEl) totalEl.textContent = totalReports;
        if (resolvedEl) resolvedEl.textContent = resolvedReports;
        if (pendingEl) pendingEl.textContent = pendingReports;
    }

    centerMapOnLocation() {
        if (this.currentLocation && this.mapFull) {
            this.mapFull.setView([this.currentLocation.lat, this.currentLocation.lng], 15);
        } else {
            this.getCurrentLocation();
            setTimeout(() => {
                if (this.currentLocation && this.mapFull) {
                    this.mapFull.setView([this.currentLocation.lat, this.currentLocation.lng], 15);
                }
            }, 2000);
        }
    }

    markAllNotificationsRead() {
        this.notifications.forEach(notification => {
            notification.unread = false;
        });
        this.updateNotificationsList();
        this.showMessage('All notifications marked as read', 'success');
    }

    handleProfileAction(action) {
        switch(action) {
            case 'edit-profile':
                this.showMessage('Edit profile feature coming soon!', 'success');
                break;
            case 'settings':
                this.showMessage('Settings feature coming soon!', 'success');
                break;
            case 'help-support':
                this.showMessage('Help & Support feature coming soon!', 'success');
                break;
            case 'about':
                alert('CivicGuardian v2.1.0\nCommunity Crime Reporting App\n\nBuilt with ❤️ for community safety');
                break;
            case 'logout':
                if (confirm('Are you sure you want to logout?')) {
                    this.showMessage('Logged out successfully', 'success');
                    setTimeout(() => {
                        this.showScreen('home');
                    }, 1000);
                }
                break;
        }
    }

    showFilterOptions() {
        const filterOptions = ['All', 'Theft', 'Vandalism', 'Accident', 'Suspicious', 'Hazard'];
        const selectedFilter = prompt(`Select filter:\n${filterOptions.map((option, index) => `${index}: ${option}`).join('\n')}`);
        
        if (selectedFilter !== null) {
            const filterIndex = parseInt(selectedFilter);
            if (filterIndex >= 0 && filterIndex < filterOptions.length) {
                this.filterReports(filterOptions[filterIndex]);
            }
        }
    }

    filterReports(filter) {
        const reportsListFull = document.getElementById('reports-list-full');
        if (!reportsListFull) return;

        reportsListFull.innerHTML = '';
        
        let filteredIncidents = this.incidents;
        if (filter !== 'All') {
            filteredIncidents = this.incidents.filter(incident => 
                incident.type.toLowerCase() === filter.toLowerCase()
            );
        }
        
        filteredIncidents.forEach(incident => {
            const reportCard = this.createReportCard(incident);
            reportsListFull.appendChild(reportCard);
        });
    }

    loadStoredData() {
        try {
            const storedReports = localStorage.getItem('civicGuardianReports');
            if (storedReports) {
                this.reports = JSON.parse(storedReports);
            }
        } catch (error) {
            console.log('Error loading stored data:', error);
        }
    }

    saveStoredData() {
        try {
            localStorage.setItem('civicGuardianReports', JSON.stringify(this.reports));
        } catch (error) {
            console.log('Error saving data:', error);
        }
    }
}

// Initialize the app when DOM is loaded
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new CivicGuardianApp();
});

// Make app globally available for onclick handlers
window.app = app;