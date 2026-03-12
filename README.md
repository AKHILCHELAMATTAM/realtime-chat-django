Real-Time Individual Chat Application (Django + Channels)

A real-time one-to-one chat application built using Django (MVT Architecture) and Django Channels (WebSockets).

Users can register/login, view other users, see online status, and start private real-time chats with message history and read receipts.

Tech Stack

Python

Django (MVT Architecture)

Django Channels (WebSocket)

SQLite

HTML

CSS

JavaScript

Bootstrap 5

Features
1. Authentication

User Registration

User Login

Logout functionality

Only authenticated users can access:

User list

Chat pages

2. User List

Displays all registered users except the currently logged-in user

Shows online/offline status using a green indicator

Click on a user to start a private chat

3. Real-Time Private Chat (WebSocket)

Real-time messaging using WebSockets

Messages stored in SQLite database

Displays previous chat history

Auto-scroll to latest messages

Prevents sending empty messages

4. Read Receipts

Message indicators:

✓ → Message sent

✓✓ → Message read

Messages are marked as read when:

The receiver opens the chat

The receiver receives the message while the chat window is open

Project Architecture (MVT + Consumer)

This project strictly follows Django’s MVT architecture with an additional Consumer layer for WebSockets.

Layer	Responsibility
Model	Database schema (Custom User, ChatMessage)
View	Handles HTTP requests and sends context to templates
Template	UI rendering (no business logic)
Consumer	Handles WebSocket communication for real-time chat
Folder Structure
realtime_chat/
│
├── manage.py
│
├── realtime_chat/
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
│
├── accounts/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── signals.py
│
├── chat/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── consumers.py
│   └── routing.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── user_list.html
│   └── chat.html
│
└── static/
    └── css/
        └── app.css
Database Models
Custom User Model (accounts.User)

Fields:

email (unique)

username

password

is_online (BooleanField)

last_seen (DateTimeField)

ChatMessage Model (chat.ChatMessage)

Fields:

sender (ForeignKey → User)

receiver (ForeignKey → User)

content

created_at

is_read

read_at

Setup Instructions (Local)
1. Clone the Repository
git clone https://github.com/AKHILCHELAMATTAM/realtime-chat-django.git
cd <your-repo>
2. Create Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate
Mac / Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Run Migrations
python manage.py makemigrations
python manage.py migrate
5. Create Superuser (Optional)
python manage.py createsuperuser
6. Run the Server
python manage.py runserver

Open in browser:

Register

http://127.0.0.1:8000/register/

Login

http://127.0.0.1:8000/login/

User List

http://127.0.0.1:8000/
How to Test Real-Time Chat

Register two users

Open two browsers (or one normal + one incognito)

Login as User A in one browser

Login as User B in the other

Open chat between the two users

Send messages and verify:

Real-time delivery

✓ sent indicator

✓✓ read indicator

Chat history persists after refresh

Validation & Security

Prevents empty messages (frontend + backend validation)

Only authenticated users can access chat pages

WebSocket connections protected with AuthMiddlewareStack

Views protected with @login_required

Live Demo

Hosted URL

https://realtime-chat-django-1.onrender.com/
Test Credentials

User 1

email: akhil@gmail.com
password: Akhil123

User 2

email: manu@gmail.com
password: Manu123
GitHub Repository

Repository Link

https://github.com/AKHILCHELAMATTAM/realtime-chat-django.git
Screenshots / Demo (Optional)

Screen Recording: https://www.youtube.com/watch?v=89Fv2QPqbr8

Screenshots: Add images here

Future Enhancements

Typing indicator

Unread message counter

Delete message feature

File sharing support

Author

Name: Akhil Raj
GitHub: https://github.com/AKHILCHELAMATTAM/
Email: akhilrajchelamattam@gmail.com