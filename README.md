# University Education System
## Overview
This project is a University Education System designed to manage various components of a university, including user authentication, course management, registration, grading, academic management, communication, and academic transcripts. The backend is built with Django, while the frontend utilizes React.

## Features
- **Authentication and User Management:** Allows users to register, login, and manage their accounts. Supports different user roles such as students, professors, and administrators.
- **Education System:** Manages courses, departments, and semesters.
- **Registration System:** Handles course and semester registrations for students.
- **Grading System:** Manages grades, evaluations, and academic performance.
- **Academic Management:** Manages academic calendars and events.
- **Communication System:** Facilitates communication between users through messages and notifications.
- **Academic Service System:** Generates and manages academic transcripts for students.

## Technologies Used
- **Backend:** Django, Django REST Framework
- **Frontend:** React, Redux (optional)
- **Database:** PostgreSQL 
- **Other Tools:** npm, Webpack, Babel, Django REST Framework, React Router, Axios, etc.

## Setup Instructions
1. Backend Setup:

- Navigate to the backend directory.
- Create a virtual environment: python3 -m venv venv.
- Activate the virtual environment: source venv/bin/activate.
- Install dependencies: pip install -r requirements.txt.
- Set up the database: python manage.py migrate.
- Create a superuser: python manage.py createsuperuser.
- Run the development server: python manage.py runserver.
2. Frontend Setup:

- Navigate to the frontend directory.
- Install dependencies: npm install.
- Start the development server: npm start.
3. Accessing the Application:

- Backend API: http://localhost:8000/api/
- Frontend UI: http://localhost:3000/

## Our Team
![Team Image](team.png)


## License
This project is licensed under the MIT License.
