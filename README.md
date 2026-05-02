# 🚀 AI QA Agent

An AI-powered Quality Assurance automation platform that performs **exploratory testing** and **goal-based testing** on web applications using browser automation and Large Language Models.

---

## 🔥 Demo

> ⚡ Enter any website URL → AI tests it automatically
> 🎯 Supports goal-based testing (Login, Search, Explore)

---

## 🧠 Key Features

### 🤖 AI-Powered Testing

* Uses **Gemini LLM** to decide actions dynamically
* Analyzes **screenshots + DOM structure**
* Mimics real user behavior

### 🎯 Goal-Based Testing

* Login flow testing
* Search functionality testing
* Exploratory testing

### ⚙️ Automated Browser Interaction

* Powered by **Playwright**
* Clicks buttons, fills inputs, scrolls pages
* Smart element detection

### 📊 QA Report Generation

* Page load validation
* UI element checks (buttons, inputs, links)
* Score-based evaluation

### 🧪 Test Case Generation

* Functional test cases
* Edge cases
* Negative test scenarios

### 🧠 AI Explanation

* Explains issues clearly
* Highlights impact (UX, performance, SEO)

### 🎨 Modern Dashboard UI

* Built with React + Tailwind CSS
* Visual score chart
* Step-by-step agent actions
* Screenshot preview

---

## 🏗️ Tech Stack

### Backend

* **FastAPI**
* **Playwright**
* **Google Gemini API**
* Python

### Frontend

* **React.js**
* **Tailwind CSS**
* **Recharts**

---

## 📁 Project Structure

SQA/
├── backend/
│   ├── main.py
│   ├── browser.py
│   ├── agent.py
│   ├── static/
│   └── .env
│
├── qa-ui/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── requirements.txt
├── start.sh
└── README.md

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repo

git clone https://github.com/Dosscyril/Quality_assurance_AI_agent.git
cd Quality_assurance_AI_agent

---

### 2️⃣ Backend Setup

pip install -r requirements.txt
playwright install

Create `.env` file inside `backend/`:

GOOGLE_API_KEY=your_api_key_here

Run backend:
uvicorn backend.main:app --reload

---

### 3️⃣ Frontend Setup

cd qa-ui
npm install
npm start

---

## 🚀 Usage

1. Open frontend → http://localhost:3000
2. Enter any website URL
3. Select goal:

   * Explore
   * Login
   * Search
4. Click **Run Test**

---

## 🧠 How It Works

User Input
↓
Frontend (React)
↓
FastAPI Backend
↓
Playwright opens browser
↓
Gemini AI analyzes page
↓
AI decides next action
↓
Actions executed (click/fill/scroll)
↓
Validation + QA checks
↓
Report + Testcases generated
↓
Displayed in UI

---

## 🌍 Deployment

* Backend → Render
* Frontend → Vercel

---

## 💡 Future Improvements

* Multi-step workflows (signup, checkout)
* Authentication handling
* Parallel testing
* Performance metrics integration
* CI/CD integration

---

## 🎯 Resume Highlight

Built an AI-powered QA automation platform using FastAPI, Playwright, and LLMs that performs exploratory and goal-based testing on web applications with automated reporting and test case generation.

---

## 👨‍💻 Author

Dosscyril

---

## ⭐ If you like this project, give it a star!
