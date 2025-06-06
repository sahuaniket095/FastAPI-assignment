# FastAPI Role-Based Quiz API

The **FastAPI Role-Based Quiz API** is a secure and efficient web application designed with FastAPI, PostgreSQL, and SQLAlchemy. It utilizes JWT (JSON Web Tokens) for authentication and implements role-based access control (RBAC). The system differentiates between Admin and Participant roles to provide appropriate access levels. Admin users can create and manage quizzes, while Participants can attempt quizzes and view their results. This structure ensures secure, organized management of quizzes and user activities.

---

## 🚀 Project Overview

This API allows for the creation, management, and participation in quizzes, with role-based permissions:

- **Admins**: Have full control to create, update, and delete quizzes and questions.
- **Participants**: Can browse available quizzes, submit answers, and check their scores.
- **Key Features**:
  - Secure authentication using JWT.
  - Scalable database design using PostgreSQL.
  - Interactive API interface powered by FastAPI's built-in Swagger UI.

---

## 🛠️ Technologies & Tools Used

- **FastAPI**: A modern, fast web framework for building APIs with Python.
- **PostgreSQL**: A robust, open-source relational database management system.
- **SQLAlchemy**: An Object-Relational Mapper (ORM) for easy database interaction.
- **JWT**: JSON Web Tokens for secure, stateless authentication.
- **Pydantic**: For data validation and creating API schemas.
- **Python 3.8+**: The programming language used to develop the backend.

---

## 📋 Prerequisites

To run this project, ensure you have the following installed on your system:

- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **PostgreSQL**: [Download PostgreSQL](https://www.postgresql.org/download/)
- **PgAdmin** (optional, for database management): [Download PgAdmin](https://github.com/pgadmin-org/pgadmin4.git)

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
Start by cloning the repository to your local machine:

git clone https://github.com/sahuaniket095/FastAPI-assignment-1.git
cd FastAPI-assignment-1

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```
git clone https://github.com/sahuaniket095/FastAPI-assignment-1.git
cd FastAPI-assignment-1
```
### 2. Create a Virtual Environment
```
python -m venv venv
#on Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```
### 3. Install Dependencies
```
pip install -r requirements.txt
```
### 4. Set Up the PostgreSQL Database

To set up the PostgreSQL database, follow these steps:

1. **Open pgAdmin 4**:
   - Launch pgAdmin 4 from your start menu or by searching for it on your computer.
   - If you haven't set a master password yet, create one when prompted.

2. **Register a New Server**:
- In the pgAdmin 4 interface, navigate to the **Servers** section on the left.
- Right-click on **Servers** and select **Register** > **Server**.
- Fill in the server details as shown above.
- Click **Save** to register the server.

3. **Create a New Database**:
- Expand the newly registered server in the **Servers** list.
- Right-click on **Databases** and select **New Database**.
- Fill in the database details:
  - **Database Name**: Choose a name for your database.
  - **Owner**: Select the owner from the dropdown list.
- Click **Save** to create the database.

4. **Run the Query Script**:
- Expand the newly created database in the **Databases** list.
- Right-click on the database and select **Query Tool**.
- Open the `QuizDatabaseQuery.sql` file and copy its contents into the Query Tool window.
- Click the **Play** button or press `F5` to execute the SQL script and create the tables for your database.

4. **Configure Database Credentials:**:
- Open **database.py** and update the **SQLALCHEMY_DATABASE_URL**:
```
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:YourPassword@localhost/DatabaseName"
```
- Replace YourPassword with your PostgreSQL password.

### How to Run the Application
### 1. Start the FastAPI Server:
```
uvicorn main:app --reload
```

### Access the API:
Open your browser and go to http://localhost:8000/docs for the Swagger UI.
