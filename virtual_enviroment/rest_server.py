from flask import Flask, url_for, request, redirect, abort, jsonify

app = Flask(__name__, static_url_path='', static_folder='staticpages')

books = [
    {"id": 1, "Title":"Harry Potter", "Author":"JK", "Price":1000},
    {"id": 2, "Title":"The Mortal Instruments", "Author":"Cassandra Clare", "Price":2000},
    {"id": 3, "Title":"Cooking Book", "Author":"Clare Tubridy", "Price":1500},
]

nextId = 4

# Get All
@app.route('/books')
def getAll():
    return jsonify(books)

# Find by Id
@app.route('/books/<int:id>')
def findById(id):
    foundBooks = list(filter (lambda t : t["id"] == id, books))
    if len(foundBooks) == 0:
        return jsonify({}) , 204
    return jsonify(foundBooks[0])

# Create
#  curl -X POST http://127.0.0.1:5000/books
@app.route('/books', methods=['POST'])
def create():
    global nextId
    if not request.json:
        abort(400)

    book = {
        "id": nextId, 
        "Title":"Game Of Thrones", 
        "Author":"George R. R. Martin", 
        "Price":500
    }

    books.append(book)
    nextId += 1
    return jsonify(book)

# Update
# curl -X PUT -d "{\"Price\":999}" -H "content-type:application/json" http://127.0.0.1:5000/books/1
@app.route('/books/<int:id>', methods=['PUT'])
def update(id):
    foundBooks = list(filter(lambda t : t["id"] == id, books))
    if len(foundBooks) == 0:
        return jsonify({}), 404
    
    currentBook = foundBooks[0]
    if 'Title' in request.json:
        currentBook['Title'] = request.json['Title']
    if 'Author' in request.json:
        currentBook['Author'] = request.json['Author']
    if 'Price' in request.json:
        currentBook['Price'] = request.json['Price']

    return jsonify(currentBook)

# Delete
@app.route('/books/<int:id>', methods=['DELETE'])
def delete(id):
    foundBooks = list(filter(lambda t : t["id"] == id, books))
    if len(foundBooks) == 0:
        return jsonify({}), 404
    
    books.remove(foundBooks[0])
    return jsonify({"done":True})

if __name__ == '__main__':
    app.run(debug=True)