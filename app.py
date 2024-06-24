from flask import *
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'db1.db'
def connect_db():
    db=getattr(g,'_database',None)
    if db is None:
        db=g._database=sqlite3.connect(app.config['DATABASE'])
    return db

@app.route('/',methods=['GET','POST'])
def index():
    db=connect_db()
    cursor=db.cursor()
    if request.method == 'POST':
        cursor.execute('select * from products')
        data = cursor.fetchall()
        chosen_id = request.form.get('radio')
        if request.form['submit'] == 'calprofit':
            cursor.execute("select * from products where id='" + str(chosen_id) + "'")
            data2 = cursor.fetchall()
            print(data2)
            profit = (int(data2[0][4]) - int(data2[0][3])) * int(data2[0][2])
            return render_template('index.html',data=data,profit=profit)
        elif request.form['submit']=='changeprice':
            new_price=request.form.get('new_price')
            cursor.execute("update products set salesprice='"+str(new_price)+"' where id='"+str(chosen_id)+"'")
            db.commit()
            cursor.execute("select * from products")
            data = cursor.fetchall()
        return render_template('index.html',data=data)
    else:
        cursor.execute('select * from products')
        data=cursor.fetchall()
        return render_template('index.html',data=data)

if __name__ == '__main__':
    app.run()
