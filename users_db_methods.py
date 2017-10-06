import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "chat.sqlite")

def insert_row_in_users_db(username, firstname, lastname, email, password):
    """
    Creates a row in chat.sqlite's users table

    :param uid: a string, the unique identifier of the user
    :param username: a string, the user's chosen username
    :param firstname: a string, the first name of the user
    :param lastname: a string, the last name of the user
    :param email: a string, the email of the user
    :param password: a string, the plaintext password of the user
    """
    uid = uuid4().hex
    pwd_hash = generate_password_hash(password)
    login_time = set_lastlogin(uid)
    row_data = (uid, username, firstname, lastname, email, pwd_hash, login_time)

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO users (uid, username, firstname, lastname, email, passwordhash, 
                      lastlogin) VALUES (?, ?, ?, ?, ?, ?, ?);''', row_data)


def get_uid_from_username(username):
    """
        Gets a user's uid from the table given a username

        :param uid: a string, the unique username of the user
        :return: a string, the unique id of the user. Else,
                 returns None if unable to extract username from database
        """
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT uid FROM users WHERE username=?;', (username,))
        result = c.fetchone()
        if result is None:
            return None
        return result[0]

def get_username(uid):
    """
    Gets a user's username from the table given a uid

    :param uid: a string, the unique identifier of the user
    :return: a string, the unique username of the user. Else,
             returns None if unable to extract username from database
    """
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT username FROM users WHERE uid=?;', (uid,))
        result = c.fetchone()
        if result is None:
            return None
        return result[0]

def get_firstname(uid):
    """
    Gets a user's first name from the table given a uid

    :param uid: a string, the unique identifier of the user
    :return: a string, the first name of the user. Else, returns
             None if unable to extract first name from database
    """
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT firstname FROM users WHERE uid=?;', (uid,))
        result = c.fetchone()
        if result is None:
            return None
        return result[0]

def get_lastname(uid):
    """
    Gets a user's last name from the table given a uid

    :param uid: a string, the unique identifier of the user
    :return: a string, the last name of the user. Else, returns
             None if unable to extract last name from database
    """
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT lastname FROM users WHERE uid=?;', (uid,))
        result = c.fetchone()
        if result is None:
            return None
        return result[0]

def get_email(uid):
    """
    Gets a user's email address from the table given a uid

    :param uid: a string, the unique identifier of the user
    :return: a string, the email of the user. Else, returns
             None if unable to extract email from database
    """
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT email FROM users WHERE uid=?;', (uid,))
        result = c.fetchone()
        if result is None:
            return None
        return result[0]

def get_password(uid):
    """
    Gets a user's last name from the table given a uid

    :param uid: a string, the unique identifier of the user
    :return: a string, the password hash of the user. Else, returns
             None if unable to extract password from database
    """
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT passwordhash FROM users WHERE uid=?;', (uid,))
        result = c.fetchone()
        if result is None:
            return None
        return result[0]

def check_password(uid, password):
    """
    Checks if a users password matches the inputted, plaintext one

    :param uid: a string, the unique id of the user
    :param password: a string, the plaintext password of the user
    :return: a boolean, true if the passwords match
    """
    pwd_hash = get_password(uid)
    return check_password_hash(pwd_hash, password)

def get_lastlogin(uid):
    """
    Gets a user's last login time from the table given a uid

    :param uid: a string, the unique identifier of the user
    :return: a string, the date of the user's last login. Else,
             returns None if unable to extract the date from database
    """
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT lastlogin FROM users WHERE uid=?;', (uid,))
        result = c.fetchone()
        if result is None:
            return None
        return result[0]

def get_login_time(uid):
    """
    Gets a user's last login time from the table given a uid

    :param uid: a string, the unique identifier of the user
    :return: a boolean, true if the user is logged in. Else, returns
             None if unable to extract the information from database
    """
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT loggedin FROM users WHERE uid=?;', (uid,))
        result = c.fetchone()
        if result is None:
            return None
        return result[0]

def set_lastlogin(uid):
    """
    Sets the login time of the user to be the time when the function is called

    :param uid: a string, the unique identifier of the user
    """
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("UPDATE users SET lastlogin=DATETIME('NOW') WHERE uid=?;", (uid,))