import os
from app import app, db
from flask import render_template, redirect, flash, session, request, send_from_directory, url_for
from app.models import Administrator, User, Audio, Active
from app.forms import AdminForm, LoginForm, AudioForm, PlayerForm
from flask_login import current_user, login_user, logout_user, login_required
from flask import Markup
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename


#region global vars & methods
accepted_methods = ["GET", "POST"]


def upload_file(filerequest, type=None):
    if request.method =="POST":
        if filerequest not in request.files:
            message = Markup('<div class="alert alert-warning alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>No file part</div>')
            flash(message)
            return redirect(request.url_rule.endpoint)
        
        file = request.files[filerequest]
        print("attempting to upload {}".format(file.filename))
        if file.filename == '':
            message = Markup('<div class="alert alert-warning alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>No selected file</div>')
            flash(message)
            return redirect(request.url_rule.endpoint)

        try:
            filename = secure_filename(file.filename)
            print(filename)
            print(os.path.join(app.config['AUDIO'], filename))
            if type=="audio":
                file.save(os.path.join(app.config['AUDIO'], filename))
            elif type=="post":
                file.save(os.path.join(app.config['POSTS'], filename))
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>File uploaded successfully</div>')
            flash(message)
            return filename
        except Exception as e:
            message = Markup('<div class="alert alert-dagner alert-dismissible"><button type="button" class="close">&times;</button>File upload failed: {}'.format(e))
            flash(message)
            return redirect(url_for(request.url_rule.endpoint))

#endregion


@app.route('/login', methods=accepted_methods)
def login():
    if current_user.is_authenticated:
        return redirect(url_for('alt_index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=form.username.data).first()
        print(user.username)
        if user is None or not user.check_password(form.password.data):
            message = Markup('<div class="alert alert-danger alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>Invalid username or password</div>')
            return redirect(url_for('admin_dashboard'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('alt_index')
        return redirect(next_page)
    return render_template('layout2/login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
def index():
    return render_template('layout1/index.html')


@app.route('/index', methods=accepted_methods)
def alt_index():
    admin = db.session.query(Administrator).count()
    track = db.session.query(Active).get(1)
    print(admin)

    if admin == 0:
        return redirect(url_for('admin_welcome'))

    return render_template('layout2/index.html', track=track)

@app.route('/photos')
def photos():
    return render_template('photos.html')



#region ADMINISTRATION
@app.route('/admin')
def admin_dashboard():
    u_count = User.query.count()
    users = db.session.query(User).all()
    return render_template('admin/index.html', u_count=u_count, users=users)


@app.route('/admin/setup')
def admin_setup():
    return render_template('admin/setup.html')

@app.route('/admin/welcome', methods=accepted_methods)
def admin_welcome():
    form = AdminForm()

    if form.validate_on_submit():
        admin = Administrator()
        admin.username = form.username.data
        admin.first_name = form.first_name.data
        admin.last_name = form.last_name.data
        admin.email = form.email.data
        admin.set_password(form.password.data)
        print(form.password.data)
        print(admin.pass_hash)
        admin.site_title = form.site_title.data
        admin.site_logo_image = form.site_logo_image.data
        admin.site_logo_text = form.site_logo_text.data
        admin.jumbotron_image = form.jumbotron_image.data
        admin.site_dominant_color = form.site_dominant_color.data
        admin.site_accent_color = form.site_accent_color.data
        admin.site_background_color = form.site_background_color.data
        admin.facebook = form.facebook.data
        admin.twitter = form.twitter.data
        admin.instagram = form.instagram.data
        admin.soundcloud = form.soundcloud.data
        admin.youtube = form.youtube.data
        admin.spotify = form.spotify.data
        admin.twitter_consumer_key = form.twitter_consumer_key.data
        admin.twitter_consumer_key_secret = form.twitter_consumer_key_secret.data
        admin.twitter_access_token = form.twitter_access_token.data
        admin.twitter_access_token_secret = form.twitter_access_token_secret.data

        db.session.add(admin)
        
        user = User()
        user.username = admin.username
        user.first_name = admin.first_name
        user.last_name = admin.last_name
        user.email = admin.email
        user.pass_hash = admin.pass_hash

        db.session.add(user)

        db.session.commit()

        message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dimiss="alert">&times;</button> Administrative settings saved. User {} has been created.'.format(user.username))
        flash(message)
        return redirect(url_for('login'))
    return render_template('admin/welcome.html', form=form)


@app.route('/admin/audio', methods=accepted_methods)
def admin_audio():
    form = PlayerForm()
    upform = AudioForm()
    tracks = Audio.query.all()
    
            
    if form.validate_on_submit():
        if form.active_track.data is None:
            pass
        else:
            active = Active.query.get(1)
            print(active)

            if active is None:
                active = Active()
            
            active.track_id = form.active_track.data.id
            print("saving active track")
            db.session.add(active)
            db.session.commit()

            return redirect(url_for('admin_audio'))


    if upform.validate_on_submit():
        audio = Audio()
        audio.name = upform.name.data
        audio.is_active = upform.is_active.data
        audio.file = upload_file('file', type='audio')
        if upform.album_art.data is not None:
            audio.album_art = upload_file('album_art', type="audio")
        

        db.session.add(audio)
        db.session.commit()

        message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button> Audio track added successfully!</div>')
        return redirect(url_for('admin_audio'))

    return render_template('admin/audio.html', form=form, upform=upform, tracks=tracks)

#endregion