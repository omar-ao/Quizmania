#!/usr/bin/python3
"""
Renders home page
"""

from flask import Blueprint, jsonify, render_template, request
import requests
from flask_login import current_user, login_required

home = Blueprint('home', __name__)

categories = {
    'General Knowledge' : '9',
    'Entertainment: Books': '10',
    'Entertainment: Film': '11',
    'Entertainment: Music' : '12',
    'Entertainment: Musicals & Theatres': '13',
    'Entertainment: Television': '14',
    'Entertainment: Video Games' : '15',
    'Entertainment: Board Games': '16',
    'Science & Nature' : '17',
    'Science: Computers': '18',
    'Science: Mathematics': '19',
    'Mythology' : '20',
    'Sports': '21',
    'Geography': '22',
    'History': '23',
    'Politics': '24',
    'Art' : '25',
    'Celebrities': '26',
    'Animals': '27',
    'Vehicles': '28',
    'Entertainment: Comics': '29',
    'Science: Gadgets': '30',
    'Entertainment: Japanese Anime & Manga' : '31',
    'Entertainment: Cartoon & Animations': '32',
}

colors = [
    "#1a1a2e", "#16213e", "#0f3460", "#53354a", "#2e294e",
    "#1f4068", "#2b2e4a", "#3a506b", "#1c2541", "#344955",
    "#212121", "#1e1e24", "#202040", "#323232", "#2c3e50",
    "#1b263b", "#2d4059", "#1c1c1c", "#283149", "#2d2d34",
    "#232931", "#293462", "#1d1e33", "#222831", "#232323"
]


@home.route('/', methods=['GET'])
@login_required
def index():
    """Renders index page"""
    return render_template('/home_page.html', categories=categories,
                           colors=colors)

@home.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    """Generates quiz based on the category selected"""
    category = request.form.get('category')
    difficulty = request.form.get('difficulty')
    quiz_type = request.form.get('quiz_type')

    params = ""
    if difficulty != "Any":
        params = "&difficulty={}".format(difficulty.lower())

    if quiz_type != "Any":
        params = params + "&type={}".format(quiz_type)

    url = "https://opentdb.com/api.php?amount=10&category={}{}".format(
            categories.get(category), params)

    response = requests.get(url=url)
    
    if response.status_code == 200:
        questions = response.json()['results']
        return jsonify({'questions': questions})
    else:
        return jsonify({'error': 'Failed to fetch questions'}), 500
