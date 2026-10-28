# 🛡️ WebGuard — Security Header Scanner

WebGuard is a web application built with **React** and **Flask** that scans public HTTP/HTTPS websites and checks their HTTP security response headers. It helps users identify important security headers that are present or missing in a website's response.

## ✨ Features

- **Website Scanning:** Enter a public HTTP or HTTPS URL to scan its response.
- **Security Header Analysis:** Checks five important HTTP security headers.
- **Clear Results:** Displays which headers are present and which are missing.
- **SSL Warning:** Reports SSL-related warnings when detected.
- **REST API:** Uses a Flask backend to process scan requests.
- **Interactive Interface:** Provides a React-based frontend for entering URLs and viewing results.

## 🔍 Security Headers Checked

| Header | Purpose |
|---|---|
| `Content-Security-Policy` | Helps control which resources a browser can load. |
| `Strict-Transport-Security` | Instructs browsers to use HTTPS for future connections. |
| `X-Content-Type-Options` | Helps prevent MIME-type sniffing. |
| `X-Frame-Options` | Helps protect against clickjacking. |
| `Referrer-Policy` | Controls how much referrer information is shared. |

## 🛠️ Tech Stack

**Frontend**
- React
- JavaScript
- HTML
- CSS

**Backend**
- Python
- Flask
- REST API

## 📁 Project Structure

```text
WebGuard/
├── backend/
│   ├── tests/
│   │   └── backend_test.py
│   ├── .env.example
│   ├── requirements.txt
│   └── server.py
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.css
│   │   ├── App.js
│   │   ├── index.css
│   │   └── index.js
│   ├── .env.example
│   ├── package.json
│   └── tailwind.config.js
├── .gitignore
└── README.md
```

## 🚀 Getting Started

Follow these steps to run WebGuard locally.

### Prerequisites

Install the following:
- Python
- Node.js and npm

### 1. Clone the Repository

```bash
git clone https://github.com/sudeepasurapaneni/project-4-application-security.git
cd project-4-application-security
```

### 2. Start the Backend

Open a terminal and run:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python server.py
```

The backend API runs at:

`http://localhost:5000`

### 3. Start the Frontend

Open a **second terminal** from the project directory and run:

```bash
cd frontend
cp .env.example .env
npm install
npm start
```

Open the following address in your browser:

`http://localhost:3000`

### 4. Scan a Website

1. Open WebGuard in your browser.
2. Enter a publicly accessible HTTP or HTTPS website URL.
3. Click **Scan website**.
4. Review the security headers reported as present or missing.

## 🔌 API Endpoint

**Endpoint:** `POST /api/scan`

**Request body:**

```json
{
  "url": "https://example.com"
}
```

The API returns scan information, including the HTTP response status, response headers, security-header checks, and any SSL warning.

## ⚠️ Limitations

- Results depend on the response received from the target website.
- Some websites may block requests or fail to respond.
- A missing security header does not automatically mean a website is vulnerable; security depends on multiple factors.
- WebGuard checks selected response headers and is not a complete security audit.

## 🎯 Project Objective

The objective of WebGuard is to make basic website security-header inspection easier through a simple interface backed by a Python API.

## 👩‍💻 Author

**Sudeepa**

GitHub: [@sudeepasurapaneni](https://github.com/sudeepasurapaneni)
