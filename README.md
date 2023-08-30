# COMPSCI 235 S2 2023: Game Library Web Application by Tom, Victoria and Kevin

## Description

A Web application that demonstrates use of Python's Flask framework and makes use of libraries such as Jinja templating libraries.
Architectural design patterns and principles including Repository, Dependency Inversion and Single Responsibility have been used to design the application. 
The application uses Flask Blueprints to maintain a separation of concerns between application functions. 
Unit testing using the pytest tool verifies model, repository and service layer functionality,

## Installation

**Installation via requirements.txt**

**Windows**
```shell
$ cd cs235-2023-gameswebapp-assignment-tlig606_kjia020_vrya365
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

**MacOS**
```shell
$ cd cs235-2023-gameswebapp-assignment-tlig606_kjia020_vrya365
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File or PyCharm'->'Settings' and select this project from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add Interpreter'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution

**Running the application**

From the *cs235-2023-gameswebapp-assignment-tlig606_kjia020_vrya365* directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 

## Testing

After you have configured pytest as the testing tool for PyCharm (File - Settings - Tools - Python Integrated Tools - Testing), you can then run tests from within PyCharm by right-clicking the tests folder and selecting "Run pytest in tests".

Alternatively, from a terminal in the root folder of the project, you can also call 'python -m pytest tests' to run all the tests. PyCharm also provides a built-in terminal, which uses the configured virtual environment. 

## Configuration

The *cs235-2023-gameswebapp-assignment-tlig606_kjia020_vrya365/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.
 
## Data sources

The data files are modified excerpts downloaded from:

https://huggingface.co/datasets/FronkonGames/steam-games-dataset



