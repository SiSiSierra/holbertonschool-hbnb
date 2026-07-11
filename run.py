from app import create_app
from app.services import facade

app = create_app()

if __name__ == '__main__':
    admin = {
            'first_name': 'admin',
            'last_name': 'user',
            'email': 'admin@user.com',
            'password': 'HBNB',
            'is_admin': True
            }
    with app.app_context():
        try:
            facade.get_user_by_email(admin['email'])
        except KeyError:
            facade.create_user(admin)
    app.run(debug=True)
