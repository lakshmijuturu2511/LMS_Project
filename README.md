# LMS_Project
Copy this EXACTLY into your README.md file 👇

# 📚 Learning Management System (LMS)
A full-stack Learning Management System (LMS) built using FastAPI, SQLite, HTML, and CSS.
This project allows users to:
- Register & Login
- Explore Courses
- Watch Video Lessons
- Track Learning Progress
- Mark Lessons as Completed
---
# 🚀 Features
✅ User Authentication  
✅ Session Management  
✅ Course Dashboard  
✅ Video Lessons  
✅ Progress Tracking  
✅ Responsive UI  
✅ Database Integration using SQLite  
✅ Multi-User Support  
---
# 🛠️ Tech Stack
## Backend
- FastAPI
- Python
- SQLAlchemy
## Frontend
- HTML
- CSS
## Database
- SQLite
---
# 📂 Project Structure
```bash
lms_project/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── course.html
│
├── main.py
├── models.py
├── database.py
└── README.md

⸻

⚙️ Installation & Setup

1️⃣ Clone Repository

git clone https://github.com/your-username/LMS-Project.git
cd LMS-Project

⸻

2️⃣ Create Virtual Environment

Mac/Linux

python3 -m venv venv
source venv/bin/activate

Windows

python -m venv venv
venv\Scripts\activate

⸻

3️⃣ Install Dependencies

pip install fastapi uvicorn sqlalchemy jinja2 python-multipart itsdangerous

⸻

4️⃣ Run the Server

uvicorn main:app --reload

⸻

▶️ Open in Browser

http://127.0.0.1:8000

⸻

📌 Add Sample Data

Run once:

http://127.0.0.1:8000/add-sample-data

⸻

🔐 Authentication Features

* User Registration
* User Login
* Session-Based Authentication
* Logout Support

⸻

📈 Future Enhancements

🚀 Admin Panel
🚀 Quiz System
🚀 Certificate Generation
🚀 File Upload Support
🚀 Deployment Support

⸻

