# #!/bin/bash
# set -e

# # Check Python version
# python3 --version

# # Check pip version
# python3 -m pip --version || echo "pip not found"

# # Install pip if necessary
# if ! python3 -m pip --version &> /dev/null; then
#     echo "Pip is not installed. Installing pip."
#     curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
#     python3 get-pip.py
# fi

# # Check if pip is installed correctly
# python3 -m pip --version

# # Create and activate virtual environment
# if [ ! -d "venv" ]; then
#     python3 -m venv venv
# fi

# source venv/bin/activate

# # Upgrade pip in the virtual environment
# pip install --upgrade pip

# # Install dependencies
# pip install -r requirements.txt

# Run additional build commands
# e.g., python manage.py migrate
# e.g., python manage.py collectstatic --noinput


# echo "Make Migration..."
# python3.9 manage.py makemigrations --noinput
# python3.9 manage.py migrate --noinput

# echo "Collect Static..."
# python3.9 manage.py collectstatic --noinput --clear



#!/bin/bash
set -e

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Exiting."
    exit 1
fi

# Check if pip is installed
if ! python3 -m pip --version &> /dev/null; then
    echo "Pip is not installed. Installing pip."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
fi

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip in the virtual environment
pip install --upgrade pip

pip install -r requirements.txt
python manage.py collectstatic --noinput 


# List contents of the directory for debugging
echo "Contents of staticfiles directory:"
ls -l staticfiles

# Check if the staticfiles_build directory exists and contains files
if [ -d "staticfiles" ]; then
    echo "Static files collected successfully."
else
    echo "Static files were not collected properly."
    exit 1
fi


