#!/usr/bin/env python3
"""
Django Project Setup Automation Script
Run this script in an empty folder to set up a complete Django project.
"""

import os
import sys
import subprocess
import secrets
import platform


def run_command(command, shell=True, check=True):
    """Execute a shell command."""
    print(f"\n→ Running: {command}")
    try:
        result = subprocess.run(
            command, shell=shell, check=check, text=True, capture_output=True
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(e.stderr)
        if check:
            sys.exit(1)
        return None


def generate_secret_key():
    """Generate a Django secret key."""
    return secrets.token_urlsafe(50)


def create_env_file():
    """Create .env file with SECRET_KEY."""
    secret_key = generate_secret_key()
    env_content = f"""SECRET_KEY={secret_key}
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
"""
    with open(".env", "w") as f:
        f.write(env_content)
    print("✓ Created .env file with SECRET_KEY")


def create_gitignore():
    """Create comprehensive .gitignore file."""
    gitignore_content = """# Python
# Created by https://www.toptal.com/developers/gitignore/api/django,python
# Edit at https://www.toptal.com/developers/gitignore?templates=django,python

### Django ###
*.log
*.pot
*.pyc
__pycache__/
local_settings.py
db.sqlite3
db.sqlite3-journal
media

# If your build process includes running collectstatic, then you probably don't need or want to include staticfiles/
# in your Git repository. Update and uncomment the following line accordingly.
# <django-project-name>/staticfiles/

### Django.Python Stack ###
# Byte-compiled / optimized / DLL files
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo

# Django stuff:

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/#use-with-ide
.pdm.toml

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

### Python ###
# Byte-compiled / optimized / DLL files

# C extensions

# Distribution / packaging

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.

# Installer logs

# Unit test / coverage reports

# Translations

# Django stuff:

# Flask stuff:

# Scrapy stuff:

# Sphinx documentation

# PyBuilder

# Jupyter Notebook

# IPython

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/#use-with-ide

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm

# Celery stuff

# SageMath parsed files

# Environments

# Spyder project settings

# Rope project settings

# mkdocs documentation

# mypy

# Pyre type checker

# pytype static type analyzer

# Cython debug symbols

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.

### Python Patch ###
# Poetry local configuration file - https://python-poetry.org/docs/configuration/#local-configuration
poetry.toml

# ruff
.ruff_cache/

# LSP config files
pyrightconfig.json

# End of https://www.toptal.com/developers/gitignore/api/django,python
"""
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    print("✓ Created .gitignore file")


def update_settings():
    """Update settings.py to use environment variables and add DRF/CORS config."""
    settings_path = os.path.join("core", "settings.py")

    with open(settings_path, "r") as f:
        content = f.read()

    # Add imports at the top
    imports = """import os
from dotenv import load_dotenv

load_dotenv()

"""

    # Replace SECRET_KEY
    content = content.replace(
        "SECRET_KEY = ",
        "# SECRET_KEY moved to .env\nSECRET_KEY = os.getenv('SECRET_KEY')\n# SECRET_KEY = ",
    )

    # Replace DEBUG
    content = content.replace(
        "DEBUG = True", "DEBUG = os.getenv('DEBUG', 'False') == 'True'"
    )

    # Replace ALLOWED_HOSTS
    content = content.replace(
        "ALLOWED_HOSTS = []",
        "ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')",
    )

    # Add to INSTALLED_APPS
    installed_apps_addition = """    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'user_auth_app',
]"""
    content = content.replace(
        "    'django.contrib.staticfiles',\n]",
        "    'django.contrib.staticfiles',\n" + installed_apps_addition,
    )

    # Add CORS middleware
    middleware_addition = "    'corsheaders.middleware.CorsMiddleware',\n"
    content = content.replace(
        "MIDDLEWARE = [\n    'django.middleware.security.SecurityMiddleware',",
        "MIDDLEWARE = [\n"
        + middleware_addition
        + "    'django.middleware.security.SecurityMiddleware',",
    )

    # Add CORS and REST_FRAMEWORK settings at the end
    cors_and_rest_config = """

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}
"""

    # Add imports and append config
    if "from pathlib import Path" in content:
        content = content.replace(
            "from pathlib import Path", f"from pathlib import Path\n{imports}"
        )
    else:
        content = imports + content

    content += cors_and_rest_config

    with open(settings_path, "w") as f:
        f.write(content)

    print("✓ Updated settings.py with environment variables and DRF/CORS config")


def create_auth_app_structure(python_path):
    """Create user_auth_app with API subfolder structure."""
    print("\n[7/17] Creating 'user_auth_app' app...")
    run_command(f"{python_path} manage.py startapp user_auth_app")

    # Create API subfolder structure
    print("  Creating API subfolder structure...")
    api_path = os.path.join("user_auth_app", "api")
    os.makedirs(api_path, exist_ok=True)

    # Create __init__.py to make it a package
    with open(os.path.join(api_path, "__init__.py"), "w") as f:
        f.write("")

    # Create urls.py
    with open(os.path.join(api_path, "urls.py"), "w") as f:
        f.write(
            """from django.urls import path
from . import views

urlpatterns = [
    # Add your API endpoints here
    # Example:
    # path('register/', views.register, name='register'),
    # path('login/', views.login, name='login'),
]
"""
        )

    # Create serializers.py
    with open(os.path.join(api_path, "serializers.py"), "w") as f:
        f.write(
            """from rest_framework import serializers
from django.contrib.auth.models import User


# Example User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        

# Example Registration Serializer
# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']
#     
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user
"""
        )

    # Create views.py
    with open(os.path.join(api_path, "views.py"), "w") as f:
        f.write(
            """from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer


# Example API view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    \"\"\"Get the current user's profile.\"\"\"
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# Example Registration View
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register(request):
#     serializer = RegisterSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         return Response({
#             'user': UserSerializer(user).data,
#             'message': 'User registered successfully'
#         }, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
        )

    print("  ✓ Created user_auth_app/api/ with urls.py, serializers.py, views.py")


def main():
    print("=" * 60)
    print("Django Project Setup Script")
    print("=" * 60)

    # Check if directory is empty (or only contains this script)
    files = [f for f in os.listdir(".") if f not in ["setup_django.py", "__pycache__"]]
    if files:
        response = input("⚠️  Directory is not empty. Continue anyway? (y/n): ")
        if response.lower() != "y":
            print("Aborted.")
            sys.exit(0)

    # Detect OS for activation command
    is_windows = platform.system() == "Windows"
    venv_activate = (
        r".\.venv\Scripts\Activate.ps1" if is_windows else "source .venv/bin/activate"
    )
    python_cmd = "python" if is_windows else "python3"

    # Step 1: Create virtual environment
    print("\n[1/17] Creating virtual environment...")
    run_command(f"{python_cmd} -m venv .venv")

    # Set pip path for Windows/Unix
    pip_path = os.path.join(".venv", "Scripts" if is_windows else "bin", "pip")
    python_path = os.path.join(".venv", "Scripts" if is_windows else "bin", "python")

    print(f"\n✓ Virtual environment created!")
    print(f"  To activate manually, run: {venv_activate}")

    # Step 2: Upgrade pip
    print("\n[2/17] Upgrading pip...")
    run_command(f"{python_path} -m pip install --upgrade pip")

    # Step 3: Install Django and python-dotenv
    print("\n[3/17] Installing Django and python-dotenv...")
    run_command(f"{pip_path} install django python-dotenv")

    # Step 4: Generate .env file
    print("\n[4/17] Creating .env file...")
    create_env_file()

    # Step 5: Create Django project
    print("\n[5/17] Creating Django project 'core'...")
    run_command(f"{python_path} -m django startproject core .")

    # Step 6: Update settings.py
    print("\n[6/17] Updating settings.py...")
    update_settings()

    # Step 7: Create user_auth_app with API structure
    create_auth_app_structure(python_path)

    # Step 8: Create .gitignore
    print("\n[8/17] Creating .gitignore...")
    create_gitignore()

    # Step 9: Install DRF and CORS headers
    print("\n[9/17] Installing djangorestframework and django-cors-headers...")
    run_command(f"{pip_path} install djangorestframework django-cors-headers")

    print(
        "\n[10-13/17] Settings already updated (INSTALLED_APPS, MIDDLEWARE, CORS, REST_FRAMEWORK)"
    )

    # Step 14: Make migrations
    print("\n[14/17] Making migrations...")
    run_command(f"{python_path} manage.py makemigrations")

    # Step 15: Run migrations
    print("\n[15/17] Running migrations...")
    run_command(f"{python_path} manage.py migrate")

    # Step 16: Create superuser (optional)
    print("\n[16/17] Creating superuser...")
    response = input("Do you want to create a superuser now? (y/n): ")
    if response.lower() == "y":
        run_command(f"{python_path} manage.py createsuperuser", check=False)
    else:
        print(
            "  Skipped. You can create one later with: python manage.py createsuperuser"
        )

    # Step 17: Freeze requirements
    print("\n[17/17] Creating requirements.txt...")
    run_command(f"{pip_path} freeze > requirements.txt")

    # Final instructions
    print("\n" + "=" * 60)
    print("✅ Django project setup complete!")
    print("=" * 60)
    print("\nNext steps:")
    print(f"  1. Activate virtual environment: {venv_activate}")
    print(f"  2. Run the development server: {python_cmd} manage.py runserver")
    print("  3. Visit http://127.0.0.1:8000/ in your browser")
    print("  4. Admin panel: http://127.0.0.1:8000/admin/")
    print("\nProject structure:")
    print("  📁 core/              - Main project settings")
    print("  📁 user_auth_app/          - Authentication app")
    print("    📁 api/             - API subfolder")
    print("      📄 __init__.py    - Python package file")
    print("      📄 urls.py        - API URL routes")
    print("      📄 views.py       - API view functions")
    print("      📄 serializers.py - DRF serializers")
    print("  📄 .env               - Environment variables (SECRET_KEY, DEBUG, etc.)")
    print("  📄 .gitignore         - Git ignore rules")
    print("  📄 requirements.txt   - Python dependencies")
    print("\n⚠️  Remember: CORS is configured for localhost:3000 and localhost:5173")
    print("   Update CORS_ALLOWED_ORIGINS in settings.py for production!")


if __name__ == "__main__":
    main()
