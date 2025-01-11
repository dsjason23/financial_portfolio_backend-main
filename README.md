# Install requirements
pip install -r requirements.txt


# Run the app

# Or with specific host and port
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


# test

http://localhost:8000/api/v1/portfolio/
http://localhost:8000/api/v1/sentiment/
http://localhost:8000/api/v1/users/