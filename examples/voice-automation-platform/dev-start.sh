#!/bin/bash

# Voice Automation Platform - Development Server Launcher
# Starts both backend and frontend in parallel

set -e

echo "=================================="
echo "Starting Voice Automation Platform"
echo "=================================="
echo ""

# Check if setup has been run
if [ ! -d "backend/venv" ]; then
    echo "⚠ Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

if [ ! -d "frontend/node_modules" ]; then
    echo "⚠ Node modules not found. Please run ./setup.sh first."
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down servers..."
    kill $(jobs -p) 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend
echo "Starting backend server..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait a bit for backend to start
sleep 2

# Start frontend
echo "Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "=================================="
echo "✅ Servers Started!"
echo "=================================="
echo ""
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/api/docs"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID

