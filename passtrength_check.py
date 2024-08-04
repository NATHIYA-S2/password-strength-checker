from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Function to check if the password length is at least 12 characters
def check_length(password):
    return len(password) >= 12

# Function to check complexity requirements
def check_complexity(password):
    has_uppercase = any(c.isupper() for c in password)
    has_lowercase = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in r'!@#$%^&*()-_=+[{]}\|;:\'",<.>/?' for c in password)
    return has_uppercase, has_lowercase, has_digit, has_special

# Function to check for more than 3 consecutive or non-consecutive identical characters
def check_repeated_characters(password):
    # Check for more than 3 consecutive identical characters
    if any(password[i] == password[i + 1] == password[i + 2] == password[i + 3] for i in range(len(password) - 3)):
        return False
    
    # Check for more than 3 non-consecutive identical characters
    for char in set(password):
        if password.count(char) > 3:
            return False

    return True

# Common passwords for the uniqueness check
common_passwords = ["0","0000","00000","000000","0000000","00000000","9999999999","123456","password","123456789","qwerty","12345678","password1","1234567","iloveyou","letmein","welcome","admin","letmein1","1q2w3e4r","password123","abc123","123123","monkey","1234","sunshine","football"]

# Function to check if the password is in the list of common passwords
def check_common_password(password):
    return password not in common_passwords

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Strength Checker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
        }
        .container {
            width: 80%;
            margin: auto;
            overflow: hidden;
        }
        header {
            background: #333;
            color: #fff;
            padding-top: 30px;
            min-height: 70px;
            border-bottom: #fff 3px solid;
            text-align: center;
        }
        h1 {
            margin: 0;
            font-size: 24px;
        }
        .form-container {
            background: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
            text-align: center;
        }
        input[type="text"] {
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            width: 80%;
            max-width: 500px;
        }
        button {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            background-color: #333;
            color: #fff;
            font-size: 16px;
            cursor: pointer;
        }
        button:disabled {
            background-color: #aaa;
            cursor: not-allowed;
        }
        button:hover {
            background-color: #555;
        }
        .result {
            margin-top: 20px;
            font-size: 18px;
            font-weight: bold;
        }
        .requirements {
            margin-top: 20px;
            text-align: left;
            font-size: 16px;
        }
        .requirements ul {
            list-style: none;
            padding: 0;
        }
        .requirements li {
            margin-bottom: 10px;
        }
        .requirement-status {
            color: #d9534f; /* Default color for unmet requirements */
        }
        .requirement-status.satisfied {
            color: #000; /* Black color for met requirements */
        }
        .requirement-status.bold {
            font-weight: bold; /* Bold text for unmet requirements */
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>Password Strength Checker</h1>
        </div>
    </header>
    
    <div class="container">
        <div class="form-container">
            <h2>Check Your Password Strength</h2>
            <form id="password-form" method="post" action="/assess_password">
                <input type="text" id="password" name="password" placeholder="Enter your password" required>
                <button type="submit">Check Strength</button>
            </form>
            <div class="result" id="result"></div>
            <div class="requirements">
                <h3>Password Requirements:</h3>
                <ul>
                    <li><span id="length-status" class="requirement-status">Must be at least 12 characters long.</span></li>
                    <li><span id="uppercase-status" class="requirement-status">Must include at least one uppercase letter (A-Z).</span></li>
                    <li><span id="lowercase-status" class="requirement-status">Must include at least one lowercase letter (a-z).</span></li>
                    <li><span id="digit-status" class="requirement-status">Must include at least one number (0-9).</span></li>
                    <li><span id="special-status" class="requirement-status">Must include at least one special character (e.g., !@#$%^&*()-_=+[{\\]}\|;:'",<.>/?).</span></li>
                    <li><span id="common-status" class="requirement-status">Cannot be a common password.</span></li>
                    <li><span id="repeated-status" class="requirement-status">Cannot have more than 3 consecutive or non-consecutive identical characters.</span></li>
                </ul>
            </div>
        </div>
    </div>
    
    <script>
        document.getElementById('password').addEventListener('input', function() {
            const password = document.getElementById('password').value;

            fetch('/check_password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({ 'password': password })
            })
            .then(response => response.json())
            .then(data => {
                // Update requirement statuses dynamically
                updateRequirementStatus('length-status', data.length_ok);
                updateRequirementStatus('uppercase-status', data.has_uppercase);
                updateRequirementStatus('lowercase-status', data.has_lowercase);
                updateRequirementStatus('digit-status', data.has_digit);
                updateRequirementStatus('special-status', data.has_special);
                updateRequirementStatus('common-status', data.common_ok);
                updateRequirementStatus('repeated-status', data.repeated_ok);
            });
        });

        document.getElementById('password-form').addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission

            const password = document.getElementById('password').value;

            fetch('/assess_password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({ 'password': password })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('result').innerText = `Your password strength is: ${data.strength}`;
                
                // Update requirement statuses
                updateRequirementStatus('length-status', data.length_ok);
                updateRequirementStatus('uppercase-status', data.has_uppercase);
                updateRequirementStatus('lowercase-status', data.has_lowercase);
                updateRequirementStatus('digit-status', data.has_digit);
                updateRequirementStatus('special-status', data.has_special);
                updateRequirementStatus('common-status', data.common_ok);
                updateRequirementStatus('repeated-status', data.repeated_ok);
            });
        });

        function updateRequirementStatus(elementId, status) {
            const element = document.getElementById(elementId);
            if (status) {
                element.classList.add('satisfied');
                element.classList.remove('bold');
            } else {
                element.classList.add('bold');
                element.classList.remove('satisfied');
            }
        }
    </script>
</body>
</html>
    ''')

@app.route('/check_password', methods=['POST'])
def check_password():
    password = request.form.get('password')
    length_ok = check_length(password)
    has_uppercase, has_lowercase, has_digit, has_special = check_complexity(password)
    repeated_ok = check_repeated_characters(password)
    common_ok = check_common_password(password)

    return jsonify({
        'length_ok': length_ok,
        'has_uppercase': has_uppercase,
        'has_lowercase': has_lowercase,
        'has_digit': has_digit,
        'has_special': has_special,
        'common_ok': common_ok,
        'repeated_ok': repeated_ok
    })

@app.route('/assess_password', methods=['POST'])
def assess_password():
    password = request.form.get('password')
    length_ok = check_length(password)
    has_uppercase, has_lowercase, has_digit, has_special = check_complexity(password)
    repeated_ok = check_repeated_characters(password)
    common_ok = check_common_password(password)
    
    requirements = {
        'length_ok': length_ok,
        'has_uppercase': has_uppercase,
        'has_lowercase': has_lowercase,
        'has_digit': has_digit,
        'has_special': has_special,
        'common_ok': common_ok,
        'repeated_ok': repeated_ok
    }

    # Calculate strength based on requirements met
    requirements_met = sum(requirements.values())

    if length_ok and has_uppercase and has_lowercase and has_digit and has_special and common_ok and repeated_ok:
        strength = "Strong - Your password meets all the requirements."
    elif requirements_met >= 5:
        strength = "Above Moderate - Your password meets most of the requirements."
    elif requirements_met > 3:
        strength = "Moderate - Your password meets more than three requirements."
    else:
        strength = "Weak - Your password does not meet enough requirements."
    
    return jsonify({
        'strength': strength,
        **requirements
    })

if __name__ == '__main__':
    app.run(debug=True)

