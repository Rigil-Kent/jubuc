from app import app
from flask import render_template, redirect, flash, session, send_from_directory, url_for




@app.route('/')
def index():
    return render_template('index.html')