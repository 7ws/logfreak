# Set up the app
setup:
	pip install -r requirements.txt  # Install Python dependencies
	./manage.py migrate  # Run database migrations
