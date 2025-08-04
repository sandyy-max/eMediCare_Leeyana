# eMediCare - Hospital Management System

A comprehensive healthcare management system built with Django REST Framework and modern frontend technologies. This platform streamlines patient appointments, medical records, pharmacy requests, notifications, and health package management.

## Key Features

### Authentication & User Management
- Patient registration and login (JWT tokens)
- Profile management and password change
- Role-based access for patients and administrators

### Appointment Management
- Book appointments by department (Cardiology, Pulmonology, etc.)
- Dynamic doctor selection and appointment tracking
- Admin approval and notifications

### Pharmacy System
- Medicine catalog browsing
- Prescription upload and medicine requests
- Request tracking and admin processing

### Medical History
- View prescriptions, reports, and doctor assignments
- Automated medicine reminders
- Full CRUD for medical records

### Health Packages
- Browse, purchase, and track health packages with discounts
- Admin package management

### Notification System
- Real-time notifications for all activities
- Centralized notification page

### User Interface
- Responsive, consistent design across devices
- Interactive dashboard

---

## Technology Stack

**Backend:**  
- Django 5.2.4, Django REST Framework 3.16.0  
- JWT Authentication, SQLite/PostgreSQL  
- Django Jazzmin, DRF YASG

**Frontend:**  
- HTML5/CSS3, JavaScript (ES6+), Fetch API  
- Local Storage

**Libraries:**  
- Pillow, Twilio, Django Anymail, Django OTP, Phone Number Field

---

## Installation

**Prerequisites:**  
- Python 3.8+, pip

**Steps:**
1. Clone the Repository
   ```bash
   git clone <repository-url>
   cd eMediCare_last
   ```
2. Set Up Virtual Environment
   ```bash
   cd server
   python -m venv env
   # Windows:
   env\Scripts\activate
   # macOS/Linux:
   source env/bin/activate
   ```
3. Install Dependencies
   ```bash
   cd emedicare
   pip install -r requirements.txt
   ```
4. Run Migrations
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Create Superuser
   ```bash
   python manage.py createsuperuser
   ```
6. Start Server
   ```bash
   # Windows:
   start_server.bat
   # Manual:
   python manage.py runserver
   ```
   Access at `http://localhost:8000`

---

## Quick Start

- Open `client/home.html` or visit `http://localhost:8000`
- Register or login
- Explore appointments, pharmacy, medical history, health packages, notifications, and profile management

---

## Project Structure

```
eMediCare_last/
├── client/
│   ├── home.html
│   ├── userauth/
│   ├── dashboard/
│   ├── package/
│   ├── pharmacy/
│   ├── medical_history/
│   ├── notifications.html
│   └── js/
├── server/
│   └── emedicare/
├── requirements.txt
├── start_server.bat
└── README.md
```

---

## Configuration

**Environment Variables:**  
Create `.env` in `server/emedicare/`:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Database:**  
SQLite by default. For production, update `settings.py` for PostgreSQL.

---

## User Roles

**Patient:**  
- Register, book appointments, upload prescriptions, view history, buy packages, manage profile, receive notifications

**Administrator:**  
- Approve appointments, assign doctors, manage inventory, process requests, manage packages, send notifications, view analytics

---

## Security Features

- JWT authentication, CORS protection, input validation, SQL injection and XSS protection, role-based access

---

## Testing

**Manual Testing:**  
- Test registration, login, bookings, medicine requests, notifications, profile, medical history

**API Testing:**  
Use Postman or curl for endpoints (see original for examples).

---

## Deployment

**Development:**  
- Use `start_server.bat` or `python manage.py runserver`

**Production:**  
- Set `DEBUG=False`, configure database and environment variables, use Gunicorn

---

## Support

- Review documentation and code comments
- Use sample data for testing
- Check notification system for errors

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test
4. Submit a pull request

---

## License

MIT License.

---

## Acknowledgments

- Django and DRF teams
- Contributors and testers
- Healthcare professionals

Made With ❤️ by SANDHYA

---

Developed by SANDHYA for better healthcare management.
