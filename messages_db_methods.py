import sqlite3
import os
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "chat.sqlite")

# For this, I will need a new table in the database to track messages being sent and chats opened.
# This will be one giant table containing all messages between users. The columns are as follows:
    # username1 <-> username2 : where username1 is the user whose username comes first in abc-order
    # from : a username dictating who sent the message
    # timeStamp : the DATETIME of the message being sent
    # content : content of the message -- either a link or text
    # format : a string whether content is TEXT, IMAGE, or VIDEO
    # imageWidth : metadata for the width of an image, else null
    # imageHeight : metadata for the height of an image, else null
    # videoLength : metadata for the length of a video, else null
    # videoSource : metadata for the source of video, else null

# enum is for specifying the format of content
class Format(Enum):
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'
    VIDEO = 'VIDEO'
    LINK = 'LINK'

def insert_row_in_messages_db(users, sender, content, format, image_width=None, image_height=None,
                     video_length=None, video_source=None):
    """
    Creates a row in chat.sqlite's messages table
    """
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO messages (users, sender, content, format, imageWidth, 
                     imageHeight, videoLength, videoSource) VALUES (?, ?, ?, ?, ?, ?, ?, ?);''',
                  (users, sender, content, format, image_width, image_height, video_length, video_source))

