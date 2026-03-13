# 🚀 TaskMaster — Project & Task Management System (Django)-- https://klickit2015.pythonanywhere.com/projects/

TaskMaster is a full-featured **project management and team collaboration** platform built with  
**Django + Tailwind CSS**, featuring authentication, role-based access, project tracking, kanban board,  
task management, comments, and a modern UI.

---
<img width="1919" height="996" alt="image" src="https://github.com/user-attachments/assets/55a8b899-298c-452b-99be-a451d81477de" />

<img width="1914" height="999" alt="image" src="https://github.com/user-attachments/assets/8d32497b-707a-4456-aaf9-e81a9ffbd6bf" />

## ⭐ Features

### 🔐 Authentication & Users
- Custom User model (Admin / Manager / Member)
- Registration, login, logout
- User profile with statistics
- Role-based permissions

### 📊 Dashboard
- Real-time stats
- Recent projects
- Recent tasks
- Progress indicators
- Quick actions

### 📁 Project Management
- Create / Update / Delete projects
- Assign members
- Track progress
- Status management (Planning → Completed)
- Due date and overdue detection

### 📋 Task Management
- Kanban style task board:
  - To Do → In Progress → Review → Completed
- Task assignment
- Priority levels
- Comments system
- Attachments model (ready)
- Due date alerts

### 💬 Collaboration
- Add comments on tasks
- Activity tracking (model ready)
- User mentions supported (future ready)

### 🎨 UI/UX
- Responsive design (mobile friendly)
- Tailwind CSS styling
- Smooth animations
- Modern dashboard UI
- Gradient cards & buttons

---

## 📂 Project Structure

taskmaster_project/
│
├── taskmaster/ # Core settings & URLs
├── accounts/ # Authentication app
├── projects/ # Projects app
├── tasks/ # Tasks & comments app
├── templates/ # All HTML templates
├── static/ # CSS/JS/Images
├── media/ # Uploaded files
├── requirements.txt
└── manage.py

yaml
Copy code

---

## 🗄️ Models Included
- **CustomUser**
- **Project**
- **Task**
- **Comment**
- **Attachment**

Each model contains helper functions + business logic (e.g., progress calculation, overdue detection).

---

## 🔗 URL Routing

/login/ → Login
/register/ → Register
/projects/ → All projects
/projects/dashboard/ → Main dashboard
/projects/<id>/ → Project detail + Kanban board
/tasks/<id>/ → Task detail + comments
/admin/ → Django admin

yaml
Copy code

---

## 🛠️ Installation & Setup

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
2️⃣ Apply migrations
bash
Copy code
python manage.py migrate
3️⃣ Create Admin User
bash
Copy code
python manage.py createsuperuser
4️⃣ Start server
bash
Copy code
python manage.py runserver
Access at:
👉 http://127.0.0.1:8000/login/

📸 (Optional) Screenshots
You can upload images inside a /screenshots folder:

scss
Copy code


🎯 Future Enhancements
WebSockets (real-time task update)

Push/email notifications

Calendar view

File uploads for attachments

Export to PDF/Excel

Full REST API

Mobile App (Flutter/React Native)

🎓 Learning Outcomes
Django authentication

Custom User model

CRUD operations

Many-to-many relationships

Kanban board design

Tailwind UI

REST framework basics

🏆 Perfect For
College Projects

Resume Portfolio

Startup MVP

Freelance client work

Learning Django professionally

🙌 Contributing
Pull requests are welcome! For major changes, please open an issue first.

📄 License
This project is open-source under the MIT License.

❤️ Author
Developed by Shivam — feel free to connect!




