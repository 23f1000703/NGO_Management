# NGO Management System

A Flask-based web application for managing NGO records through a
browser-based interface.

**GitHub:** https://github.com/23f1000703/NGO_Management

## Features

-   Login page
-   Staff management
-   Add, edit, and delete records
-   Beneficiary management
-   Donation management
-   Search and filtering


## Tech Stack

-   Python and Flask
-   SQLite
-   HTML, CSS, Bootstrap
-   Jinja2 templates

## Installation

Clone the repository:

``` bash
git clone https://github.com/23f1000703/NGO_Management.git
cd NGO_Management
```

Create and activate a virtual environment (Windows):

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies from `requirements.txt`:

``` bash
pip install -r requirements.txt
```

Run the application:

``` bash
python app.py
```

Open the local URL shown in the terminal. 
You can Login using username--admin123 and password -- admin134

## Database

The application uses SQLite. Check `app.py` for the database location
and initialization steps. Use fictional data in public demos.

