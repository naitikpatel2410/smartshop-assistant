from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    # Create a new user (use your desired username, email, and password)
    user = User(username='admin7', password='admin123')

    # Add user to the database
    db.session.add(user)
    db.session.commit()

    print("User added to the database!")
