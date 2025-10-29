TECHSTACK

1. FastAPI

Why FastAPI?

It’s fast and simple to set up — perfect for quickly spinning up a backend.
It offers built-in async support which mkaes it ideal for our use case here.
I’ve been wanting to try FastAPI for a while, and this project was a great opportunity to get hands-on experience with it in a practical use case.

2. PostgresDB with Supabase

Why this DB stack choice?

I went with PostgreSQL because I’m comfortable working with it and have prior experience designing and querying relational databases.
I chose Supabase since it provides a quick and reliable way to spin up a managed PostgreSQL instance in the cloud.

SETTING UP IN LOCAL MACHINE

1️⃣ Clone the Repository

git clone https://github.com/avishekpadhi/fastapi-webhook-service.git
cd fastapi-webhook-service

2️⃣ Create and Activate Virtual Environment
python3 -m venv venv
source venv/bin/activate #for macOS/Linux

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Environment Variables
#Create a .env file in the project root
touch .env

Add the Postgres DB connection string in the .env file:
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<dbname>

6️⃣ Run the Server
fastapi dev app/main.py

TESTING IN LOCAL

1️⃣ After starting the server, in the terminal:

curl http://127.0.0.1:8000/

✅ Expected response:

{
"status": "HEALTHY",
"current_time": "2025-10-29T12:10:00.123Z"
}

curl -X POST http://127.0.0.1:8000/v1/webhooks/transactions \
 -H "Content-Type: application/json" \
 -d '{
"transaction_id": "txn_abc123def456",
"source_account": "acc_user_789",
"destination_account": "acc_store_123",
"amount": 1000.50,
"currency": "INR"
}'

✅ Expected response (within 500ms):

{
"message": "Webhook received"
}

curl http://127.0.0.1:8000/v1/transactions/txn_abc123def456

✅ Expected response
If you query before 30s ⏱️ → you’ll get:

{
"transaction_id": "txn_abc123def456",
"status": "processing",
...
}

✅ Expected response
If you query after 30s →

{
"transaction_id": "txn_abc123def456",
"status": "processed",
"processed_at": "2025-10-29T12:15:00.000Z"
...
}
