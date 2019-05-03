from app import app
from flask import render_template, redirect, flash, session, send_from_directory, url_for




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index')
def alt_index():
    return render_template('layout2/index.html')

@app.route('/photos')
def photos():
    return render_template('photos.html')



#region ADMINISTRATION
@app.route('/admin')
def admin_dashboard():
    return render_template('layout2/admin/index.html')

#endregion