import os
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helper import apology, login_required
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///app.db")

@app.route('/')
@login_required
def home():
    schemes = [
        {
            "name": "Pradhan Mantri Jan Dhan Yojana",
            "link": "https://pmjdy.gov.in/",
            "tags": ["financial", "inclusion"]
        },
        {
            "name": "Ayushman Bharat",
            "link": "https://www.pmjay.gov.in/",
            "tags": ["medical", "healthcare"]
        },
        {
            "name": "Pradhan Mantri Awas Yojana",
            "link": "https://pmaymis.gov.in/",
            "tags": ["housing", "urban development"]
        },
        {
            "name": "National Scholarship Portal",
            "link": "https://scholarships.gov.in/",
            "tags": ["education", "scholarship"]
        },
        {
            "name": "Atal Pension Yojana",
            "link": "https://npscra.nsdl.co.in/scheme-details/APY.php",
            "tags": ["financial", "pension"]
        }
    ]
    return render_template('index.html', schemes=schemes)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("loginIdentifier"):
            return apology("must provide phone number or aadhar number", 400)

        # Ensure password was submitted
        elif not request.form.get("loginPassword"):
            return apology("must provide password", 400)

        login_identifier = request.form.get("loginIdentifier")
        password = request.form.get("loginPassword")

        # Determine if login identifier is Aadhar number or phone number
        if len(login_identifier) == 12 and login_identifier.isdigit():
            # Query database for Aadhar number
            rows = db.execute("SELECT * FROM user_primary_data JOIN user_secondary_data ON user_primary_data.user_id = user_secondary_data.user_id WHERE user_secondary_data.aadhar = ?", login_identifier)
        elif len(login_identifier) == 10 and login_identifier.isdigit():
            # Query database for phone number
            rows = db.execute("SELECT * FROM user_primary_data WHERE phone_number = ?", login_identifier)
        else:
            return apology("invalid phone number or aadhar number format", 400)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
            return apology("invalid phone number/aadhar number and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]
        print("login sucessfull")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
    

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Get form data
        first_name = request.form.get("firstName")
        middle_name = request.form.get("middleName")
        last_name = request.form.get("lastName")
        age = request.form.get("age")
        dob = request.form.get("dob")
        gender = request.form.get("gender")
        marital_status = request.form.get("maritalStatus")
        phone_number = request.form.get("phoneNumber")
        village_city = request.form.get("villageCity")
        district = request.form.get("district")
        state = request.form.get("state")
        country = request.form.get("country")
        pincode = request.form.get("pincode")
        partner_name = request.form.get("partnerName")
        parent_names = request.form.get("parentNames")
        children_details = request.form.get("childrenDetails")
        aadhar_number = request.form.get("aadharNumber")
        aadhar_copy = request.files["aadharCopy"]
        password = request.form.get("password")
        confirm_password = request.form.get("confirmPassword")

        # Validate form data
        if not first_name or not age or not dob or not gender or not marital_status or not phone_number or not village_city or not district or not state or not country or not pincode or not aadhar_number or not aadhar_copy or not password or not confirm_password:
            return apology("must provide all required fields", 400)

        if password != confirm_password:
            return apology("passwords do not match", 400)

        if len(aadhar_number) != 12:
            return apology("aadhar number must be exactly 12 digits", 400)

        # Save aadhar copy
        aadhar_copy_filename = secure_filename(aadhar_copy.filename)
        aadhar_copy.save(os.path.join("uploads", aadhar_copy_filename))

        # Hash password
        hash = generate_password_hash(password)

        # Combine first, middle, and last names
        full_name = f"{first_name} {middle_name} {last_name}".strip()

        try:
            # Begin a transaction
            db.execute("BEGIN TRANSACTION")

            # Insert user into user_primary_data table
            user_id = db.execute("INSERT INTO user_primary_data (password, name, dob, sex, phone_number, caste) VALUES (?, ?, ?, ?, ?, ?)",
                     hash, full_name, dob, gender, phone_number, "N/A")

            # Insert user into user_secondary_data table
            db.execute("INSERT INTO user_secondary_data (user_id, address, email, aadhar, PAN, disability, ration_card, marital_status, spouse_details, child_details) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   user_id, f"{village_city}, {district}, {state}, {country}, {pincode}", "N/A", aadhar_number, "N/A", "N/A", "N/A", marital_status, partner_name, children_details)

            # Commit the transaction
            db.execute("COMMIT")

        except Exception as e:
            # Rollback the transaction in case of error
            db.execute("ROLLBACK")
            return apology(f"An error occurred: {e}", 500)

        # Redirect to login page
        return redirect("/login")

    else:
        return render_template("registration.html")

# Add this new route to handle chat messages

@app.route("/chat", methods=["POST"])
@login_required
def chat():
    """Handle chat messages"""
    message = request.json.get("message")
    if not message:
        return {"error": "Message is required"}, 400
    
    # For now, just echo back the message
    # Later we can implement actual chatbot logic here
    response = f"You said: {message}"
    
    return {"response": response}

@app.route("/logout")
def logout():
    """Log user out"""
    # Clear the session
    session.clear()
    # Redirect to login page
    return redirect("/login")










if __name__ == '__main__':
    app.run(debug=True)
    