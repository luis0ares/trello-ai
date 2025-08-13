# Task-Board

![License](https://img.shields.io/badge/license-MIT-blue)
![Made With](https://img.shields.io/badge/made%20with-AI-blueviolet)

A modern **task management application** inspired by **Trello**, enhanced with **AI** for smart task planning and **secure authentication** using your Discord account.  
This project is structured as a **monorepo**, containing both **backend** and **frontend** applications.

> _Note: This is a side project developed for learning and experimentation purposes._

---

## 🚀 Features

- ✅ **Trello-like board** for organizing tasks
- ✅ **AI-powered assistant** for intelligent task creation
- ✅ **Authentication & Authorization** (Login/Register)
- ✅ **Responsive UI** optimized for desktop and mobile

---

## 🛠 Tech Stack

- **Frontend:** Next.js 15, TypeScript, Tailwind CSS
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL (SQLAlchemy)
- **AI Integration:** OpenAI API
- **Authentication:** Discord OAuth2

---

## 🤖 AI Integration

The AI assistant helps users by:

- Generating **task suggestions** based on natural language input
- **Organizing tasks** into boards automatically
- Providing **priority recommendations** for better workflow

Example:

> **User:** "Plan a marketing campaign for next month"  
> **AI:** Creates tasks like "Define target audience", "Create ad content", "Schedule social posts"

---

## ✅ Project Roadmap

### **Milestones**

- **MVP**: Basic board UI + manual task creation + authentication
- **Beta**: AI task planning + drag-and-drop functionality
- **v1.0**: Public release + optimized performance + testing

---

## ✅ To-Do List

### **Frontend**

- [x] Project setup with Next.js 15 + Tailwind CSS
- [x] Basic UI for boards and tasks
- [ ] Implement **task creation**
- [ ] Implement **drag-and-drop** for task cards
- [ ] Implement **task editing** and **deletion**
- [ ] Implement **authentication** using Discord OAuth2
- [ ] Integrate with backend API for data persistence
- [ ] Improve **UI design** for better support on mobile devices
- [ ] Implement **AI assistant chat** component
- [ ] Integrate with OpenAI API for task planning

### **Backend**

- [x] Project setup (FastAPI)
- [x] Database schema for boards and tasks
- [x] API endpoints for boards
- [ ] API endpoints for tasks
- [ ] Database schema for users
- [ ] Implement **Discord OAuth2**
- [ ] OpenAI API integration endpoint for task planning
- [ ] Unit and integration tests

---

## ▶️ Getting Started

### **Clone the repository**

```bash
git clone https://github.com/your-username/task-board.git
cd task-board
```

### **Install dependencies and run applications**

For **frontend**:

```bash
cd frontend
npm install
npm run dev
```

For **backend**:

First, install [Poetry](https://python-poetry.org/docs/#installation), then install the project dependencies:

```bash
cd backend
poetry install
poetry run task run
```

---

## 📜 Changelog

### **v0.1.0 - Initial Setup**

- ✅ Created monorepo structure
- ✅ Initialized frontend with Next.js and Tailwind CSS
- ✅ Initialized backend with FastAPI
- ✅ Created basic project structure
- ✅ Set up basic backend project configuration and dependencies
- ✅ Infrastructure layer for boards and tasks created
- ✅ Alembic setup with first migration
- ✅ API endpoints for boards
- ✅ Basic frontend UI and CI/CD setup