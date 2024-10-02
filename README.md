# Django Chat App

## Overview

The **Django Chat App** is a real-time messaging platform that allows users to communicate seamlessly via instant messaging. Built with Django, WebSockets, and Django Channels, this app is designed for scalability, real-time performance, and ease of use. It provides a smooth and interactive chat experience, making it suitable for integration into any application requiring real-time communication features.

## Key Features

- **Real-time Messaging**: Messages are sent and received instantly using Django Channels and WebSockets.
- **User Authentication**: Secure user registration, login, and logout functionality with Django's built-in authentication system.
- **Group Chats**: Ability to create and manage group conversations.
- **Private Messaging**: Users can send direct messages to one another.
- **Message Persistence**: All chat messages are stored in a database for future retrieval.
- **Asynchronous Handling**: Real-time communication is handled asynchronously for optimal performance.
- **Responsive Design**: The frontend is mobile-friendly, ensuring a consistent experience across devices.
  
## Tech Stack

- **Backend**: Django, Django Channels, WebSockets
- **Frontend**: HTML, CSS, JavaScript (with optional frameworks like React/Vue.js for enhancement)
- **Database**: SQLite (can be configured for PostgreSQL or other databases)
- **Asynchronous Framework**: Django Channels
- **Real-Time Communication**: WebSockets

## Prerequisites

Ensure you have the following installed before proceeding:

- Python 3.8+
- Django 4.0+
- Redis (for channel layers and WebSocket management)
- A virtual environment tool (e.g., `virtualenv` or `conda`)

## Installation and Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/farad-alam/Django-Chat-App.git
    cd Django-Chat-App
    ```

2. **Set up the virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up Redis** (Required for WebSocket communication):
    - Install and run Redis. For installation steps, refer to [Redis documentation](https://redis.io/documentation).

5. **Set up the database**:
    ```bash
    python manage.py migrate
    ```

6. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

7. **Run Redis**:
    Ensure that Redis is running in the background:
    ```bash
    redis-server
    ```

8. **Access the application**:
    Open your browser and navigate to `http://127.0.0.1:8000` to start using the app.

## Usage

- **User Authentication**: Create an account or log in to an existing one.
- **Chat Functionality**: 
  - Create new chat rooms or join existing ones.
  - Send private messages to other users.
  - Participate in group conversations.
- **Real-time Updates**: Messages appear instantly in the chat without page reload.

## Project Structure

```bash
├── chat_app/                  # Main Django app for chat functionality
│   ├── consumers.py           # WebSocket consumers for handling real-time communication
│   ├── models.py              # Database models for users, messages, and chat rooms
│   ├── routing.py             # WebSocket routing
│   ├── views.py               # Views for handling HTTP requests
├── static/                    # Static files (CSS, JS)
├── templates/                 # HTML templates
├── manage.py                  # Django project management script
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
