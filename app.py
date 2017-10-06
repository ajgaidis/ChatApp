from flask import Flask, render_template, request, session, redirect, url_for, Request
from forms import SignupForm, LoginForm
from users_db_methods import *
from messages_db_methods import *
from flask_socketio import SocketIO, send, emit, join_room, leave_room, rooms, Namespace
import re

app = Flask(__name__)
app.secret_key = "got that good good dev key"
socketio = SocketIO(app)


################################
## CREATE AND LOG IN/OUT A USER
################################


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Logs a user into the chat and records the login

    :return:
    """
    if 'username' in session:  # ensure user can't see signup if logged in
        return redirect(url_for('home'))

    form = LoginForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form)
        else:
            username = form.username.data
            password = form.password.data
            uid = get_uid_from_username(username)

            if uid is not None and check_password(uid, password):
                session['username'] = username  # initialize a session cookie
                set_lastlogin(uid)  # record login time in database
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Signs a user up for an account so that they may log in

    :return:
    """
    if 'username' in session:  # ensure user can't see signup if logged in
        return redirect(url_for('home'))

    form = SignupForm()

    if request.method == 'POST':
        if not form.validate(): # ensure that a user enters all fields correctly
            return render_template('signup.html', form=form)
        else:
            username = form.username.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            insert_row_in_users_db(username, first_name, last_name, email, password)

            session['username'] = username  # initialize a session cookie
            return redirect(url_for('home'))

    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@app.route('/logout')
def logout():
    """
    Logs a user out of the chat and records logout

    :return:
    """
    session.pop('username', None)  # remove session cookie
    return redirect(url_for('index'))


@app.route('/index')
def index():
    """
    Gets the main index page of the chat site!

    :return:
    """
    render_template('index.html')

@app.route('/home')
def home():
    """
    Gets the home page of the chat site!

    :return:
    """
    if 'username' not in session:  # ensure user can't see home if not logged in
        return redirect(url_for('login'))

    return render_template("home.html")


###################
## MESSAGE SENDING
###################

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:  # ensure user is logged in
        return redirect(url_for('login'))

    if request.method == 'POST':
        return redirect(url_for('chat'))

    elif request.method == 'GET':
        return render_template('chat.html')

@socketio.on('message')
def handle_message(msg):
    sender = session['username']
    recipient = msg['recipient']
    users = concat_usernames(sender, recipient)
    message = msg['message']
    format = str(is_text_image_video(message))

    insert_row_in_messages_db(users, sender, message, format)

    # TODO : Add hard coding for metadata
    msg['sender'] = sender
    join_room(users)
    send(msg, room=users)

def concat_usernames(username1, username2):
    """ Returns the concatenation input strings in the form "username1 <-> username2 """
    usernames_sorted = sorted([username1, username2])
    return usernames_sorted[0] + " <-> " + usernames_sorted[1]

def is_text_image_video(msg):
    """ Returns whether the input message is of enum type TEXT, VIDEO, or IMAGE """

    # Regex taken from gruber's github @ https://gist.github.com/gruber/8891611
    url = re.match("""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:
com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel
|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj
|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de
|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp
|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki
|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq
|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn
|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv
|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi
|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]
+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)
[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|
mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|
ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr
|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf
|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm
|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml
|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph
|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss
|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve
|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))""", msg)
    print(url)
    if url is None:
        return Format.TEXT
    elif re.match("""((.png)|(.jpg)|(.tiff)|(.gif)|(.bmp)|(.exif)|(.svg)|(.bpg)|(.bat)|(.ppm)|(.pgm)|(.pbm))""", url):
        return Format.IMAGE
    elif re.match("""((youtube.com)|(vevo.com)|(vimeo.com)|(dailymotion.com)|(twitch.com)|(metacafe.com))""", url):
        return Format.VIDEO
    else: # if there is url but isn't a video or image
        return Format.LINK


####################
## MESSAGE FETCHING
####################

# For this, I will need to extract messages from the database model identified in the previous
#  section and deliver them.



if __name__ == '__main__':
    socketio.run(app, debug = True, port = 8000)  # start server