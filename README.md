# BOOK STORE WITH PYTHON FLASK

## Terminal commands
Note: Make sure you have installed the [Python](https://www.python.org/downloads/)
### Clone the source code
    > git clone https://github.com/sieunhantanbao/book-strore.git
    > cd book-store
### Install [`virtualenv`](https://flask.palletsprojects.com/en/3.0.x/installation/#virtual-environments)
    > py -3 -m venv .venv
    > .venv\Scripts\activate
    
### Install the packages
    > pip install -r requirements.txt

### Run the data migration
    > flask db upgrade

### Run the app
    > python main.py

## Viewing the app ###

    Open the following url on your browser to view swagger documentation
    http://127.0.0.1:5000/