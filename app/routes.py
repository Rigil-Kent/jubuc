import os
import string
from datetime import datetime, timedelta, date
from app import app, db
from flask import render_template, redirect, flash, session, request, send_from_directory, url_for
from app.models import Administrator, User, Audio, Active, Post, Show
from app.forms import AdminForm, LoginForm, AudioForm, PlayerForm, PostForm, ShowForm
from flask_login import current_user, login_user, logout_user, login_required
from flask import Markup
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename


#region global vars & methods
accepted_methods = ["GET", "POST"]
translate = str.maketrans('', '', string.punctuation)


def upload_file(filerequest, type=None):
    if request.method =="POST":
        if filerequest not in request.files:
            message = Markup('<div class="alert alert-warning alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>No file part</div>')
            flash(message)
            return redirect(request.url)
        
        file = request.files[filerequest]
        print("attempting to upload {}".format(file.filename))
        if file.filename == '':
            message = Markup('<div class="alert alert-warning alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>No selected file</div>')
            flash(message)
            return redirect(request.url)

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
            return redirect(url_for(request.url))

#endregion


@app.route('/login', methods=accepted_methods)
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

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
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/', methods=accepted_methods)
def index():
    admin = db.session.query(Administrator).count()
    track = db.session.query(Active).get(1)
    posts = db.session.query(Post).all()
    shows = db.session.query(Show).all()

    if admin == 0:
        return redirect(url_for('admin_welcome'))

    return render_template('index.html', track=track, posts=posts, shows=shows)

@app.route('/about')
def about():
    track = db.session.query(Active).get(1)
    post = db.session.query(Post).order_by(Post.id.desc()).first()
    return render_template('about.html', post=post, track=track)


@app.route('/shows')
def shows():
    track = db.session.query(Active).get(1)
    shows = Show.query.filter(Show.timestamp >= date.today())
    past_shows = Show.query.filter(Show.timestamp <= date.today())
    return render_template('shows.html', track=track, shows=shows, past_shows=past_shows)


@app.route('/blog/<slug>')
def blog_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    prev_id = post.id - 1
    next_id = post.id + 1
    if prev_id > 0:
        prev = Post.query.filter_by(id=(prev_id)).first()
    else:
        prev = None

    if next_id > 0:
        _next = Post.query.filter_by(id=next_id).first()
    else:
        _next = None

    track = db.session.query(Active).get(1)
    
    return render_template('blog_post.html', prev=prev, next=_next, post=post, track=track)

@app.route('/shows/<slug>')
def show_post(slug):
    show = db.session.query(Show).filter_by(slug=Show.slug).first()
    track = db.session.query(Active).get(1)
    return render_template('blog_post.html', show=show, track=track)

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

@app.route('/admin/posts', methods=accepted_methods)
def admin_posts():
    form = PostForm()
    posts = Post.query.all()


    if form.validate_on_submit():
        post = Post()

        post.user_id = current_user.id
        post.title = form.title.data
        post.slug = form.title.data.translate(translate).replace(' ', '-').lower()
        post.body = form.body.data
        if form.featured_image.data is not None:
            post.featured_image = upload_file('featured_image', 'post')

        message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button> {} was posted sucessfully. </div>'.format(form.title.data))
        db.session.add(post)
        db.session.commit()
        flash(message)

        return redirect(url_for('admin_posts'))
    return render_template('admin/posts.html', form=form, posts=posts)

@app.route('/admin/shows', methods=accepted_methods)
def admin_shows():
    form = ShowForm()
    shows = db.session.query(Show).all()
    

    if form.validate_on_submit():
        show = Show()
        show.title = form.title.data
        show.slug = form.title.data.translate(translate).replace(' ', '-').lower()
        show.user_id = current_user.id
        show.timestamp = form.timestamp.data
        show.location = form.location.data
        show.url = form.url.data4
        show.details = form.details.data
        if form.url.data is not None:
            show.venue = '<a href="{}" alt="{}" title="{}">{}</a>'.format(form.url.data, form.title.data, form.title.data, form.title.data)
        else:
            show.venue = show.location

        if form.featured_image.data is not None:
             show.featured_image = upload_file('featured_image', 'post')
        
        message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button> {} was posted on the front page</div>'.format(form.title.data))
        
        db.session.add(show)
        db.session.commit()
        flash(message)
        return redirect(url_for('admin_shows'))

    return render_template('admin/shows.html', form=form, shows=shows)
#endregion