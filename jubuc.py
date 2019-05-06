from app import app, db
from app.models import User, Administrator, Audio, Active
from werkzeug.security import generate_password_hash, check_password_hash



@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Administrator': Administrator,
        'Audio': Audio,
        'Active': Active
    }


if __name__ == "__main__":
    app.run()