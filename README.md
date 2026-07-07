# 🌌 Orbit CRM

[![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46C3C6?style=for-the-badge&logo=render)](https://render.com)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-000000?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-47A248?style=for-the-badge&logo=mongodb)](https://mongodb.com)

> A modern, glass-themed Customer Relationship Management (CRM) system with an intuitive bento grid layout and real-time pipeline management.


## ✨ Features

### 🎨 Design
- **Liquid Glass UI** - Modern glassmorphism design with animated aurora background
- **Bento Grid Layout** - Clean, organized dashboard with responsive cards
- **Dark Theme** - Eye-friendly dark mode with subtle gradients
- **Responsive** - Optimized for desktop, tablet, and mobile devices

### 📊 Core CRM Features
- **Dashboard** - Real-time statistics, pipeline charts, and lead status overview
- **Customer Management** - Full CRUD operations with tags and contact info
- **Lead Tracking** - Status-based filtering (New, Contacted, Qualified, Lost)
- **Pipeline/Kanban Board** - Drag-and-drop deal management across stages
- **Task Management** - Create, complete, and track tasks with due dates
- **Calendar** - Monthly view with events and meetings
- **Reports** - Pipeline analytics and key performance metrics

### ⚡ Technical Features
- **Zero Setup** - Runs with in-memory demo data (no database required)
- **MongoDB Support** - Seamless MongoDB Atlas integration
- **RESTful API** - Full CRUD endpoints for all resources
- **Real-time Updates** - Dynamic data updates without page refresh
- **Glass Effects** - CSS backdrop-filter for beautiful glass effects
- **Animations** - Smooth animations and transitions

---

# 🚀 Quick Start

## Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- (Optional) MongoDB Atlas account for persistent storage

## Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/orbit-crm.git
cd orbit-crm
```

### 2. Create and activate virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file:

```env
# Demo Mode
MONGO_URI=
PORT=5000

# Production (Optional)
# MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/crm_db
```

### 5. Run the application

```bash
python app.py
```

### 6. Open your browser

```
http://localhost:5000
```

The application starts with seeded demo data and is ready to use immediately.

---

# 🗄️ Database Options

## Option 1 — In-Memory Demo

✅ No setup required

✅ Preloaded demo data

✅ Perfect for testing

⚠ Data resets after restarting the server

---

## Option 2 — MongoDB Atlas

1. Create a MongoDB Atlas account
2. Create a cluster
3. Copy your connection string
4. Add it to `.env`

```env
MONGO_URI=your_connection_string
```

5. Restart the application

---

# 📁 Project Structure

```text
orbit-crm/
├── app.py
├── requirements.txt
├── render.yaml
├── .env
├── templates/
│   └── index.html
└── README.md
```

---

# 🚢 Deployment

## Deploy on Render

Push your repository:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/orbit-crm.git
git push -u origin main
```

Render Settings

| Setting | Value |
|---------|------|
| Environment | Python |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app --bind 0.0.0.0:$PORT` |
| Plan | Free |

Environment Variables

```
MONGO_URI=<optional>
PYTHON_VERSION=3.11.9
```

---

# 📊 API Endpoints

| Endpoint | Methods | Description |
|-----------|---------|-------------|
| `/api/customers` | GET POST | Customers |
| `/api/customers/<id>` | PUT DELETE | Customer |
| `/api/leads` | GET POST | Leads |
| `/api/leads/<id>` | PUT DELETE | Lead |
| `/api/deals` | GET POST | Deals |
| `/api/deals/<id>` | PUT DELETE | Deal |
| `/api/tasks` | GET POST | Tasks |
| `/api/tasks/<id>` | PUT DELETE | Task |
| `/api/events` | GET POST | Events |
| `/api/events/<id>` | DELETE | Delete Event |
| `/api/reports/summary` | GET | Dashboard Summary |

---

# 🎯 Features Overview

## Dashboard

- Statistics Cards
- Pipeline Overview
- Lead Distribution
- Recent Activity

## Pipeline

- Drag & Drop Kanban Board
- Deal Stages
- Deal Value Tracking

## Tasks

- Task Completion
- Due Dates
- Overdue Highlighting

## Calendar

- Monthly View
- Meetings
- Calls
- Demos

---

# 🛠 Built With

- Flask
- Python
- MongoDB
- Vanilla JavaScript
- HTML5
- CSS3
- Glassmorphism UI

---

# 🔧 Environment Variables

| Variable | Description |
|----------|-------------|
| MONGO_URI | MongoDB Connection |
| PORT | Server Port |
| PYTHON_VERSION | Python Version |

---

# 📱 Responsive Design

- Desktop Layout
- Tablet Layout
- Mobile Layout
- Bottom Navigation
- Floating Action Button

---

# 🤝 Contributing

1. Fork the project

2. Create your feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit

```bash
git commit -m "Added new feature"
```

4. Push

```bash
git push origin feature/new-feature
```

5. Open a Pull Request

---

# 🐛 Known Issues

- Demo mode resets after restart
- Calendar requires refresh after adding events
- Drag-and-drop isn't persisted in demo mode

---

# 🙏 Acknowledgements

- Render
- MongoDB Atlas
- Flask
- Google Fonts

---

# 📞 Support

For support:

Create an issue in the GitHub repository.

---

# ⚡ Useful Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run
python app.py

# Freeze packages
pip freeze > requirements.txt

# Tests
pytest
```

---

# 🎨 Color Palette

| Name | Hex |
|------|-----|
| Aurora Violet | `#7c6ff0` |
| Aurora Teal | `#35d0ba` |
| Aurora Coral | `#ff6f91` |
| Aurora Amber | `#ffb545` |
| Background | `#080b14` |
| Glass | `rgba(255,255,255,.055)` |

---

# ❤️ Author

Made with ❤️ by **Yathavan Loganathan**

If you like this project, consider giving it a ⭐ on GitHub.
````
