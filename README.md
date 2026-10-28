# WebGuard

WebGuard is a Flask + React application that requests a public HTTP/HTTPS website and checks five security response headers.

## Run locally

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python server.py
```
API: `http://localhost:5000`.

### Frontend
In a second terminal:
```bash
cd frontend
cp .env.example .env
npm install
npm start
```
Open `http://localhost:3000`.

Enter a public `http://` or `https://` URL and click **Scan website**. Results are based on the website's response headers.

## API
`POST /api/scan` with JSON body `{"url":"https://example.com"}` returns the response status, headers, five security-header checks, and any SSL warning.
