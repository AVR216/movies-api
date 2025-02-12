from flask import Blueprint, jsonify, request
from models.MovieModel import MovieModel
from models.entities.Movie import Movie
from utils.uuid.UUIDFormat import UUIDFormat
from utils.dates.DateFormat import DateFormat

main = Blueprint('movie_blueprint', __name__)

@main.route('/')
def get_movies():
    try:
        movies = MovieModel.get_movies()
        return jsonify(movies), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/<id>')
def find_movie(id):
    try:
        valid_uuid(id)
        movie = MovieModel.find_movie(id)
        if movie != None:
            return jsonify(movie), 200
        else:
           return jsonify({"message": f'Movie with id: {id} not found'}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

@main.route('/', methods=['POST'])    
def register_movie():
    try:
        title = request.json['title']
        duration = request.json['duration']
        released = request.json['released']
        movie_to_register = Movie(id=None, title=title, duration = duration, released = DateFormat.from_string(released))
        rows_affected = MovieModel.add_movie(movie_to_register)
        return jsonify({"Inserted-records": rows_affected})
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/<id>', methods=['DELETE'])    
def remove_movie(id):
    try:
        valid_uuid(id)
        rows_affected = MovieModel.delete(id)
        return jsonify({"Deleted-records": rows_affected})
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/<id>', methods=['PUT'])    
def update_movie(id):
    try:
        valid_uuid(id)
        tit = request.json['title']
        dur = int(request.json['duration'])
        rel = request.json['released']
        movie = Movie(id=None, title=tit, duration=dur, released=DateFormat.from_string(rel))
        affected_rows = MovieModel.update(movie=movie, movie_id=id)
        if affected_rows > 0 :
            return jsonify({"message": "movie updated successfully"}), 200
        else :
            return jsonify({"message": "Movie not updated"}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


def valid_uuid(value):
    is_valid = UUIDFormat.is_valid_uuid(value)
    if not is_valid:
        raise ValueError("Invalid movie ID")