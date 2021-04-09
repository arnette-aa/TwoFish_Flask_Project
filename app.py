from flask import Flask, redirect, url_for, render_template, request, flash
from models import db, User, Todo
from forms import RegisterForm, LoginForm, TaskForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00'
app.config['DEBUG'] = True

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db.init_app(app)

db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        attempted_password = form.password.data
        password = attempted_user.password
        if attempted_user and check_password(
            attempted_password, password
            ):
                login_user(attempted_user)
                flash(f'Success! You are logged in as: {attempted_user.username} ')
                return redirect(url_for('index'))
        else:
            flash('Username and password do not match. Please try again')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have successfully logget out.')
    return redirect(url_for('login_page')) 


@app.route('/register', methods=['Post', 'Get'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are now logged in as: {user_to_create.username} ')
        return redirect(url_for('index'))

    if form.errors != {}: #If there are no erros in the validation
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/taskmaster', methods=['POST', 'GET'])
@login_required
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/taskmaster')
        except:
            return 'err'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/taskmaster')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
    else:
        return render_template('update.html', task=task)

    try:
        db.session.commit()
        return redirect('/taskmaster')
    except:
        return 'There was an issue updating this task'

def check_password(attempted_password, password):
    if attempted_password == password:
        return True

    

if __name__ == "__main__":
     app.run(port=3000)
