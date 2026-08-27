# DocDiagno: Heart Disease Prediction Risk Analytics Platform

DocDiagno is a Flask web application for exploring health information and estimating heart disease or diabetes risk with trained machine-learning models. It includes user registration and login, three prediction workflows, health tips, and a contact form.

**GitHub Repository:** [Heart Disease Prediction Risk Analytics Platform](https://github.com/saad112411/Heart-Disease-Prediction-Risk-Analytics-Platform-)

> This project is for educational and research use only. Its predictions are not a medical diagnosis and should not replace advice from a qualified healthcare professional.

## Features

- Framingham-based heart disease risk prediction
- Combined heart disease prediction
- Diabetes risk prediction
- User registration and login with bcrypt password hashing
- MySQL-backed user storage
- Health tips and contact form pages
- Pre-trained models stored in `models/`
- Jupyter notebooks and training scripts for experimentation and retraining

## Technology

- Python and Flask
- Flask-Bcrypt, Flask-MySQLdb, and Flask-Mail
- NumPy and scikit-learn-compatible pickle models
- HTML, CSS, and JavaScript frontend
- MySQL database

## Project Structure

```text
app.py                  Flask application and routes
models/                 Trained prediction models
Data/                   Datasets used by the project
templates/              Jinja2 HTML templates
static/                 CSS, JavaScript, and images
training/               Model-training code
Model_training/         Tuning utilities
Predictions/            Prediction helpers
notebooks/              Exploratory analysis and training notebooks
test_*.py               Test modules at the project root
requirements.txt        Python dependencies
```

## Installation

1. Clone the repository and enter the application directory:

	```bash
	git clone https://github.com/saad112411/Heart-Disease-Prediction-Risk-Analytics-Platform-.git
	cd Heart-Disease-Prediction-Risk-Analytics-Platform-/DocDiagno
	```

2. Create and activate a virtual environment:

	```bash
	python -m venv venv
	source venv/bin/activate       # Linux/macOS
	# venv\\Scripts\\activate    # Windows
	```

3. Install the dependencies:

	```bash
	python -m pip install -r requirements.txt
	```

## Database Setup

Create a MySQL database named `myflaskapp` and a `users` table before using registration or login:

```sql
CREATE DATABASE myflaskapp;
USE myflaskapp;

CREATE TABLE users (
	 id INT AUTO_INCREMENT PRIMARY KEY,
	 name VARCHAR(255) NOT NULL,
	 email_or_phone VARCHAR(255) NOT NULL UNIQUE,
	 password VARCHAR(255) NOT NULL
);
```

Update the MySQL and Flask-Mail settings in `app.py` or, preferably, move them to environment variables before deploying. Never commit real passwords, mail credentials, or production secret keys.

## Run the Application

From the `DocDiagno` directory:

```bash
python app.py
```

Open `http://127.0.0.1:5000/` in a browser. The main application pages include:

- `/` registration
- `/login` login
- `/heartfram` Framingham prediction
- `/heartcombined` combined heart disease prediction
- `/diabetes` diabetes prediction
- `/healthtips` health information

## Run Tests

```bash
pytest
```

## Data and Models

The repository includes CSV datasets, notebooks, training utilities, and serialized models. Retraining a model may change its feature order or preprocessing requirements, so keep the corresponding form fields and prediction code synchronized when replacing files in `models/`.

## License

No license is currently specified for this project.