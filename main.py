from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///whiteboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Whiteboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    data = request.json.get('data')
    board = Whiteboard.query.first()

    if board:
        board.data = data
    else:
        board = Whiteboard(data=data)
        db.session.add(board)
    db.session.commit()
    return jsonify(success=True)

@app.route('/load', methods=['GET'])
def load():
    board = Whiteboard.query.first()
    if board:
        return jsonify(success=True, data=board.data)
    return jsonify(success=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)