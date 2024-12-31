# User Routes
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        farmer_type = request.form['farmer_type']
        province = request.form['province']
        farm_size = request.form['farm_size']

        # Password hashing
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('signup'))
        
        # Use the correct hashing method
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create a new user record
        new_user = User(full_name=full_name, phone=phone, email=email, password=hashed_password,
                        farmer_type=farmer_type, province=province, farm_size=farm_size)

        try:
            # Add to the database and commit
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
        except:
            flash('Error in account creation. Try again!', 'danger')
            return redirect(url_for('signup'))
    return render_template("signup.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Store the user id in the session
            session['username'] = user.full_name  # Store the user's name in session
            flash('Login successful!', 'success')
            return redirect(url_for('index'))  # Redirect to the main page
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('crop_prediction'))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('user_id', None)  # Remove user_id from session
    session.pop('username', None)  # Remove username from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))
