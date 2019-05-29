import os
import string
from datetime import datetime, timedelta, date
from app import app, db
from flask import render_template, redirect, flash, session, request, send_from_directory, url_for
from app.models import Administrator, User, Audio, Active, Post, Show, Photo, Contact
from app.forms import AdminForm, LoginForm, AudioForm, PlayerForm, PhotoForm, PostForm, ShowForm, UserForm, ContactForm, EditPhotoForm, SettingsForm, EditUserForm, EditShowForm, EditContactForm, EditAudioForm, EditPostForm
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
            message = Markup('<div class="alert alert-dagner alert-dismissible"><button type="button" class="close">&times;</button>File upload failed: {}</div>'.format(e))
            flash(message)
            return redirect(url_for(request.url))

#endregion


@app.route('/login', methods=accepted_methods)
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    admin = db.session.query(Administrator).count()
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
            next_page = url_for('admin_dashboard')
        return redirect(next_page)
    return render_template('login.html', form=form, admin_setting=admin)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/', methods=accepted_methods)
def index():
    admin = db.session.query(Administrator).count()
    track = db.session.query(Active).get(1)
    posts = db.session.query(Post).order_by(Post.id.desc()).limit(4)
    shows = Show.query.filter(Show.timestamp >= date.today()).order_by(Show.timestamp.desc()).limit(4)
    photos = db.session.query(Photo).order_by(Photo.timestamp.desc()).limit(4)
    form = ContactForm()


    if admin == 0:
        return redirect(url_for('admin_welcome'))

    admin_settings = db.session.query(Administrator).get(1)

    if form.validate_on_submit():
        contact = Contact()
        contact.name = form.name.data
        contact.email = form.email.data
        contact.phone = form.phone.data
        contact.subject = form.subject.data
        contact.message = form.message.data

        db.session.add(contact)
        db.session.commit()

        message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button> Thank you! Jubuc will be in touch with you shortly.</div>')
        flash(message)
        return redirect(url_for('index'))

    return render_template('index.html', form=form, track=track, posts=posts, shows=shows, photos=photos, admin_settings=admin_settings)

@app.route('/about', methods=accepted_methods)
def about():
    track = db.session.query(Active).get(1)
    post = db.session.query(Post).order_by(Post.id.desc()).first()
    admin_settings = db.session.query(Administrator).get(1)
    form = ContactForm()

    if form.validate_on_submit():
        contact = Contact()
        contact.name = form.name.data
        contact.email = form.email.data
        contact.phone = form.phone.data
        contact.subject = form.subject.data
        contact.message = form.subject.data
        
        db.session.add(contact)
        db.session.commit()
        message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button> Thank you! Jubuc will be in touch with you shortly.</div>')
        flash(message)
        return redirect(url_for('index'))


    return render_template('about.html', form=form, admin_settings=admin_settings, post=post, track=track)


@app.route('/shows', methods=accepted_methods)
def shows():
    form = ContactForm()
    track = db.session.query(Active).get(1)
    shows = Show.query.filter(Show.timestamp >= date.today()).order_by(Show.timestamp.desc()).limit(10)
    past_shows = Show.query.filter(Show.timestamp <= date.today()).order_by(Show.timestamp.desc()).limit(5)
    admin_settings = db.session.query(Administrator).get(1)

    if form.validate_on_submit():
        contact = Contact()
        contact.name = form.name.data
        contact.email = form.email.data
        contact.phone = form.phone.data
        contact.subject = form.subject.data
        contact.message = form.subject.data
        
        db.session.add(contact)
        db.session.commit()
        message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button> Thank you! Jubuc will be in touch with you shortly.</div>')
        flash(message)
        return redirect(url_for('index'))

    return render_template('shows.html', track=track, admin_settings=admin_settings, shows=shows, past_shows=past_shows, form=form)


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

@app.route('/blog')
def blog():
    posts = Post.query.all()
    admin_settings = Administrator.query.get(1)
    return render_template('blog.html', posts=posts, admin_settings=admin_settings)


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
@login_required
def admin_dashboard():
    u_count = User.query.count()
    t_count = Audio.query.count()
    p_count = Post.query.count()
    s_count = Show.query.count()
    users = db.session.query(User).all()
    return render_template('admin/index.html', u_count=u_count, p_count=p_count, t_count=t_count, s_count=s_count, users=users)

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

        message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dimiss="alert">&times;</button> Administrative settings saved. User {} has been created.</div>'.format(user.username))
        flash(message)
        return redirect(url_for('login'))
    return render_template('admin/welcome.html', form=form)

@app.route('/admin/audio', methods=accepted_methods)
@login_required
def admin_audio():
    form = PlayerForm()
    upform = AudioForm()
    tracks = Audio.query.all()
    
            
    if form.validate_on_submit():
        if form.active_track.data is None:
            pass
        else:
            active = Active.query.get(1)

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
@login_required
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
@login_required
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
        show.url = form.url.data
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

@app.route('/admin/photos', methods=accepted_methods)
@login_required
def admin_photos():
    form = PhotoForm()
    photos = db.session.query(Photo).all()

    if form.validate_on_submit():
        photo = Photo()
        photo.name = form.name.data
        photo.caption = form.caption.data
        photo.file = upload_file('file')
        photo.user_id = current_user.id

        db.session.add(photo)
        db.session.commit()
        message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>Photo added successfully</div>')
        flash(message)
        return redirect(url_for('admin_photos'))
    return render_template('admin/photos.html', form=form, photos=photos)

@app.route('/admin/users', methods=accepted_methods)
@login_required
def admin_users():
    form = UserForm()
    users = db.session.query(User).all()

    if form.validate_on_submit():
        user =  User()
        user.username = form.username.data
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.pass_hash = user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>User <strong>{}</strong> added.</div>'.format(user.username))
        flash(message)
        return redirect(url_for('admin_users'))
    return render_template('admin/user.html', form=form, users=users)

@app.route('/admin/contacts', methods=accepted_methods)
@login_required
def admin_contacts():
    form = ContactForm()
    contacts = db.session.query(Contact).all()

    if form.validate_on_submit():
        contact = Contact()
        contact.name = form.name.data
        contact.email = form.email.data
        contact.phone = form.phone.data
        contact.subject = form.subject.data
        contact.message = form.message.data

        db.session.add(contact)
        db.session.commit()

        message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>Contact added successfully for {}</div>'.format(contact.name))
        flash(message)
        return redirect(url_for('admin_contacts'))
    return render_template('admin/contact.html', form=form, contacts=contacts)

@app.route('/admin/settings', methods=accepted_methods)
@login_required
def admin_settings():
    form = SettingsForm()
    admin = db.session.query(Administrator).get(1)
    if request.method == "GET":
        form.username.data = admin.username
        form.first_name.data = admin.first_name
        form.last_name.data = admin.last_name
        form.email.data = admin.email

        form.about_details.data = admin.about_detail
        form.about_heading.data = admin.about_heading

        form.site_dominant_color.data = admin.site_dominant_color
        form.site_accent_color.data = admin.site_accent_color

    if form.validate_on_submit():
        admin = db.session.query(Administrator).get(1)
        admin.first_name = form.first_name.data
        admin.last_name = form.last_name.data
        admin.email = form.email.data

        admin.about_detail = form.about_details.data
        admin.about_heading = form.about_heading.data

        admin.site_dominant_color = form.site_dominant_color.data
        admin.site_accent_color = form.site_accent_color.data
        db.session.add(admin)
        db.session.commit()

        message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>Settings saved</div>')
        flash(message)
        return redirect(url_for('admin_settings'))
    return render_template('admin/settings.html', form=form)
#region Delete Ops
@login_required
@app.route('/admin/delete/user/<username>')
def delete_user(username):
    user = db.session.query(User).filter_by(username = username).first_or_404()
    message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>User <strong>{}</strong> deleted</div>'.format(username))
    db.session.delete(user)
    db.session.commit()
    flash(message)
    return redirect(url_for('admin_users'))

@login_required
@app.route('/admin/delete/track/<track>')
def delete_track(track):
    track = db.session.query(Audio).filter_by(name=track).first_or_404()
    message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>Track <strong>{}</strong> deleted</div>'.format(track.name))
    os.remove(os.path.join(app.config['AUDIO'], track.album_art))
    os.remove(os.path.join(app.config['AUDIO'], track.file))

    db.session.delete(track)
    db.session.commit()
    flash(message)
    return redirect(url_for('admin_audio'))

@login_required
@app.route('/admin/delete/post/<title>')
def delete_post(title):
    post = db.session.query(Post).filter_by(title=title).first_or_404()
    message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>Post <strong>{}</strong> deleted</div>'.format(post.title))
    if post.featured_image:
        os.remove(os.path.join(app.config['POSTS'], post.featured_image))
    db.session.delete(post)
    db.session.commit()
    flash(message)
    return redirect(url_for('admin_posts'))

@login_required
@app.route('/admin/delete/show/<title>')
def delete_show(title):
    show = db.session.query(Show).filter_by(title=title).first_or_404()
    message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>Show <strong>{}</strong> deleted</div>'.format(show.title))
    if show.featured_image:
        os.remove(os.path.join(app.config['POSTS'], show.featured_image))
    
    db.session.delete(show)
    db.session.commit()
    flash(message)
    return redirect(url_for('admin_shows'))

@login_required
@app.route('/admin/delete/photo/<name>')
def delete_photo(name):
    photo = db.session.query(Photo).filter_by(name=name).first_or_404()
    message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>Photo <strong>{}</strong> deleted</div>'.format(photo.name))
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], photo.file))
    db.session.delete(photo)
    db.session.commit()
    flash(message)
    return redirect(url_for('admin_photos'))

@app.route('/admin/delete/contact/<id>')
def delete_contact(id):
    contact = db.session.query(Contact).filter_by(id=id).first_or_404()
    message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>Contact <strong>{}</strong> deleted</div>'.format(contact.name))
    db.session.delete(contact)
    db.session.commit()
    flash(message)
    return redirect(url_for('admin_contacts'))
#endregion Delete Ops


#region Edit Ops

@app.route('/admin/edit/user/<username>', methods=accepted_methods)
@login_required
def edit_user(username):
    user = db.session.query(User).filter_by(username=username).first_or_404()
    form = EditUserForm()

    if request.method == "GET":
        form.username.data = user.username
        form.email.data = user.email
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.bio.data = user.bio
        form.facebook.data = user.facebook
        form.twitter.data = user.twitter

    if form.validate_on_submit():
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.bio = form.bio.data
        user.facebook = form.facebook.data
        user.twitter = form.twitter.data

        db.session.add(user)
        db.session.commit()
        message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button> User {} settings saved</div>'.format(user.username))
        flash(message)
        return redirect(url_for('admin_users'))
        
    return render_template('admin/user_edit.html', form=form, user=user)

@app.route('/admin/edit/show/<title>', methods=accepted_methods)
@login_required
def edit_show(title):
    show = db.session.query(Show).filter_by(title=title).first_or_404()
    form = EditShowForm()

    if request.method == "GET":
        form.title.data = show.title
        form.timestamp.data = show.timestamp
        form.details.data = show.details
        form.location.data = show.location
        form.url.data = show.url

    if form.validate_on_submit():
        show.title = form.title.data
        if form.timestamp.data is not None:
            show.timestamp = form.timestamp.data
        show.details = form.details.data
        show.location = form.location.data
        show.url = form.url.data

        db.session.add(show)
        db.session.commit()
        message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>Show {} updated.</div>'.format(show.title))
        flash(message)
        return redirect(url_for('admin_shows'))
    return render_template('admin/show_edit.html', form=form, show=show)

@app.route('/admin/edit/contact/<id>', methods=accepted_methods)
@login_required
def edit_contact(id):
    contact = db.session.query(Contact).filter_by(id=id).first_or_404()
    form = EditContactForm()

    if request.method == "GET":
        form.name.data = contact.name
        form.phone.data = contact.phone
        form.email.data = contact.email


    if form.validate_on_submit():
        contact.name = form.name.data
        contact.phone = form.phone.data
        contact.email   = form.email.data

        db.session.add(contact)
        db.session.commit()
        message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>Contact {} updated.</div>'.format(contact.name))
        flash(message)
        return redirect(request.url)

    return render_template('admin/contact_edit.html', form=form, contact=contact)


@app.route('/admin/edit/audio/<name>', methods=accepted_methods)
@login_required
def edit_track(name):
    track = db.session.query(Audio).filter_by(name=name).first_or_404()
    form = EditAudioForm()

    if request.method == "GET":
        form.name.data = track.name

    if form.validate_on_submit():
        track.name = form.name.data
        if form.file.data is not None:
            track.file = upload_file('file', type='AUDIO') 
        if form.album_art.data is not None:
            track.album_art = upload_file('album_art', type='AUDIO')

       

        db.session.add(track)
        db.session.commit()
        message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>Audio track {} updated.</div>'.format(track.name))
        flash(message)
        return redirect(url_for('admin_audio'))

    return render_template('admin/audio_edit.html', form=form, track=track)


@app.route('/admin/edit/post/<title>', methods=accepted_methods)
@login_required
def edit_post(title):
    post = db.session.query(Post).filter_by(title=title).first_or_404()
    form = EditPostForm()

    if request.method == "GET":
        form.title.data = post.title
        form.body.data = post.body

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        if form.featured_image.data is not None:
            post.featured_image = upload_file('featured_image', type="POSTS")

        db.session.add(post)
        db.session.commit()

        message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>Post {} updated.</div>'.format(post.title))
        flash(message)

        return redirect(url_for('admin_posts'))

    return render_template('admin/post_edit.html', form=form, post=post)

@app.route('/admin/edit/photo/<name>', methods=accepted_methods)
@login_required
def edit_photo(name):
    photo = db.session.query(Photo).filter_by(name=name).first_or_404()
    form = EditPhotoForm()

    if request.method == "GET":
        form.name.data = photo.name
        form.caption.data = photo.caption

    if form.validate_on_submit():
        photo.name = form.name.data
        photo.caption = form.caption.data
        if form.file.data is not None:
            photo.file = upload_file('file')

        db.session.add(photo)
        db.session.commit()
        message = Markup('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert">&times;</button>Photo {} saved</div>'.format(photo.name))
        flash(message)
        return redirect(url_for('admin_photos'))
    return render_template('admin/photo_edit.html', form=form, photo=photo)
#endregion


#endregion