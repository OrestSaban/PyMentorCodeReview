# PyMentor Review

PyMentor Review is an educational code review assistant for beginner Python programmers. It analyzes Python code and provides beginner-friendly feedback on code quality, readability, naming, complexity, and common mistakes.

## Project Structure

- `backend/`: FastAPI backend containing the AST-based code analyzer.
- `frontend/`: React + Vite frontend providing a modern code editor interface.

## Prerequisites

- Node.js
- Python 3.9+

## Setup Instructions

### Backend Setup

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run tests to ensure everything is working:
   ```bash
   pytest
   ```
5. Start the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

### Frontend Setup

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at the URL shown in the terminal (usually `http://localhost:5173`).

## Usage

1. Open the frontend in your browser.
2. Paste some Python code into the editor.
3. Click "Analyze" to see beginner-friendly feedback.
