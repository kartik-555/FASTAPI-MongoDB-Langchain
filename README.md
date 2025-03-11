
# FastAPI WebSocket and Authentication Example

This project demonstrates a FastAPI application with WebSocket support and JWT-based authentication. The application includes endpoints for user signup and login, as well as a WebSocket endpoint for real-time communication.

---

## 🚀 Features

- ✅ User signup and login with JWT-based authentication  
- 📡 WebSocket endpoint for real-time communication  
- 🔐 Pydantic models for request validation  
- 💾 MongoDB for data storage using Motor (async driver)  
- 🐳 Docker support for containerized deployment  

---

## 📦 Setup

### ✅ Prerequisites

- Python 3.12  
- Docker  
- MongoDB Atlas or Local MongoDB instance  

---

### 🛠️ Installation

1. **Clone the repository**  
   ```sh
   git clone https://github.com/kartik-555/FASTAPI-MongoDB-Langchain.git
   cd FASTAPI-MongoDB-Langchain
   ```

2. **Create and activate a virtual environment**  
   ```sh
   python3 -m venv env
   source env/bin/activate  # On Windows use: .\env\Scripts\activate
   ```

3. **Install the dependencies**  
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables**  
   - Create a `.env` file in the root directory  
   - Copy content from `env_example.txt` and fill in your values  
     ```env
     MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
     SECRET_KEY=your-secret-key
     ```

---

## 🚀 Running the Application

### ▶️ Start FastAPI Server (Dev)

```sh
uvicorn app.main:app --reload
```

The server will be available at: [http://localhost:8000](http://localhost:8000)

---

### 🐳 Run with Docker

1. **Build the Docker image**  
   ```sh
   docker build -t fastapi-app .
   ```

2. **Run the Docker container**  
   ```sh
   docker run -d -p 8000:8000 fastapi-app
   ```

---

## 📬 API Endpoints

- `POST /signup` – Register a new user  
- `POST /login` – Login and receive JWT token  
- `ws://localhost:8000/ws/${topic}?token=${token}` – WebSocket connection (authenticated)

---

## 🧠 Tech Stack

- **FastAPI** – Web framework  
- **Motor** – Async MongoDB driver  
- **PyJWT** – JWT handling  
- **Pydantic** – Data validation  
- **Docker** – Containerization  

---
