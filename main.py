from fastapi import FastAPI, Form, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

import models
from database import engine, SessionLocal

app = FastAPI()

# Session
app.add_middleware(SessionMiddleware, secret_key="secret123")

# Create tables
models.Base.metadata.create_all(bind=engine)

# Static + Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ---------------- DATABASE ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- HOME ----------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>LMS Project</h1>
    <a href='/register'>Register</a><br>
    <a href='/login'>Login</a>
    """


# ---------------- REGISTER ----------------
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
def register(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.username == username).first()

    if existing_user:
        return {"message": "Username already exists ❌"}

    user = models.User(username=username, password=password)
    db.add(user)
    db.commit()

    return RedirectResponse(url="/login", status_code=303)

# ---------------- LOGIN ----------------
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.username == username,
        models.User.password == password
    ).first()

    if user:
        request.session["user"] = user.username
        request.session["user_id"] = user.id   # 🔥 important
        return RedirectResponse(url="/dashboard", status_code=303)

    return {"message": "Invalid Credentials ❌"}


# ---------------- LOGOUT ----------------
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/")


# ---------------- DASHBOARD ----------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):

    if "user" not in request.session:
        return RedirectResponse(url="/login")

    courses = db.query(models.Course).all()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "courses": courses,
        "user": request.session["user"]
    })


# ---------------- COURSE PAGE ----------------
@app.get("/course/{course_id}", response_class=HTMLResponse)
def course_page(request: Request, course_id: int, db: Session = Depends(get_db)):

    if "user_id" not in request.session:
        return RedirectResponse(url="/login")

    user_id = request.session.get("user_id")

    lessons = db.query(models.Lesson).filter(models.Lesson.course_id == course_id).all()

    completed = db.query(models.Progress).filter_by(user_id=user_id).all()
    completed_ids = [p.lesson_id for p in completed]

    total = len(lessons)
    done = sum(1 for l in lessons if l.id in completed_ids)

    progress_percent = int((done / total) * 100) if total > 0 else 0

    return templates.TemplateResponse("course.html", {
        "request": request,
        "lessons": lessons,
        "progress": progress_percent
    })


# ---------------- COMPLETE LESSON ----------------
@app.get("/complete/{lesson_id}/{course_id}")
def complete(request: Request, lesson_id: int, course_id: int, db: Session = Depends(get_db)):

    user_id = request.session.get("user_id")

    existing = db.query(models.Progress).filter_by(
        user_id=user_id,
        lesson_id=lesson_id
    ).first()

    if not existing:
        db.add(models.Progress(user_id=user_id, lesson_id=lesson_id))
        db.commit()

    return RedirectResponse(url=f"/course/{course_id}", status_code=303)


# ---------------- ADD SAMPLE DATA ----------------
@app.get("/add-sample-data")
def add_data(db: Session = Depends(get_db)):

    # Check if already exists
    existing = db.query(models.Course).first()
    if existing:
        return {"message": "Data already exists ⚠️"}

    python_course = models.Course(title="Python Full Course")
    web_course = models.Course(title="Web Development")
    db_course = models.Course(title="Database Management")
    ai_course = models.Course(title="Artificial Intelligence")

    db.add_all([python_course, web_course, db_course, ai_course])
    db.commit()

    db.add_all([
        models.Lesson(title="Intro", content="https://www.youtube.com/embed/kqtD5dpn9C8", course_id=python_course.id),
        models.Lesson(title="HTML Basics", content="https://www.youtube.com/embed/UB1O30fR-EE", course_id=web_course.id),
        models.Lesson(title="DBMS Intro", content="https://www.youtube.com/embed/ztHopE5Wnpc", course_id=db_course.id),
        models.Lesson(title="AI Intro", content="https://www.youtube.com/embed/2ePf9rue1Ao", course_id=ai_course.id),
    ])

    db.commit()

    return {"message": "Data added only once ✅"}