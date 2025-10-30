# MinistryLearn Backend API

A comprehensive Flask-based REST API for the Ministry Learning Platform, providing authentication, course management, and learning management system functionality.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- PostgreSQL (or use the provided cloud database)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Dunamis-001/MinistryLearn-Backend.git
   cd MinistryLearn-Backend
   ```

2. **Create and activate virtual environment**
   ```bash
   # For Windows
   python -m venv venv
   venv\Scripts\activate

   # For Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your configuration
   nano .env  # or use your preferred editor
   ```

5. **Set up the database**
   ```bash
   # Run migrations
   flask db upgrade
   
   # Seed the database with initial data
   python seed_data.py
   ```

6. **Run the application**
   ```bash
   python wsgi.py
   ```

The API will be available at `http://127.0.0.1:5000`

## 📋 Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_APP=wsgi.py

# Database Configuration
DATABASE_URL=postgresql://username:password@host:port/database

# JWT Configuration
JWT_SECRET=your-secure-jwt-secret-here

# Cloudinary Configuration (for file uploads)
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name

# SendGrid Configuration (for emails)
SENDGRID_API_KEY=your-sendgrid-api-key

# CORS Configuration
CORS_ORIGINS=http://localhost:5173,http://your-frontend-ip:5173
```

### Required Services

- **Database**: PostgreSQL (local or cloud)
- **File Storage**: Cloudinary account
- **Email Service**: SendGrid account

## 🗄️ Database Setup

### Using Render (Recommended)

1. Create a PostgreSQL database on [Render](https://render.com)
2. Copy the external database URL
3. Update `DATABASE_URL` in your `.env` file

### Using Local PostgreSQL

1. Install PostgreSQL locally
2. Create a database named `ministrylearn`
3. Update `DATABASE_URL` in your `.env` file:
   ```env
   DATABASE_URL=postgresql://postgres:password@localhost:5432/ministrylearn
   ```

## 🔧 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://127.0.0.1:5000/docs/`
- **Health Check**: `http://127.0.0.1:5000/health/`

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get user profile
- `POST /api/auth/refresh` - Refresh access token

### Courses
- `GET /api/courses` - List all courses
- `POST /api/courses` - Create a new course
- `GET /api/courses/{id}` - Get course details
- `PUT /api/courses/{id}` - Update course
- `DELETE /api/courses/{id}` - Delete course

### Enrollments
- `GET /api/enrollments` - List user enrollments
- `POST /api/courses/{id}/enroll` - Enroll in a course
- `DELETE /api/enrollments/{id}` - Unenroll from course

### Modules & Lessons
- `GET /api/courses/{id}/modules` - List course modules
- `POST /api/courses/{id}/modules` - Create module
- `GET /api/modules/{id}/lessons` - List module lessons
- `POST /api/modules/{id}/lessons` - Create lesson

### Assessments
- `GET /api/courses/{id}/assessments` - List course assessments
- `POST /api/assessments/{id}/submit` - Submit assessment
- `GET /api/submissions` - List user submissions

### Media & Announcements
- `POST /api/media/upload` - Upload media files
- `GET /api/announcements` - List announcements
- `POST /api/announcements` - Create announcement

## 🧪 Testing

Run the test suite:
```bash
python test_app_load.py
```

## 🚀 Deployment

### Using Render (Recommended)

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set the following environment variables in Render:
   - `DATABASE_URL`
   - `JWT_SECRET`
   - `CLOUDINARY_URL`
   - `SENDGRID_API_KEY`
   - `CORS_ORIGINS`

### Using Heroku

1. Install Heroku CLI
2. Create a new Heroku app
3. Add PostgreSQL addon
4. Set environment variables
5. Deploy:
   ```bash
   git push heroku main
   ```

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- Input validation with Marshmallow
- SQL injection protection with SQLAlchemy ORM

## 📦 Dependencies

### Core Dependencies
- **Flask**: Web framework
- **SQLAlchemy**: ORM
- **Flask-JWT-Extended**: JWT authentication
- **Flask-CORS**: Cross-origin resource sharing
- **Marshmallow**: Serialization/validation

### Database
- **psycopg2-binary**: PostgreSQL adapter
- **Flask-Migrate**: Database migrations

### External Services
- **Cloudinary**: File storage
- **SendGrid**: Email service

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🔗 Links

- **Repository**: [MinistryLearn-Backend](https://github.com/Dunamis-001/MinistryLearn-Backend)
- **Frontend**: [MinistryLearn-Frontend](https://github.com/Dunamis-001/MinistryLearn-Frontend)
- **Live Demo**: [Coming Soon]

## 🆘 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/Dunamis-001/MinistryLearn-Backend/issues) page
2. Create a new issue with detailed information
3. Contact the development team

## 📝 Changelog

### v1.0.0
- Initial release
- User authentication system
- Course management
- Assessment system
- File upload support
- Email notifications
