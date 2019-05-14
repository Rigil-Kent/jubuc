from app import app, db
from app.models import User, Administrator, Audio, Active, Post, Show, Photo
from werkzeug.security import generate_password_hash, check_password_hash



@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Administrator': Administrator,
        'Audio': Audio,
        'Active, Post': Active, 
        'Post': Post,
        'Show': Show,
        'Photo': Photo
    }


if __name__ == "__main__":
    app.run(host='0.0.0.0')