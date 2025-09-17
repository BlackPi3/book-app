#!/bin/bash

# BookApp Startup Script

BACKEND_PORT=${BACKEND_PORT:-8000}
FRONTEND_PORT=${FRONTEND_PORT:-8080}

set -u

echo "🚀 Starting BookApp Development Servers..."

if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
  echo "Script must be run from project root (where backend/ and frontend/ exist)." >&2
  exit 1
fi

# --- Backend ---
echo "📊 Starting Backend Server on port ${BACKEND_PORT}..."
cd backend || exit 1
if [ ! -d "venv" ]; then
  echo "Python venv missing; create it first (python -m venv venv && source venv/bin/activate && pip install -r requirements.txt)" >&2
  exit 1
fi
source venv/bin/activate
uvicorn app.main:app --reload --port ${BACKEND_PORT} &
BACK_PID=$!
cd ..

# Wait briefly so backend is up
sleep 2

# --- Frontend ---
echo "🖥️  Starting Frontend UI5 Server on port ${FRONTEND_PORT}..."
cd frontend || exit 1
# Ensure dependencies installed
if [ ! -d node_modules ]; then
  echo "Installing frontend dependencies..."
  npm install --no-fund --no-audit
fi
# Prefer local binary via npm script (resolves to @ui5/cli)
PORT=${FRONTEND_PORT} npm run start -- --port ${FRONTEND_PORT} &
FRONT_PID=$!
cd ..

echo "✅ Both servers started"
echo "📊 Backend:  http://localhost:${BACKEND_PORT}"
echo "🖥️  Frontend: http://localhost:${FRONTEND_PORT}"

echo "Press Ctrl+C to stop both."

trap 'echo; echo "⏹ Stopping..."; kill ${BACK_PID} ${FRONT_PID} 2>/dev/null; exit 0' INT TERM
wait
