from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = '87.98.230.253' 
app.config['MYSQL_USER'] = 'hlbtnjwi_admin3'
app.config['MYSQL_PASSWORD'] = 'contrapass33'
app.config['MYSQL_DB'] = 'hlbtnjwi_restaurant'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts = data)

@app.route('/request')
def Req():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    cur.close()
    return render_template('request.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        cliente = request.form['cliente']
        platillo = request.form['platillo']
        mesa = request.form['mesa']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (cliente, platillo, mesa) VALUES (%s,%s,%s)", (cliente, platillo, mesa))
        mysql.connection.commit()
        flash('Contact Added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        cliente = request.form['cliente']
        platillo = request.form['platillo']
        mesa = request.form['mesa']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET cliente = %s,
                mesa = %s,
                platillo = %s
            WHERE id = %s
        """, (cliente, mesa, platillo, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Req'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
