from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
import requests
from datetime import datetime, timedelta

app = Flask("__main__")
app.secret_key = "c29ydGUuYmlvdGVjc2EuY29tL2FkbWluCg=="
app.permanent_session_lifetime= timedelta(hours=1)

BASE_URL = "http://127.0.0.1:8000/"

def validateUser(email: str, password: str):
    return email=='sysadmin@biotecsa.com' and password == 'elPaso01+'        

@app.route('/')
def root():
    return redirect(url_for("login"))


def validateUser():
    return ('user' in session)
        