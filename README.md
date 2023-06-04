Kitchen Service Plan - Manzilik Task


Project Description
The Kitchen Service Plan project aims to manage the weekly service plan for kitchen employees. It allows you to create employees, assign service days, and generate a weekly plan. You can also check the vacation days for each employee and exclude them from the weekly plan if they have a vacation.

Project Setup
Follow the steps below to set up and run the project locally:

Create a virtual environment:
python -m venv env
Activate the virtual environment:
env\Scripts\activate
Install Django:
pip install django
Install project requirements:
pip install -r requirements.txt
Apply database migrations:
python manage.py makemigrations
python manage.py migrate
Run the development server:
python manage.py runserver

API Endpoints
The following API endpoints are available in the Kitchen Service Plan project:
Get List of Employees:

Method: GET
URL: http://127.0.0.1:8000/kitchen/employee/
Description: Retrieve the list of employees in the system.
Create Employee:

Method: POST
URL: http://127.0.0.1:8000/kitchen/employee/
Description: Create a new employee. Provide the necessary details in the request body.
Get Weekly Plan for Date:

Method: GET
URL: http://127.0.0.1:8000/kitchen/weekly-plan/working_days/?date=<date>
Description: Retrieve the weekly plan for a specific date. Replace <date> with the desired date in the format "YYYY-MM-DD". The response will include the employee's name, service date, and day of the week.

Get Vacation Days for Employees:

Method: GET
URL: http://127.0.0.1:8000/kitchen/vacations/
Description: Retrieve the vacation days for all employees.
Create Vacation Day for Employee:

Method: POST
URL: http://127.0.0.1:8000/kitchen/vacations/
Description: Create a vacation day for a specific employee. Provide the employee ID and the date of the vacation day in the request body.
Get Weekly Plan with Consideration of Weekly Off Days:

Method: GET
URL: http://127.0.0.1:8000/kitchen/weekly-plan/working_days/?date=<date>
Description: Retrieve the weekly plan for a specific date, considering the weekly off days (Friday and Saturday) as non-working days. Replace <date> with the desired date in the format "YYYY-MM-DD". The response will include the employee's name, service date, and day of the week.
Feel free to use these endpoints to manage vacation days, create vacation days for employees, and get the weekly plan while considering the weekly off days.
  
  
Additional Notes
The weekly plan consists of 5 working days.
You can check the vacation days for each employee and exclude them from the weekly plan if they have a vacation.
