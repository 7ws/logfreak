# Set up the app
setup:
	pip install -r requirements.txt  # Install Python dependencies
	bower install  # Install Bower components
	./manage.py migrate  # Run database migrations

dev:
	redis-server&
	./manage.py rqworker&
	./manage.py runserver
