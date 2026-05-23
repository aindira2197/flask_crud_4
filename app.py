from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'

db = SQLAlchemy(app)


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)


@app.route('/')
def index():

    notes = Note.query.all()

    return render_template(
        'index.html',
        notes=notes
    )


@app.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'POST':

        title = request.form.get('title')
        content = request.form.get('content')

        note = Note(
            title=title,
            content=content
        )

        db.session.add(note)
        db.session.commit()

        return redirect('/')

    return render_template('create.html')


if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)
