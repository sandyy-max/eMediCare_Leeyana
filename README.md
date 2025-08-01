# 🏥 eMediCare - Hospital Management System

A comprehensive hospital management system built with Django REST Framework and modern frontend technologies. This system provides a complete solution for managing patient appointments, medical records, pharmacy operations, and health packages.

## 🌟 Features

### 🔐 Authentication & User Management
- **Patient Registration & Login** - Secure user authentication with JWT tokens
- **Profile Management** - Users can view and edit their personal information
- **Role-based Access** - Different access levels for patients and administrators

### 📅 Appointment Management
- **Book Appointments** - Patients can book appointments with different departments
- **Department Selection** - Cardiology, Pulmonology, Dermatology, Pediatrics, Gynecology
- **Appointment Tracking** - View appointment status and history
- **Admin Approval** - Administrators can approve and assign doctors to appointments

### 💊 Pharmacy System
- **Medicine Catalog** - Browse available medicines with details
- **Medicine Requests** - Patients can request specific medicines
- **Prescription Upload** - Upload prescription documents
- **Order Tracking** - Track medicine request status

### 📋 Medical History
- **Prescription Records** - View past prescriptions and medical history
- **Doctor Assignments** - Track which doctors provided treatment
- **Medical Reports** - Access to medical reports and diagnoses

### 🏥 Health Packages
- **Package Browsing** - View available health checkup packages
- **Package Purchase** - Buy health packages online
- **Package Management** - Track purchased packages and their status

### 📱 User Dashboard
- **Personal Dashboard** - Centralized view of all patient activities
- **Navigation System** - Easy access to all features
- **Real-time Updates** - Live status updates for appointments and requests

## 🛠️ Technology Stack

### Backend
- **Django 5.2.4** - Main web framework
- **Django REST Framework** - API development
- **JWT Authentication** - Secure token-based authentication
- **SQLite/PostgreSQL** - Database management
- **CORS Headers** - Cross-origin resource sharing

### Frontend
- **HTML5/CSS3** - Modern, responsive design
- **JavaScript (ES6+)** - Dynamic functionality
- **Fetch API** - HTTP requests to backend
- **Local Storage** - Client-side data persistence

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd eMediCare_last
```

### Step 2: Install Dependencies
```bash
cd server/emedicare
pip install -r requirements.txt
```

### Step 3: Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### Step 5: Start the Server
```bash
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
- **Book Appointments** - Select department and book appointments
- **Browse Pharmacy** - View and request medicines
- **Check Medical History** - View past prescriptions
- **Buy Health Packages** - Purchase health checkup packages
- **Manage Profile** - Update personal information

## 📁 Project Structure

```
eMediCare_last/
├── client/                     # Frontend files
│   ├── home.html              # Landing page
│   ├── userauth/              # Authentication pages
│   │   ├── login.html
│   │   └── register.html
│   ├── dashboard/             # User dashboard
│   ├── package/              # Health packages
│   ├── pharmacy/             # Pharmacy system
│   └── medical_hitory/       # Medical history
├── server/
│   └── emedicare/            # Django backend
│       ├── userauth/         # User authentication app
│       ├── appointment/      # Appointment management
│       ├── clinical/         # Medical records
│       ├── pharmacy/         # Pharmacy system
│       ├── package/          # Health packages
│       └── notification/     # Notifications
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
- Register and login
- Book appointments
- Request medicines
- View medical history
- Purchase health packages
- Manage profile

### Administrator
- Approve appointments
- Assign doctors
- Manage medicine inventory
- Process medicine requests
- Manage health packages
- View system analytics

## 🔒 Security Features

- **JWT Authentication** - Secure token-based authentication
- **CORS Protection** - Cross-origin request security
- **Input Validation** - Server-side data validation
- **SQL Injection Protection** - Django ORM protection
- **XSS Protection** - Built-in Django security

## 🧪 Testing

### Manual Testing
1. **Registration Flow** - Test user registration
2. **Login Flow** - Test authentication
3. **Appointment Booking** - Test appointment creation
4. **API Endpoints** - Test all REST API endpoints

### API Testing
Use tools like Postman or curl to test API endpoints:
```bash
# Login
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number":"1234567890","password":"test123"}'

# Book Appointment
curl -X POST http://localhost:8000/api/appointments/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"full_name":"John Doe","phone_number":"1234567890","department":"Cardiology","symptoms":"Chest pain"}'
```

## 🚀 Deployment

### Development
```bash
python manage.py runserver
```

### Production
1. Set `DEBUG = False` in settings
2. Configure production database
3. Use Gunicorn:
```bash
gunicorn emedicare.wsgi:application
```

## 📞 Support

For issues and questions:
- Check the documentation
- Review the code comments
- Test with the provided sample data

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

---

**Made with ❤️ for better healthcare management** 