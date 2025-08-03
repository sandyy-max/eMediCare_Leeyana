# 🏥 eMediCare - Hospital Management System

A comprehensive hospital management system built with Django REST Framework and modern frontend technologies. This system provides a complete solution for managing patient appointments, medical records, pharmacy operations, health packages, and notifications.

## 🌟 Features

### 🔐 Authentication & User Management
- **Patient Registration & Login** - Secure user authentication with JWT tokens
- **Profile Management** - Users can view and edit their personal information
- **Password Change** - Secure password update functionality
- **Role-based Access** - Different access levels for patients and administrators

### 📅 Appointment Management
- **Book Appointments** - Patients can book appointments with different departments
- **Department Selection** - Cardiology, Pulmonology, Dermatology, Pediatrics, Gynecology
- **Dynamic Doctor Loading** - Shows available doctors based on selected department
- **Appointment Tracking** - View appointment status and history
- **Admin Approval** - Administrators can approve, confirm, or reject appointments
- **Notification System** - Real-time notifications for appointment status changes
- **Upcoming Appointments** - View confirmed appointments with doctor details

### 💊 Pharmacy System
- **Medicine Catalog** - Browse available medicines with details
- **Medicine Requests** - Patients can request specific medicines with prescription upload
- **Request Tracking** - Track medicine request status
- **Admin Management** - Administrators can process and manage medicine requests

### 📋 Medical History
- **Prescription Records** - View past prescriptions and medical history
- **Doctor Assignments** - Track which doctors provided treatment
- **Medicine Reminders** - Automated reminders for medicine schedules
- **Medical Reports** - Access to medical reports and diagnoses
- **CRUD Operations** - Complete Create, Read, Update, Delete functionality

### 🏥 Health Packages
- **Package Browsing** - View available health checkup packages with pricing
- **Package Purchase** - Buy health packages online with discount options
- **Package Management** - Track purchased packages and their status
- **Admin Package Management** - Add and manage health packages
- **Discount Display** - Show original and discounted prices

### 📱 Notification System
- **Real-time Notifications** - Comprehensive notification system for all activities
- **Notification Types** - System, appointment, medicine, package, and admin notifications
- **Read/Unread Status** - Track notification status
- **Unified Notification Page** - Centralized notification management
- **Admin Notifications** - Administrators receive notifications for all activities

### 🎨 Modern UI/UX
- **Responsive Design** - Works on all devices
- **Consistent Design Language** - Unified design across all pages
- **Interactive Elements** - Modern buttons, forms, and navigation
- **Loading States** - Smooth user experience with loading indicators
- **Professional Dashboard** - Enhanced patient dashboard with health news

## 🛠️ Technology Stack

### Backend
- **Django 5.2.4** - Main web framework
- **Django REST Framework 3.16.0** - API development
- **JWT Authentication** - Secure token-based authentication
- **SQLite/PostgreSQL** - Database management
- **CORS Headers** - Cross-origin resource sharing
- **Django Jazzmin** - Enhanced admin interface
- **DRF YASG** - API documentation

### Frontend
- **HTML5/CSS3** - Modern, responsive design
- **JavaScript (ES6+)** - Dynamic functionality
- **Fetch API** - HTTP requests to backend
- **Local Storage** - Client-side data persistence

### Additional Libraries
- **Pillow** - Image processing
- **Twilio** - SMS integration
- **Django Anymail** - Email integration
- **Django OTP** - Two-factor authentication
- **Phone Number Field** - Phone number validation

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd eMediCare_last
```

### Step 2: Set Up Virtual Environment
```bash
cd server
python -m venv env
# On Windows:
env\Scripts\activate
# On macOS/Linux:
source env/bin/activate
```

### Step 3: Install Dependencies
```bash
cd emedicare
pip install -r requirements.txt
```

### Step 4: Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### Step 6: Start the Server
```bash
# Option 1: Using the batch file (Windows)
start_server.bat

# Option 2: Manual start
python manage.py runserver
```

The server will be available at `http://localhost:8000`

## 🚀 Quick Start

### 1. Access the Application
- Open `client/home.html` in your browser
- Or navigate to `http://localhost:8000` (if configured)

### 2. Register/Login
- Click "Register Now" to create a new account
- Or use existing credentials to login

### 3. Explore Features
- **Book Appointments** - Select department and book appointments with dynamic doctor loading
- **Browse Pharmacy** - View and request medicines with prescription upload
- **Check Medical History** - View past prescriptions and medical records
- **Buy Health Packages** - Purchase health checkup packages with discounts
- **Manage Profile** - Update personal information and change password
- **View Notifications** - Check all system notifications in one place
- **View My Appointments** - See upcoming appointments with doctor details

## 📁 Project Structure

```
eMediCare_last/
├── client/                     # Frontend files
│   ├── home.html              # Landing page
│   ├── userauth/              # Authentication pages
│   │   ├── login.html
│   │   ├── register.html
│   │   └── appointment.html   # Appointment booking
│   ├── dashboard/             # User dashboard
│   │   ├── dashboard.html
│   │   ├── profile.html
│   │   └── my_appointments.html
│   ├── package/              # Health packages
│   │   └── package.html
│   ├── pharmacy/             # Pharmacy system
│   │   └── pharmacy.html
│   ├── medical_hitory/       # Medical history
│   │   └── medical_history.html
│   ├── notifications.html    # Notification center
│   └── js/
│       └── api.js           # API helper functions
├── server/
│   └── emedicare/            # Django backend
│       ├── userauth/         # User authentication app
│       ├── appointment/      # Appointment management
│       ├── clinical/         # Medical records
│       ├── pharmacy/         # Pharmacy system
│       ├── package/          # Health packages
│       ├── notification/     # Notifications
│       ├── manage.py         # Django management script
│       └── db.sqlite3        # Database file
├── requirements.txt           # Python dependencies
├── start_server.bat          # Windows server startup script
└── README.md                 # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in `server/emedicare/` with:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Configuration
The project uses SQLite by default. For production, update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 👥 User Roles

### Patient
- Register and login with secure authentication
- Book appointments with department-based doctor selection
- Request medicines with prescription upload
- View comprehensive medical history
- Purchase health packages with discount options
- Manage profile and change password
- Receive real-time notifications for all activities
- View upcoming appointments with doctor details

### Administrator
- Approve, confirm, or reject appointments
- Assign doctors to appointments
- Manage medicine inventory and requests
- Process medicine requests with status updates
- Manage health packages with pricing
- Send notifications to patients
- View system analytics and reports

## 🔒 Security Features

- **JWT Authentication** - Secure token-based authentication
- **CORS Protection** - Cross-origin request security
- **Input Validation** - Server-side data validation
- **SQL Injection Protection** - Django ORM protection
- **XSS Protection** - Built-in Django security
- **Password Security** - Secure password change functionality
- **Role-based Access Control** - Different permissions for different user types

## 🧪 Testing

### Manual Testing
1. **Registration Flow** - Test user registration with validation
2. **Login Flow** - Test authentication with JWT tokens
3. **Appointment Booking** - Test appointment creation with department selection
4. **Medicine Requests** - Test medicine request with prescription upload
5. **Notification System** - Test all notification types
6. **Profile Management** - Test profile updates and password changes
7. **Medical History** - Test CRUD operations for medical records

### API Testing
Use tools like Postman or curl to test API endpoints:
```bash
# Login
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number":"1234567890","password":"test123"}' \
  -H "Accept: application/json"

# Book Appointment
curl -X POST http://localhost:8000/api/appointments/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"full_name":"John Doe","phone_number":"1234567890","department":"Cardiology","symptoms":"Chest pain","email":"john@example.com","dob":"1990-01-01"}'

# Get Medical History
curl -X GET http://localhost:8000/api/clinical/history/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get Upcoming Appointments
curl -X GET http://localhost:8000/api/appointments/upcoming/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🚀 Deployment

### Development
```bash
# Windows
start_server.bat

# Manual
python manage.py runserver
```

### Production
1. Set `DEBUG = False` in settings
2. Configure production database
3. Set up environment variables
4. Use Gunicorn:
```bash
gunicorn emedicare.wsgi:application
```

## 📞 Support

For issues and questions:
- Check the documentation
- Review the code comments
- Test with the provided sample data
- Check the notification system for error messages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Django community for the excellent framework
- DRF team for the REST API framework
- All contributors and testers
- Healthcare professionals for domain expertise

---

**Made with ❤️ for better healthcare management**

## 🆕 Recent Updates

### Version 2.2 (Latest)
- ✅ **Enhanced Pharmacy System** - Complete medicine request system with prescription file upload
- ✅ **File Upload Support** - PNG/JPG prescription images (5MB max, 10KB min) with validation
- ✅ **Admin Medicine Management** - Approve/reject requests with comments, mark as "in progress"
- ✅ **Comprehensive Notifications** - All medicine request status updates sent to patients
- ✅ **Local Storage Implementation** - File storage ready with cloud storage discussion
- ✅ **Enhanced Appointment System** - Fixed appointment display issues and added proper confirmation handling
- ✅ **Improved Medical History** - Complete CRUD operations for medical records
- ✅ **Enhanced Dashboard** - Professional design with health news and better navigation
- ✅ **Unified Design** - Consistent design language across all pages
- ✅ **Better Error Handling** - Improved API error handling and user feedback
- ✅ **Admin Notifications** - Enhanced notification system for administrators
- ✅ **Database Optimization** - Improved data structure and relationships
- ✅ **Code Cleanup** - Removed unnecessary test files and improved code organization 