# protein-domain-api
A demo project to create a REST-API for organismal protein data using Django and the Django-rest-framework.

## Installation Instructions (linux)
The following instructions assume you already have python, pip and venv installed on your system. If not please refer to the following link to get set up with Python and pip. https://www.python.org/downloads/

By making use of the relevant installation for your system from the link above you should automatically have pip and venv installed.
You can check this by opening a terminal and entering the commands:
`pip --version`
`venv --version`

If you do not find an installed version on your system you can find instructions and downloads at the following links:
[https://pip.pypa.io/en/stable/installing/] (pip)
[https://pypi.org/project/virtualenv/ ] (venv)

You can ensure you have the most up to date version of pip with the following command:
`python -m pip install --upgrade pip`

1. Navigate to the directory you would like to install the Protein Domains app in.

2. Clone this repository.

3. Open a terminal and navigate to inside the `proteindomains` folder (you should be in the top level directory where the requirements.txt file is stored). 

4. Enter the following command to create a Python virtual environment in which to install the necessary packages, give your environment a meaningful name:`python3 -m venv ./ <virtual environment name>`

5. Activate the new virtual environment with (bash/zsh)`$ source <venv>/bin/activate`. You should see the name of your virtual environment in your terminal prompt.

6. Run the following command to install the necessary packages to run the Protein Domains app:
`pip install -r requirements.txt`

7. At first, the database is built but contains no data. Import the data from the supplied input files with the following command:
     `python manage.py importdata`

8. You can now run the Protein Domain server with: `python manage.py runserver 127.0.0.1:8000`

9. Navigate to http://127.0.0.1:8000/admin and login with the superuser credentials:
       username: root
       password: root
       (here you should set up users and change the superuser credentials)

10. Navigate to  http://127.0.0.1:8000/api to see the endpoint options you can access which fulfill the requirements in the specification.
