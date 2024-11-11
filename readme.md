# Todo Application

A simple Todo application built using Django and Bootstrap. This application allows users to manage projects, todos, and export project summaries as gists in Markdown format.

## Setup

Follow these steps to set up the application locally:

### Prerequisites

- Python 3.8+
- Django 3.x
- pip (Python package installer)

#### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/ajaye2901/hatio-todoapp/tree/main
cd hatio_todo
```

#### Step 2: Create a Virtual Environment

Create a virtual environment: 

```     python3 -m venv venv       ```

#### Step 3: Activate the Virtual Environment

Activate the virtual environment:

On Windows - ``` venv\Scripts\activate  ```
On macOS/Linux - ```  source venv/bin/activate  ```

#### Step 4: Install Dependencies

Install the required dependencies from requirements.txt: 

```   pip install -r requirements.txt   ```

This will install Django and any other required libraries.


#### Step 5: Configure SQLite Database

SQLite is used as the default database, so no additional setup is required for the database. Django will automatically create the database file.

#### Step 6: Run Database Migrations

Django uses migrations to set up your database. Run the following command to apply the migrations:

```   python manage.py migrate  ```

This will create the necessary tables in the SQLite database.


##### RUN

# Step 1: Start the Django Development Server
To run the application locally:

```  python manage.py runserver  ```

This will start the development server at http://127.0.0.1:8000/ with a login page


## Step 2: Create a user by pressing the Register button

Give the details and register the user

### Step 3: Login

login in using the credentials for the registered user

#### Step 4: Home page of todo application

You can create a project from the page and view all the created projects and can navigate to seperate project by clicking the view button also can edit the project.

#### step 5 : Detail Page of project

Here you can view the todos created with pending and completed status also can create a new todo for the each created todo we can edit and delete that todos also we can export the project as gist by pressing the export gist button
