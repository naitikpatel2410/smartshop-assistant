from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    
    if 'user_id' in session:
        return redirect(url_for('main.index')) 

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('main.index'))  
        else:
            flash("Invalid credentials!")

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)  
    return redirect(url_for('auth.login'))  
