// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// API Helper Functions
class API {
    static async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'API request failed');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // User Authentication APIs
    static async register(userData) {
        return this.request('/register/', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    static async login(credentials) {
        return this.request('/token/', {
            method: 'POST',
            body: JSON.stringify(credentials)
        });
    }

    static async getProfile() {
        const token = localStorage.getItem('access_token');
        return this.request('/user/profile/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
    }

    static async getUserProfile() {
        const token = localStorage.getItem('access_token');
        return this.request('/user/profile/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
    }

    static async updateUserProfile(profileData) {
        const token = localStorage.getItem('access_token');
        return this.request('/user/profile/', {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(profileData)
        });
    }

    static async updateMedicalInfo(medicalData) {
        const token = localStorage.getItem('access_token');
        return this.request('/user/medical-info/', {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(medicalData)
        });
    }

    static async changePassword(currentPassword, newPassword) {
        const token = localStorage.getItem('access_token');
        return this.request('/user/change-password/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                current_password: currentPassword,
                new_password: newPassword
            })
        });
    }

    static async updatePreferences(preferencesData) {
        const token = localStorage.getItem('access_token');
        return this.request('/user/preferences/', {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(preferencesData)
        });
    }

    // Appointment APIs
    static async bookAppointment(appointmentData) {
        const token = localStorage.getItem('access_token');
        return this.request('/appointments/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(appointmentData)
        });
    }

    // Package APIs
    static async getPackages() {
        return this.request('/packages/');
    }

    static async buyPackage(packageData) {
        const token = localStorage.getItem('access_token');
        return this.request('/packages/buy/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(packageData)
        });
    }

    // Medical History APIs
    static async getMedicalHistory() {
        const token = localStorage.getItem('access_token');
        return this.request('/clinical/history/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
    }

    // Pharmacy APIs
    static async getMedicines() {
        return this.request('/pharmacy/medicines/');
    }

    static async requestMedicine(requestData) {
        const token = localStorage.getItem('access_token');
        return this.request('/pharmacy/request/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(requestData)
        });
    }

    static async uploadPrescription(prescriptionData) {
        const token = localStorage.getItem('access_token');
        return this.request('/pharmacy/prescriptions/upload/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(prescriptionData)
        });
    }
}

// Utility Functions
const Utils = {
    // Store user token
    setToken(token) {
        localStorage.setItem('access_token', token);
    },

    // Get stored token
    getToken() {
        return localStorage.getItem('access_token');
    },

    // Remove token (logout)
    removeToken() {
        localStorage.removeItem('access_token');
    },

    // Check if user is logged in
    isLoggedIn() {
        return !!this.getToken();
    },

    // Show success message
    showSuccess(message) {
        alert(message); // You can replace this with a better UI
    },

    // Show error message
    showError(message) {
        alert('Error: ' + message); // You can replace this with a better UI
    },

    // Navigate to page
    navigateTo(page) {
        window.location.href = page;
    }
};

// Export for use in other files
window.API = API;
window.Utils = Utils; 