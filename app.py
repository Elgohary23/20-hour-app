from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Skill
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skills.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('skills'))
    if request.method == 'POST':
        if User.query.filter_by(username=request.form['username']).first():
            flash('Username already exists')
            return redirect(url_for('signup'))

        user = User(
            username=request.form['username'],
            email=request.form['email']
        )
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('skills'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Login route called")
    if current_user.is_authenticated:
        print("User is already authenticated, redirecting to skills")
        return redirect(url_for('skills'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            print(f"User {user.username} logged in successfully")
            login_user(user)
            print("Calling redirect to skills")
            return redirect(url_for('skills'))
        else:
            print("Invalid username or password")
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/skills', methods=['GET', 'POST'])
@login_required
def skills():
    print(f"Skills route called. Current user: {current_user}") # Add this line
    if request.method == 'POST':
        new_skill = Skill(
            title=request.form['title'],
            tags=request.form['tags'],
            priority=request.form['priority'],
            duration_hours=0.0,  # Set default duration to 0
            user_id=current_user.id
        )
        db.session.add(new_skill)
        db.session.commit()
        return redirect(url_for('skills'))

    user_skills = Skill.query.filter_by(user_id=current_user.id).order_by(
        db.case(
            (Skill.priority == 'high', 1),
            (Skill.priority == 'moderate', 2),
            (Skill.priority == 'low', 3)
        )
    ).all()
    return render_template('skills.html', skills=user_skills)

@app.route('/skill/<int:skill_id>', methods=['GET', 'POST'])
@login_required
def skill_detail(skill_id):
    skill = Skill.query.get_or_404(skill_id)

    # Verify that the skill belongs to the current user
    if skill.user_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        data = request.get_json()
        if data and 'duration' in data:
            # Convert minutes to hours and add to existing duration
            skill.duration_hours += data['duration'] / 60
            db.session.commit()
            return jsonify({'success': True})

    return render_template('skill_detail.html', skill=skill)

if __name__ == '__main__':
    app.run(debug=True)
