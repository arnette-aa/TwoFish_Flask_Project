from forms import RegisterForm, LoginForm

@app.route('Login')
def login_page():
    form = LoginForm()
    return render_template('login.html', form=fomr)

@app.route('/', methods=['POST', 'GET'])
def login_page():
    return render_template('login.html')


@app.route('/register', methods=['Post', 'Get'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              password_hash=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('login'))

    if form.errors != {}: #If there are no erros in the validation
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/logout')
def logout_page():
    return 
