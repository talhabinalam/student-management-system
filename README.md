# Student Management System

This **Student Management System** is a web application built using Django. It provides role-based access to manage students, staff, courses, subjects, and sessions. The system includes modules for user authentication, CRUD operations, notifications, attendance, leave management, and result handling.

## Features

### User Authentication and Role-Based Access
- **Admin (HOD)**: Comprehensive access to manage students, staff, courses, subjects, sessions, attendance, and notifications.
- **Staff**: Manage attendance, apply for leave, provide feedback, and manage student results.
- **Students**: View notifications, attendance, results, and apply for leave.

### Modules

#### HOD (Head of Department)
- **Student Management**:
  - Add, update, delete, and view student details.
- **Course Management**:
  - Add, update, delete, and view courses.
- **Staff Management**:
  - Add, update, delete, and view staff members.
- **Subject Management**:
  - Add, update, delete, and view subjects.
- **Session Management**:
  - Add, update, delete, and view academic sessions.
- **Notifications**:
  - Send and manage notifications for staff and students.
- **Attendance**:
  - View attendance records for students.
- **Leave Management**:
  - Approve or decline leave requests from staff and students.
- **Feedback**:
  - Respond to feedback from staff and students.

#### Staff
- **Notifications**:
  - View and mark notifications as read.
- **Attendance Management**:
  - Take and save attendance records.
  - View attendance details.
- **Leave Management**:
  - Apply for leave.
- **Feedback**:
  - Submit feedback to the HOD.
- **Result Management**:
  - Add and save student results.

#### Students
- **Notifications**:
  - View and mark notifications as read.
- **Attendance**:
  - View personal attendance records.
- **Leave Management**:
  - Apply for leave.
- **Feedback**:
  - Submit feedback to the HOD.
- **Results**:
  - View exam results.

## Installation

### Prerequisites
- **Python 3.8+**: Ensure Python is installed on your machine. Download it from [python.org](https://www.python.org).

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/student-management-system.git
   cd student-management-system
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate   # On macOS/Linux
   env\Scripts\activate    # On Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Configuration**
   Configure your database in the `settings.py` file. Example for PostgreSQL:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'student_management',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. **Apply Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

8. **Access the Application**
   Open your browser and go to `http://127.0.0.1:8000/`.

## Project Structure

- **`views.py`**: Contains views for handling requests for HOD, staff, and student modules.
- **`models.py`**: Defines database models for users, courses, subjects, attendance, and results.
- **`urls.py`**: URL routing for various modules and endpoints.
- **`templates/`**: Contains HTML templates for the application.
- **`static/`**: Holds static files like CSS, JavaScript, and images.

## Requirements

The `requirements.txt` file includes all necessary dependencies. Major dependencies include:
- **Django**: Python web framework.
- **Bootstrap**: Used for responsive design and styling.

## Overview
![image](https://github.com/user-attachments/assets/5cd80c29-a7ca-4bac-9826-de93d4b4d7ab)

This project demonstrates an end-to-end solution for managing a school or college system efficiently.

