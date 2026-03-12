Realtime Individual Chat Application (Django + Channels)
A real-time one-to-one chat application built using Django (MVT) and Django Channels (WebSockets).
Users can register/login, view other users, see online status, and start private real-time chats with message history and read receipts.

Tech Stack
Python
Django (MVT Architecture)
Django Channels (WebSocket)
SQLite
HTML, CSS, JavaScript
Bootstrap 5
Features
Authentication
Register
Login
Logout
Only authenticated users can access:
User list
Chat pages
User List
Shows all users except the currently logged-in user
Displays online/offline indicator (green dot)
Click user to start a private chat
Real-Time Private Chat (WebSocket)
WebSocket communication between two users
Messages stored in database (SQLite)
Previous chat history displayed
Auto-scroll to latest message
Prevents empty messages
Read Receipts
✓ = message sent
✓✓ = message read (marked when receiver opens the chat / receives message while chat is open)
Project Architecture (Strict MVT + Consumer)
Model: Database schema (Custom User, ChatMessage)
View: HTTP request handling & context passing
Template: UI rendering (no business logic inside templates)
Consumer: WebSocket handling for real-time messaging
Folder Structure (High Level)
text

realtime_chat/
  manage.py
  realtime_chat/
    settings.py
    urls.py
    asgi.py
  accounts/
    models.py
    forms.py
    views.py
    urls.py
    signals.py
  chat/
    models.py
    views.py
    urls.py
    consumers.py
    routing.py
  templates/
    base.html
    login.html
    register.html
    user_list.html
    chat.html
  static/
    css/app.css
Database Models
Custom User Model (accounts.User)
Fields:

email (unique)
username
password
is_online (BooleanField)
last_seen (DateTimeField)
ChatMessage Model (chat.ChatMessage)
sender (FK to User)
receiver (FK to User)
content
created_at
is_read
read_at
Setup Instructions (Local)
1) Clone the repo
Bash

git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
2) Create and activate virtual environment
Windows

Bash

python -m venv venv
venv\Scripts\activate
Mac/Linux

Bash

python3 -m venv venv
source venv/bin/activate
3) Install dependencies
Bash

pip install -r requirements.txt
4) Run migrations
Bash

python manage.py makemigrations
python manage.py migrate
5) Create superuser (optional)
Bash

python manage.py createsuperuser
6) Run the server
Bash

python manage.py runserver
Open:

Register: http://127.0.0.1:8000/register/
Login: http://127.0.0.1:8000/login/
Users list: http://127.0.0.1:8000/
How to Test Real-Time Chat Locally
Create two users (via register page).
Open two browsers or normal + incognito.
Login as User A in one, User B in the other.
From user list, open chat with each other.
Send messages and verify:
Real-time delivery
✓ sent, ✓✓ read
History persists after refresh
Validation & Security
Empty messages blocked (frontend + backend)
Only authenticated users can connect to WebSocket
Auth-protected pages using @login_required
WebSocket protected using AuthMiddlewareStack
Live Demo
Hosted URL: <add-your-live-url-here>
Test Credentials
User 1: <email> / <password>
User 2: <email> / <password>
GitHub Repository
Repo Link: https://github.com/<your-username>/<your-repo>
Screenshots / Recording (Optional)
Screen recording: <youtube-link-if-any>
Future Enhancements (Bonus Ideas)
Typing indicator
Unread message count
Delete message feature
File sharing
Author
Name: <your-name>
GitHub: https://github.com/<your-username>
Email: <your-email>
