Password Strength Checker

This is a Flask-based web application designed to assess the strength of a given password based on several criteria. The application checks for length, complexity, common passwords, and repetition of characters to provide feedback on the strength of the password.
Features

    Password Length: Ensures the password is at least 12 characters long.
    Complexity Check: Verifies the inclusion of uppercase letters, lowercase letters, digits, and special characters.
    Repetition Check: Detects more than 3 consecutive or non-consecutive identical characters.
    Common Password Check: Ensures the password is not a common or easily guessable password.
    Real-Time Feedback: Provides immediate feedback on password strength as you type.

Requirements

    Python 3.6 or higher
    Flask

Installation
 Clone the Repository
 bash
   
    git clone https://github.com/NATHIYA-S2/password-strength-checker.git
    cd password-strength-checker

Install Dependencies
bash
   
    pip install -r requirements.txt

Run the Application

bash

    python passtrength_check.py

    By default, the application will run on http://127.0.0.1:5000.

Usage

    Open your web browser and navigate to http://127.0.0.1:5000.
    Enter a password into the input field and click "Check Strength" or simply start typing.
    The application will display the password strength and check the password against various requirements.

Application Structure

    passtrength_check.py: Contains the Flask application and routes.
        /: Renders the main HTML page for the password strength checker.
        /check_password: API endpoint that checks password requirements in real-time.
        /assess_password: API endpoint that assesses the overall strength of the password.

    requirements.txt: Lists the dependencies for the project.

    static/: Contains static files such as CSS and JavaScript (not used in this project, but a typical directory for static assets).

Password Requirements

    Length: At least 12 characters.
    Complexity:
        At least one uppercase letter (A-Z).
        At least one lowercase letter (a-z).
        At least one digit (0-9).
        At least one special character (e.g., !@#$%^&*()-_=+[{]}|;:'",<.>/?).
    Common Passwords: The password must not be a common password.
    Repetition: No more than 3 consecutive or non-consecutive identical characters.
    
Acknowledgements

    Flask Documentation: For the web framework.
    Python Documentation: For Python programming references.
