To run the application, use the flask command or python -m flask. Before you can do that you need to tell your terminal the application to work with by exporting the FLASK_APP environment variable:

bash:
$ export FLASK_APP=setup
$ flask run
 * Running on http://127.0.0.1:5000/
Fish:
$ set -x FLASK_APP setup
$ flask run
 * Running on http://127.0.0.1:5000/
CMD:
$ set FLASK_ENV=development
$ set FLASK_APP=setup
$ flask run
 * Running on http://127.0.0.1:5000/

Powershell
$ $env:FLASK_APP = "setup"
$ flask run
 * Running on http://127.0.0.1:5000/
