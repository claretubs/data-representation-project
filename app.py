from flask import Flask, url_for, request, redirect, abort, jsonify,render_template
import mysql.connector
import json

app = Flask(__name__, static_url_path='', static_folder='static')

class ShopDAO:
    def __init__(self, config_path='config.json'):
        self.config = self.read_config(config_path)
    
    def read_config(self, config_path):
        with open(config_path, 'r') as file:
            config = json.load(file)
        return config['Database']

    def get_cursor(self):
        connection = mysql.connector.connect(
            host=self.config['host'],
            user=self.config['user'],
            password=self.config['password'],
            database=self.config['database']
        )
        mycursor = connection.cursor()
        return mycursor, connection
    
    def close_all(self, mycursor, connection):
        connection.close()
        mycursor.close()

shop_dao = ShopDAO()
mycursor, connection = shop_dao.get_cursor()
sql= '''
    CREATE TABLE IF NOT EXISTS productdata (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        Product VARCHAR(300),
        Model VARCHAR(200),
        Price INT
    )
'''
mycursor.execute(sql)
connection.commit()
shop_dao.close_all(mycursor, connection)

# RESTful API Endpoints
# Get All
@app.route('/shoes', methods=['GET'])
def getAll():
    mycursor, connection = shop_dao.get_cursor()
    mycursor.execute('SELECT * FROM productdata')
    shoes = mycursor.fetchall()
    shop_dao.close_all(mycursor, connection)

    # Create a list of dictionaries for each shoe
    shoes_list = [{'id': shoe[0], 'Product': shoe[1], 'Model': shoe[2], 'Price': shoe[3]} for shoe in shoes]
    return jsonify({'shoes': shoes_list})

# Find by Id
@app.route('/shoes/<int:id>')
def findById(id):
    mycursor, connection = shop_dao.get_cursor()
    mycursor.execute(f'SELECT * FROM productdata WHERE id = {id}')
    shoe = mycursor.fetchone()
    shop_dao.close_all(mycursor, connection)
    if not shoe:
        return jsonify({}), 204
    return jsonify({'shoe': {'id': shoe[0], 'Product': shoe[1], 'Model': shoe[2], 'Price': shoe[3]}})

# Create
# curl -X POST -H "Content-Type: application/json" -d "{\"Product\": \"New Product\", \"Model\": \"New Model\", \"Price\": 123}" http://127.0.0.1:5000/shoes
@app.route('/shoes', methods=['POST'])
def create():
    mycursor, connection = shop_dao.get_cursor()

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
    connection.commit()

    new_shoe['id'] = mycursor.lastrowid
    shop_dao.close_all(mycursor, connection)
    return jsonify({'shoe': new_shoe}), 201

# Update
# curl -X PUT -H "Content-Type: application/json" -d "{\"Product\": \"Updated Product\", \"Model\": \"Updated Model\", \"Price\": 200}" http://127.0.0.1:5000/shoes/6
@app.route('/shoes/<int:id>', methods=['PUT'])
def update(id):
    mycursor, connection = shop_dao.get_cursor()
    mycursor.execute(f'SELECT * FROM productdata WHERE id = {id}')
    current_shoe = list(mycursor.fetchone())

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
    connection.commit()

    shop_dao.close_all(mycursor, connection)
    return jsonify({'shoe': {'id': current_shoe[0], 'Product': current_shoe[1], 'Model': current_shoe[2], 'Price': current_shoe[3]}})

# Delete
# curl -X DELETE http://127.0.0.1:5000/shoes/7
@app.route('/shoes/<int:id>', methods=['DELETE'])
def delete(id):
    mycursor, connection = shop_dao.get_cursor()
    mycursor.execute(f'SELECT * FROM productdata WHERE id = {id}')
    deleted_shoe = mycursor.fetchone()

    if not deleted_shoe:
        return jsonify({}), 404

    sql = 'DELETE FROM productdata WHERE id=%s'
    values = (id,)
    mycursor.execute(sql, values)
    connection.commit()
    
    shop_dao.close_all(mycursor, connection)
    return jsonify({"done":True})

# Route to render the product list page
@app.route('/shop')
def product_list():
    return render_template('shop.html')

if __name__ == '__main__':
    app.run(debug=True)