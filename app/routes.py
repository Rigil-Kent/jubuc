from app import app, db
from flask import render_template, redirect, flash, session, request, send_from_directory, url_for
from app.models import Administrator, User
from app.forms import AdminForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from flask import Markup
from werkzeug.urls import url_parse


#region global vars
accepted_methods = ["GET", "POST"]
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


@app.route('/index')
def alt_index():
    admin = db.session.query(Administrator).count()
    print(admin)

    if admin == 0:
        return redirect(url_for('admin_welcome'))

    return render_template('layout2/index.html')

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

#endregion