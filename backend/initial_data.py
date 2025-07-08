from models import db, User, Role
from werkzeug.security import generate_password_hash
from datetime import date

def create_admin(app):
    with app.app_context():
        db.create_all()

        # Ensure roles exist
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin', description='Superuser Admin Role')
            db.session.add(admin_role)

        user_role = Role.query.filter_by(name='user').first()
        if not user_role:
            user_role = Role(name='user', description='Standard User Role')
            db.session.add(user_role)

        db.session.commit()

        # Ensure Admin exists
        admin_email = 'admin@quizmaster.com'
        existing_admin = User.query.filter_by(email=admin_email).first()

        if not existing_admin:
            admin = User(
                email=admin_email,
                password=generate_password_hash('admin123'),
                full_name='Quiz Master Admin',
                dob=date(1990, 1, 1),
                qualification='Admin Role'
            )
            admin.roles.append(admin_role)
            db.session.add(admin)
            db.session.commit()
            print("Admin account created.")
        else:
            print("Admin already exists.")
