# Coderr Backend (13_Coderr)

This is the backend for the **Coderr** platform, built with **Django** and **Django REST Framework**. It serves as the API for a marketplace connecting clients and developers.

## 🚀 Installation & Setup

Follow these steps to set up the project on your local machine.

### 1. Clone the Repository
Download the project to your local directory:
```bash
git clone [https://github.com/TobiasDreifke/13_Coderr.git](https://github.com/TobiasDreifke/13_Coderr.git)
cd 13_Coderr
```
2. Create a Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies:
```bash
# Create environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

2. Create a Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies:

```bash
# Create environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

3. Install Dependencies
Ensure pip is up to date and install the required packages:

```bash
pip install -r requirements.txt
```
⚙️ Configuration (CRITICAL)
To ensure the application runs securely and correctly, you must configure your environment variables. Never share your production SECRET_KEY publicly.

Environment Variables (.env)
```bash

Create a file named .env in the root directory (the same folder as manage.py) and add the following:
```
```bash

Code-Snippet
# A long, unique, secret key for your installation
SECRET_KEY=your-very-secret-key-goes-here

# Set to True for development, False for production
DEBUG=True

# Comma-separated list of hosts (local dev: localhost, 127.0.0.1)
ALLOWED_HOSTS=localhost,127.0.0.1

[!IMPORTANT]
Security Note: If DEBUG is set to True, Django will display detailed error pages. This is helpful for development, but extremely dangerous in production as it leaks system information.
```
🗄️ Database Setup
Once the configuration is set, prepare and initialize the database:

Run Migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

The migration step also seeds the demo guest accounts used by the frontend login:

```text
customer: andrey / asdasd
business: kevin / asdasd24
```

Create Admin User (Optional):
Access the Django admin interface at /admin by creating a superuser:
```bash
python manage.py createsuperuser
```

## Running Tests

Run the full backend test suite:

```bash
python manage.py test
```

If `python` is not available in your Windows shell, use:

```bash
py manage.py test
```

Run tests for a single app:

```bash
python manage.py test orders_app
python manage.py test offers_app
python manage.py test reviews_app
python manage.py test profiles_app
python manage.py test user_auth_app
python manage.py test base_stats_app
```

## Production Gunicorn Service

For the Hetzner deployment used in this project, a ready-to-copy `systemd` unit is provided at:

```bash
deploy/systemd/coderr-gunicorn.service
```

Install and enable it on the server:

```bash
sudo cp deploy/systemd/coderr-gunicorn.service /etc/systemd/system/coderr-gunicorn.service
sudo systemctl daemon-reload
sudo systemctl enable --now coderr-gunicorn
sudo systemctl status coderr-gunicorn --no-pager
```

If an old manually started Gunicorn process is still running, stop it first:

```bash
sudo pkill -f "gunicorn core.wsgi:application"
```

🏃‍♂️ Running the Server
Start the local development server:
```bash
python manage.py runserver
```
```bash
The application will be accessible at http://127.0.0.1:8000/.
```
🛠 Tech Stack
```bash

Framework: Django & Django REST Framework (DRF)

Database: SQLite (default for local dev)

Authentication: Token-based authentication
```

📁 Project Overview
```bash

coderr_projects/: Handles core logic for projects and offers.

coderr_auth/: User management, profiles, and authentication logic.

coderr/: Main project settings (settings.py, urls.py).
```

