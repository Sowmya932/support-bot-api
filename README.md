Support Bot API

The Support Bot API is an intelligent customer support chatbot built using FastAPI and Sentence Transformers.
It identifies user intents and returns the most relevant support responses by comparing text embeddings.
The project is fully containerized with Docker, making it easy to deploy anywhere.

🚀 Features

🧩 Intent Detection — Uses semantic similarity to understand user messages

💬 Response Generation — Matches the user’s intent with pre-trained responses

⚡ FastAPI Backend — Lightweight, fast, and easy to extend

🐳 Dockerized — Simple build and deployment using Docker

📁 Custom Training — train.py can retrain embeddings with new data

🏗️ Project Structure
support-bot/
├── services/
│   └── api/
│       └── app/
│           ├── main.py              # FastAPI entry point
│           ├── train.py             # Training script to create embeddings
│           ├── model_store.py       # Model loading and similarity logic
│           ├── intents.csv          # Sample dataset of user intents
│           ├── requirements.txt     # Python dependencies
│           ├── Dockerfile           # Docker image build instructions
│           ├── .dockerignore        # Files to exclude from Docker build
│           └── ...
└── README.md

⚙️ Tech Stack
Component	Description
Language	Python 3.10
Framework	FastAPI
Model	Sentence Transformers (all-MiniLM-L6-v2)
Vector Similarity	Cosine similarity on embeddings
Containerization	Docker
Data	CSV file with intents and sample responses
🧠 How It Works

Training (train.py)

Loads a CSV of intents and sample user phrases.

Uses Sentence Transformers to encode them into embeddings.

Saves embeddings and metadata for inference.

API (main.py)

Starts a FastAPI server.

Loads the trained model and embeddings.

When you send a message, it finds the most similar intent.

Returns a matching support response.

🧪 Example API Usage

POST /predict

Request:

{
  "text": "I want to cancel my order"
}


Response:

{
  "intent": "cancel_order",
  "response": "Please share your order id and we'll attempt cancellation if it hasn't shipped.",
  "matched_example": "want cancel order",
  "distance": 1.44
}

🐳 Run with Docker
1️⃣ Build the Docker image
docker build -t support-bot-api .

2️⃣ Run the container
docker run -d -p 8000:8000 support-bot-api

3️⃣ Access the API

Visit: http://localhost:8000/docs

You can interact with the API directly in the interactive Swagger UI.

💻 Run Locally (Without Docker)
1️⃣ Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate       # On Linux/Mac
.venv\Scripts\activate          # On Windows

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Train embeddings (if needed)
python train.py

4️⃣ Run the API
uvicorn main:app --reload


Access it at http://localhost:8000
.

📦 API Endpoints
Method	Endpoint	Description
POST	/predict	Predicts intent and returns a support response
GET	/	Root health check route
GET	/docs	Interactive Swagger documentation
🧰 Future Improvements

Integrate a real support database or CRM

Add user context tracking

Connect with a frontend chatbot UI

Implement multilingual intent recognition

Add authentication for production deployment

🧑‍💻 Author

Support Bot by [Your Name]
Built with ❤️ using FastAPI and Sentence Transformers.

