from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():

    user = User(username='admin7', password='admin123')

    
    db.session.add(user)
    db.session.commit()

    print("User added to the database!")
