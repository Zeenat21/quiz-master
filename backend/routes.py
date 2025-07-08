from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models import db, Subject, Chapter, Quiz, Question, User, Score
from functools import wraps
from datetime import datetime, date

admin_routes = Blueprint('admin_routes', __name__, url_prefix='/api')
user_routes = Blueprint('user_routes', __name__,url_prefix='/api' )

# ---------- Helper: Admin Role Check ----------
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        # if claims.get('role') != 'admin':
        if 'admin' not in claims.get('role', []):
            return jsonify({'msg': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper
def user_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        # if claims.get('role') != 'admin':
        if 'user' not in claims.get('role', []):
            return jsonify({'msg': 'User login required'}), 403
        return fn(*args, **kwargs)
    return wrapper

# ---------------------- SUBJECTS ----------------------

@admin_routes.route('/subjects', methods=['POST'])
@admin_required
def create_subject():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({'msg': 'Subject name required'}), 400

    if Subject.query.filter_by(name=name).first():
        return jsonify({'msg': 'Subject already exists'}), 400

    subject = Subject(name=name, description=description)
    db.session.add(subject)
    db.session.commit()

    return jsonify({'msg': 'Subject created successfully', 'id': subject.id}), 201

@admin_routes.route('/subjects/<int:subject_id>', methods=['PUT'])
@admin_required
def update_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    data = request.get_json()
    subject.name = data.get('name', subject.name)
    subject.description = data.get('description', subject.description)

    db.session.commit()
    return jsonify({'msg': 'Subject updated successfully'})

@admin_routes.route('/subjects/<int:subject_id>', methods=['DELETE'])
@admin_required
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    return jsonify({'msg': 'Subject deleted successfully'})

# ---------------------- CHAPTERS ----------------------
# verify whether a legitamate subject is being passed
@admin_routes.route('/chapters', methods=['POST'])
@admin_required
def create_chapter():
    data = request.get_json()
    subject_id = data.get('subject_id')
    name = data.get('name')
    description = data.get('description')

    if not subject_id or not name:
        return jsonify({'msg': 'Subject ID and chapter name required'}), 400

    chapter = Chapter(subject_id=subject_id, name=name, description=description)
    db.session.add(chapter)
    db.session.commit()

    return jsonify({'msg': 'Chapter created successfully', 'id': chapter.id}), 201

@admin_routes.route('/chapters/<int:chapter_id>', methods=['PUT'])
@admin_required
def update_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    data = request.get_json()
    chapter.name = data.get('name', chapter.name)
    chapter.description = data.get('description', chapter.description)
    db.session.commit()

    return jsonify({'msg': 'Chapter updated successfully'})

@admin_routes.route('/chapters/<int:chapter_id>', methods=['DELETE'])
@admin_required
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    return jsonify({'msg': 'Chapter deleted successfully'})

# ---------------------- QUIZZES ----------------------

@admin_routes.route('/quizzes', methods=['POST'])
@admin_required
def create_quiz():
    data = request.get_json()
    chapter_id = data.get('chapter_id')
    title = data.get('title')
    date_of_quiz = data.get('date_of_quiz')
    time_duration = data.get('time_duration')
    remarks = data.get('remarks')

    quiz = Quiz(
        chapter_id=chapter_id,
        title=title,
        date_of_quiz=datetime.strptime(date_of_quiz, "%Y-%m-%d").date() if date_of_quiz else None,
        time_duration=time_duration,
        remarks=remarks
    )
    db.session.add(quiz)
    db.session.commit()
    return jsonify({'msg': 'Quiz created successfully', 'id': quiz.id}), 201

@admin_routes.route('/quizzes/<int:quiz_id>', methods=['PUT'])
@admin_required
def update_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json()
    quiz.title = data.get('title', quiz.title)
    quiz.date_of_quiz = datetime.strptime(data.get('date_of_quiz'), "%Y-%m-%d").date() if data.get('date_of_quiz') else quiz.date_of_quiz
    quiz.time_duration = data.get('time_duration', quiz.time_duration)
    quiz.remarks = data.get('remarks', quiz.remarks)

    db.session.commit()
    return jsonify({'msg': 'Quiz updated successfully'})

@admin_routes.route('/quizzes/<int:quiz_id>', methods=['DELETE'])
@admin_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return jsonify({'msg': 'Quiz deleted successfully'})

# ---------------------- QUESTIONS ----------------------

@admin_routes.route('/questions', methods=['POST'])
@admin_required
def create_question():
    data = request.get_json()
    question = Question(
        quiz_id=data['quiz_id'],
        question_statement=data['question_statement'],
        option1=data['option1'],
        option2=data['option2'],
        option3=data['option3'],
        option4=data['option4'],
        correct_option=data['correct_option']
    )
    db.session.add(question)
    db.session.commit()
    return jsonify({'msg': 'Question added successfully', 'id': question.id}), 201

@admin_routes.route('/questions/<int:question_id>', methods=['PUT'])
@admin_required
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    data = request.get_json()
    question.question_statement = data.get('question_statement', question.question_statement)
    question.option1 = data.get('option1', question.option1)
    question.option2 = data.get('option2', question.option2)
    question.option3 = data.get('option3', question.option3)
    question.option4 = data.get('option4', question.option4)
    question.correct_option = data.get('correct_option', question.correct_option)
    db.session.commit()
    return jsonify({'msg': 'Question updated successfully'})

@admin_routes.route('/questions/<int:question_id>', methods=['DELETE'])
@admin_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({'msg': 'Question deleted successfully'})

# ---------------------- SEARCH ----------------------

@admin_routes.route('/search/users', methods=['GET'])
@admin_required
def search_users():
    keyword = request.args.get('q', '')
    users = User.query.filter(User.email.ilike(f'%{keyword}%')).all()
    return jsonify([
        {
            'id': u.id,
            'email': u.email,
            'full_name': u.full_name,
            'qualification': u.qualification,
            'last_seen': u.last_seen,
            'active': u.active,
            'roles': [{'name': r.name} for r in u.roles]
        } for u in users
    ])
    # return jsonify([{'id': u.id, 'name': u.full_name, 'email': u.email} for u in users])

@admin_routes.route('/search/subjects', methods=['GET'])
@admin_required
def search_subjects():
    keyword = request.args.get('q', '')
    subjects = Subject.query.filter(Subject.name.ilike(f'%{keyword}%')).all()
    return jsonify([{'id': s.id, 'name': s.name, 'description': s.description} for s in subjects])

@admin_routes.route('/search/quizzes', methods=['GET'])
@admin_required
def search_quizzes():
    keyword = request.args.get('q', '')
    quizzes = Quiz.query.filter(Quiz.title.ilike(f'%{keyword}%')).all()
    return jsonify([{'id': q.id, 'title': q.title, 'date_of_quiz':q.date_of_quiz, 'time_duration':q.time_duration } for q in quizzes])


# ----- ROUTES as per UI -------
@admin_routes.route('/subjects/with-details', methods=['GET'])
@admin_required
def get_subjects_with_chapters_and_quizzes():
    subjects = Subject.query.all()
    result = []

    for subject in subjects:
        subject_data = {
            "id": subject.id,
            "name": subject.name,
            "description": subject.description,
            "chapters": []
        }

        for chapter in subject.chapters:
            chapter_data = {
                "id": chapter.id,
                "name": chapter.name,
                "description": chapter.description,
                "quiz_count": len(chapter.quizzes)
            }
            subject_data["chapters"].append(chapter_data)

        result.append(subject_data)

    return jsonify(result), 200

@admin_routes.route('/quizzes/with-details', methods=['GET'])
@admin_required
def get_quizzes_with_details():
    quizzes = Quiz.query.all()

    quiz_list = []
    for quiz in quizzes:
        quiz_data = {
            'id': quiz.id,
            'title': quiz.title,
            'chapter_id': quiz.chapter_id,
            'date_of_quiz': quiz.date_of_quiz.strftime('%Y-%m-%d') if quiz.date_of_quiz else None,
            'time_duration': quiz.time_duration,
            'remarks': quiz.remarks,
            'questions': []
        }

        for q in quiz.questions:
            quiz_data['questions'].append({
                'id': q.id,
                'question_statement': q.question_statement,
                'option1': q.option1,
                'option2': q.option2,
                'option3': q.option3,
                'option4': q.option4,
                'correct_option': q.correct_option
            })

        quiz_list.append(quiz_data)

    return jsonify(quiz_list), 200

@admin_routes.route('/manage-users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([
        {
            'id': u.id,
            'email': u.email,
            'full_name': u.full_name,
            'qualification': u.qualification,
            'last_seen': u.last_seen,
            'active': u.active,
            'roles': [{'name': r.name} for r in u.roles]
        } for u in users
    ])

@admin_routes.route('/manage-users/<int:user_id>/toggle-active', methods=['PUT'])
@admin_required
def toggle_user_active(user_id):
    user = User.query.get_or_404(user_id)
    user.active = not user.active
    db.session.commit()
    return jsonify({'msg': 'User status updated'})

@admin_routes.route('/manage-users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': 'User deleted'})

##### Routes for User ##### --------------------------------------
@user_routes.route('/user/upcoming-quizzes', methods=['GET'])
@user_required
def get_upcoming_quizzes():
    today = date.today()

    quizzes = (
        db.session.query(Quiz)
        .join(Chapter)
        .join(Subject)
        .filter(Quiz.date_of_quiz >= today)
        .all()
    )

    data = []
    for quiz in quizzes:
        data.append({
            'id': quiz.id,
            'title': quiz.title,
            'chapter': quiz.chapter.name,
            'subject': quiz.chapter.subject.name,
            'question_count': len(quiz.questions),
            'date_of_quiz': quiz.date_of_quiz.isoformat(),
            'time_duration': quiz.time_duration,
        })

    return jsonify(data), 200

### need to test the route below
@user_routes.route('/user/scores', methods=['GET'])
@user_required
def get_user_scores():
    user_id = int(get_jwt_identity()) #will this work?
    scores = Score.query.filter_by(user_id=user_id).order_by(Score.timestamp.desc()).all()

    results = []
    for score in scores:
        results.append({
            "id": score.id,
            "quiz": {
                "id": score.quiz.id,
                "title": score.quiz.title
            },
            "timestamp": score.timestamp.isoformat(),
            "total_score": score.total_score,
            "percentage": score.percentage,
            "correct_answers": score.correct_answers,
            "total_questions": score.total_questions
        })

    return jsonify(results), 200