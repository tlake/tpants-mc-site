"""
A tiny Flask app for Minecraft servers.

Displays server status as well as client configuration and connection
information.
"""

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


################################
# APP SETTINGS
################################

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY="man, who knows?",
    SQLALCHEMY_DATABASE_URI="postgresql://flask:dew_it@localhost/mcdb"
)


################################
# DATABASE SETTINGS & MODELS
################################

db = SQLAlchemy(app)


class Server(db.Model):
    """Server model."""

    id = db.Column(db.Integer, primary_key=True)
    server_address = db.Column(db.String(16))
    server_port = db.Column(db.String(8))
    client_config = db.Column(db.Text)
    created = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
    )

db.create_all()
db.session.commit()


################################
# ADMIN SETTINGS & VIEWS
################################

admin = Admin(app)
admin.add_view(ModelView(Server, db.session))


################################
# APP VIEWS
################################

@app.route("/")
def index():
    """Index (and only) page of site."""
    servers = {"testkey": "testvalue"}
    return render_template("index.html", servers=servers)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
