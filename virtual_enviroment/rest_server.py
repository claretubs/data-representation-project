from flask import Flask, url_for, request, redirect, abort, jsonify
import mysql.connector

app = Flask(__name__, static_url_path='', static_folder='staticpages')

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'root',
    database = 'shoedata'
)

mycursor = mydb.cursor()
sql= '''
    CREATE TABLE IF NOT EXISTS productdata (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Product VARCHAR(50),
        Model VARCHAR(50),
        Price INT
    )
'''
mycursor.execute(sql)
mydb.commit()

# RESTful API Endpoints
# Get All
@app.route('/shoes', methods=['GET'])
def getAll():
    mycursor.execute('SELECT * FROM productdata')
    shoes = mycursor.fetchall()
    return jsonify({'shoes': [{'id': shoes[0], 'title': shoes[1], 'description': shoes[2], 'done': shoes[3]} for shoe in shoes]})

# Find by Id
@app.route('/shoes/<int:id>')
def findById(id):
    mycursor.execute(f'SELECT * FROM productdata WHERE id = {id}')
    shoe = mycursor.fetchone()
    if not shoe:
        return jsonify({}), 204
    return jsonify({'shoe': {'id': shoe[0], 'Product': shoe[1], 'Model': shoe[2], 'Price': shoe[3]}})

# Create
#  curl -X POST http://127.0.0.1:5000/shoes
@app.route('/shoes', methods=['POST'])
def create():
    if not request.json:
        abort(400)

    new_shoe = {
        'Product': request.json['Product'],
        'Model': request.json['Model'],
        'Price': request.json['Price']
    }

    sql = 'INSERT INTO productdata (Product, Model, Price) VALUES (%s, %s, %s)'
    values = (new_shoe['Product'], new_shoe['Model'], new_shoe['Price'])

    mycursor.execute(sql, values)
    mydb.commit()

    new_shoe['id'] = mycursor.lastrowid
    return jsonify({'shoe': new_shoe}), 201

# Update
# curl -X PUT -d "{\"Price\":999}" -H "content-type:application/json" http://127.0.0.1:5000/books/1
@app.route('/shoes/<int:id>', methods=['PUT'])
def update(id):
    mycursor.execute(f'SELECT * FROM productdata WHERE id = {id}')
    current_shoe = mycursor.fetchone()

    if not current_shoe:
        return jsonify({}), 404

    if 'Product' in request.json:
        current_shoe[1] = request.json['Product']
    if 'Model' in request.json:
        current_shoe[2] = request.json['Model']
    if 'Price' in request.json:
        current_shoe[3] = request.json['Price']

    sql = 'UPDATE productdata SET Product=%s, Model=%s, Price=%s WHERE id=%s'
    values = (current_shoe[1], current_shoe[2], current_shoe[3], id)

    mycursor.execute(sql, values)
    mydb.commit()

    return jsonify({'shoe': {'id': current_shoe[0], 'Product': current_shoe[1], 'Model': current_shoe[2], 'Price': current_shoe[3]}})

# Delete
@app.route('/shoes/<int:id>', methods=['DELETE'])
def delete(id):
    mycursor.execute(f'SELECT * FROM productdata WHERE id = {id}')
    deleted_shoe = mycursor.fetchone()

    if not deleted_shoe:
        return jsonify({}), 404

    sql = 'DELETE FROM productdata WHERE id=%s'
    values = (id,)
    mycursor.execute(sql, values)
    mydb.commit()
    
    return jsonify({"done":True})

if __name__ == '__main__':
    app.run(debug=True)