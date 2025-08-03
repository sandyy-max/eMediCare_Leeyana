// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// API Helper Functions
class API {
    static async request(endpoint, options = {}) {
        const url = API_BASE_URL + endpoint;
        const config = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        // Handle body for POST/PUT requests
        if (options.body && typeof options.body === 'object') {
            config.body = JSON.stringify(options.body);
            // Ensure content type is set correctly for JSON requests
            config.headers['Content-Type'] = 'application/json';
        }

        console.log('API Request Config:', {
            url: url,
            method: config.method,
            headers: config.headers,
            body: config.body
        });
        
        // Additional debugging for content type
        console.log('Content-Type header:', config.headers['Content-Type']);
        console.log('Body type:', typeof config.body);
        console.log('Body stringified:', JSON.stringify(config.body));

        try {
            const response = await fetch(url, config);
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || errorData.error || `API request failed: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API request error:', error);
            throw error;
        }
    }

    // Authentication methods
    static async login(credentials) {
        return this.request('/token/', {
            method: 'POST',
            body: credentials
        });
    }

    static async register(userData) {
        return this.request('/register/', {
            method: 'POST',
            body: userData
        });
    }

    // Appointment methods
    static async bookAppointment(appointmentData) {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('Authentication required');
        }
        return this.request('/appointments/', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: appointmentData
        });
    }

    static async getDoctorsByDepartment(department) {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('Authentication required');
        }
        return this.request(`/appointments/doctors/?department=${encodeURIComponent(department)}`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
    }

    static async getUpcomingAppointments() {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('Authentication required');
        }
        return this.request('/appointments/upcoming/', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
    }

    static async rejectAppointment(appointmentId, reason) {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('Authentication required');
        }
        return this.request(`/appointments/reject/${appointmentId}/`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: { reason: reason }
        });
    }

    // Package methods
    static async getPackages() {
        return this.request('/packages/', { method: 'GET' });
    }

    static async buyPackage(packageData) {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('Please login first to purchase packages');
        }
        return this.request('/packages/purchase/', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: packageData
        });
    }

    // Pharmacy methods
    static async getMedicines() {
        return this.request('/pharmacy/medicines/', { method: 'GET' });
    }

    static async requestMedicine(medicineData) {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('Please login first to request medicines');
        }
        
        // Check if there's a file to upload
        const formData = new FormData();
        
        // Add all medicine data to form
        Object.keys(medicineData).forEach(key => {
            if (key === 'prescription_file' && medicineData[key]) {
                formData.append('prescription_file', medicineData[key]);
            } else {
                formData.append(key, medicineData[key]);
            }
        });
        
        return this.request('/pharmacy/request/', {
            method: 'POST',
            headers: { 
                'Authorization': `Bearer ${token}`,
                // Remove Content-Type for FormData to let browser set it with boundary
            },
            body: formData
        });
    }

    static async uploadPrescription(formData) {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('Please login first to upload prescriptions');
        }
        return this.request('/pharmacy/prescriptions/upload/', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData
        });
    }

    // Medical history methods
    static async getMedicalHistory() {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('Authentication required');
        }
        return this.request('/clinical/history/', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
    }

    // Profile methods
    static async getProfile() {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('Authentication required');
        }
        return this.request('/user/profile/', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
    }

    static async updateProfile(profileData) {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('Authentication required');
        }
        return this.request('/user/profile/', {
            method: 'PUT',
            headers: { 'Authorization': `Bearer ${token}` },
            body: profileData
        });
    }

    static async getMedicalInfo() {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('Authentication required');
        }
        return this.request('/user/medical-info/', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
    }

    static async updateMedicalInfo(medicalData) {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('Authentication required');
        }
        return this.request('/user/medical-info/', {
            method: 'PUT',
            headers: { 'Authorization': `Bearer ${token}` },
            body: medicalData
        });
    }

    static async changePassword(currentPassword, newPassword) {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('Authentication required');
        }
        return this.request('/user/change-password/', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: { current_password: currentPassword, new_password: newPassword }
        });
    }

    static async updatePreferences(preferencesData) {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('Authentication required');
        }
        return this.request('/user/preferences/', {
            method: 'PUT',
            headers: { 'Authorization': `Bearer ${token}` },
            body: preferencesData
        });
    }

    // Notification methods
    static async getNotifications() {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('Authentication required');
        }
        return this.request('/notifications/', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
    }

    static async markNotificationAsRead(notificationId) {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('Authentication required');
        }
        return this.request(`/notifications/${notificationId}/mark-read/`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
    }

    static async getUnreadCount() {
        const token = localStorage.getItem('access_token');
        if (!token) {
            return 0;
        }
        try {
            const response = await this.request('/notifications/unread-count/', {
                method: 'GET',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            return response.count || 0;
        } catch (error) {
            console.error('Error getting unread count:', error);
            return 0;
        }
    }
}

// Utility Functions
const Utils = {
    setToken(token) {
        localStorage.setItem('access_token', token);
    },

    getToken() {
        return localStorage.getItem('access_token');
    },

    removeToken() {
        localStorage.removeItem('access_token');
    },

    isLoggedIn() {
        return !!localStorage.getItem('access_token');
    },

    showSuccess(message) {
        alert('Success: ' + message);
    },

    showError(message) {
        alert('Error: ' + message);
    },

    navigateTo(url) {
        window.location.href = url;
    },

    logout() {
        this.removeToken();
        this.navigateTo('../home.html');
    }
}; 