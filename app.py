from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

try:
    # ทดลองเชื่อมต่อฐานข้อมูล
    db.session.query(text("1")).all()
    print("เชื่อมต่อฐานข้อมูลสำเร็จ")
except Exception as e:
    print("มีข้อผิดพลาดในการเชื่อมต่อฐานข้อมูล:", e)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        new_task = Todo(content=content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print("มีข้อผิดพลาดในการเพิ่มงานใหม่:", e)
            return 'มีข้อผิดพลาดในการเพิ่มงานใหม่'
        
    else:
        tasks = Todo.query.all()
        # tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    delete_task = Todo.query.get_or_404(id)

    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print("มีข้อผิดพลาดในการลบงาน:", e)
        return 'มีข้อผิดพลาดในการลบงาน'
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print("มีข้อผิดพลาดในการอัพเดตงาน:", e)
            return 'มีข้อผิดพลาดในการอัพเดตงาน'

    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)