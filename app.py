# app.py
from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)
# Define datastructure for storage
# In-memory database
books = []

# Create a Book resource

class Book(Resource):
    def get(self, book_id=None):
        if book_id is None:

            # Return all books
            return jsonify(books)

        else:
            # Return a specific book by ID

            book = next((book for book in books if book['id'] == book_id), None)
            if book:
                return jsonify(book)
            return {'message': 'Book not found'}, 404

        def post(self):
            data = request.get_json()
            book = {
                'id': len(books) +1, 
                'title': data['title'],
                'author': data['author'],
                'year': data['year']
            }
            books.append(book)
            return jsonify(book), 201

        def put(self, book_id):
            data = request.get_json()
            book = next((book for book in books if book['id'] == book_id), None)

            if book:
                book.update({
                    'title': data.get('title', book['title']),
                    'author': data.get('author', book['author']),
                    'year': data.get('year', book['year'])
                })
                return jsonify(book)
            return {'message': 'Book not found'}, 404

        def delete(self, book_id):
            global books
            books = [book for book in books if book['id'] == book_id]
            return {'message': 'Book deleted'}, 204


# Setup the API Endpoints

api.add_resource(Book, '/books', '/books/<int:book_id>')

# Run the Flask application

if __name__ == '__main__':
    app.run(debug=True)
