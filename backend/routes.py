from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models import db, Subject, Chapter, Quiz, Question, User, Score, roles_users, Role
from functools import wraps
from datetime import datetime, date
from sqlalchemy import func, text, extract
from werkzeug.security import generate_password_hash, check_password_hash

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
    user_id = int(get_jwt_identity())
    # Get quiz IDs the user already attempted
    attempted_quiz_ids = db.session.query(Score.quiz_id).filter_by(user_id=user_id)

    quizzes = (
        db.session.query(Quiz)
        .join(Chapter)
        .join(Subject)
        .filter(Quiz.date_of_quiz >= today)
        .filter(~Quiz.id.in_(attempted_quiz_ids))
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

### need to test the route below - works!
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


# ----admin summary routes------
@admin_routes.route('admin-summary/subject-quiz-attempts', methods=['GET'])
@admin_required
def subject_quiz_attempts():
    results = db.session.query(
        Subject.name.label("subject"),
        func.count(Score.id).label("total_attempts"),
        func.count(func.distinct(Score.user_id)).label("unique_users")
    ).join(Subject.chapters).join(Chapter.quizzes).join(Quiz.scores) \
     .group_by(Subject.id).all()

    return jsonify([dict(row._asdict()) for row in results])


@admin_routes.route('admin-summary/top-scores-per-subject', methods=['GET'])
@admin_required
def top_scores_per_subject():
    results = db.session.execute(text("""
        SELECT s.id, s.name AS subject, MAX(sc.total_score) AS max_score
        FROM subject s
        LEFT JOIN chapter c ON s.id = c.subject_id
        LEFT JOIN quiz q ON c.id = q.chapter_id
        LEFT JOIN score sc ON q.id = sc.quiz_id
        GROUP BY s.id, s.name
    """)).fetchall()

    return jsonify([dict(row._mapping) for row in results])



##filter out the admin result
@admin_routes.route('admin-summary/user-activity', methods=['GET'])
@admin_required
def user_activity():
    # Subquery: Get all user IDs with the admin role
    admin_user_ids = db.session.query(roles_users.c.user_id) \
        .join(Role, roles_users.c.role_id == Role.id) \
        .filter(Role.name == 'admin')

    # Main query: Exclude those users
    results = db.session.query(
        User.full_name.label("user"),
        func.count(Score.id).label("total_attempts"),
        func.max(Score.timestamp).label("last_attempt")
    ).outerjoin(User.scores) \
     .filter(~User.id.in_(admin_user_ids)) \
     .group_by(User.id) \
     .all()

    return jsonify([dict(row._asdict()) for row in results])





# ROUTES FOR USER

@user_routes.route('/user/profile', methods=['GET'])
@user_required
def get_user_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)

    return jsonify({
        "email": user.email,
        "full_name": user.full_name,
        "qualification": user.qualification,
        "dob": user.dob.isoformat() if user.dob else None
    }), 200

@user_routes.route('/user/profile', methods=['PUT'])
@user_required
def update_user_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    user.full_name = data.get('full_name', user.full_name)
    user.qualification = data.get('qualification', user.qualification)
    dob_str = data.get('dob')
    if dob_str:
        user.dob = datetime.strptime(dob_str, "%Y-%m-%d").date()

    if data.get("password"):
        user.password = generate_password_hash(data["password"])

    db.session.commit()
    return jsonify({"msg": "Profile updated successfully"}), 200


### quiz attempt routes

@user_routes.route('/user/quiz/<int:quiz_id>/questions', methods=['GET'])
@user_required
def get_quiz_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    questions = [{
        "id": q.id,
        "question_statement": q.question_statement,
        "option1": q.option1,
        "option2": q.option2,
        "option3": q.option3,
        "option4": q.option4,
    } for q in quiz.questions]

    return jsonify({
        "quiz_id": quiz.id,
        "title": quiz.title,
        "duration_minutes": quiz.time_duration,
        "questions": questions
    })

@user_routes.route('/user/quiz/<int:quiz_id>/submit', methods=['POST'])
@user_required
def submit_quiz(quiz_id):
    user_id = int(get_jwt_identity())
    quiz = Quiz.query.get_or_404(quiz_id)

    data = request.get_json()
    answers = data.get("answers", [])

    if not isinstance(answers, list) or len(answers) == 0:
        return jsonify({"msg": "Invalid answer data."}), 400

    question_lookup = {q.id: q for q in quiz.questions}

    correct_count = 0
    for item in answers:
        q_id = item.get("question_id")
        selected = item.get("selected_option")

        question = question_lookup.get(q_id)
        if question and question.correct_option == selected:
            correct_count += 1

    total_questions = len(quiz.questions)
    percentage = (correct_count / total_questions) * 100
    total_score = correct_count * (100 / total_questions)  # adjust if you use weighted scoring

    # Save score to DB
    score_entry = Score(
        quiz_id=quiz.id,
        user_id=user_id,
        timestamp=datetime.utcnow(),
        total_score=total_score,
        percentage=percentage,
        correct_answers=correct_count,
        total_questions=total_questions
    )
    db.session.add(score_entry)
    db.session.commit()

    return jsonify({
        "msg": "Quiz submitted successfully.",
        "total_score": total_score,
        "percentage": percentage,
        "correct_answers": correct_count,
        "total_questions": total_questions
    }), 200


### User summary routes! ###
@user_routes.route('/user/summary/total-attempts', methods=['GET'])
@user_required
def total_attempts():
    user_id = int(get_jwt_identity())
    total = Score.query.filter_by(user_id=user_id).count()
    return jsonify({'total_quizzes_attempted': total})

@user_routes.route('/user/summary/subject-attempts', methods=['GET'])
@user_required
def subject_attempts():
    user_id = int(get_jwt_identity())
    results = db.session.query(
        Subject.name.label('subject'),
        db.func.count(Score.id).label('attempts')
    ).join(Chapter, Chapter.subject_id == Subject.id
    ).join(Quiz, Quiz.chapter_id == Chapter.id
    ).join(Score, Score.quiz_id == Quiz.id
    ).filter(Score.user_id == user_id
    ).group_by(Subject.name).all()

    response = [{'subject': r.subject, 'attempts': r.attempts} for r in results]
    return jsonify(response)

@user_routes.route('/user/summary/monthly-attempts', methods=['GET'])
@user_required
def monthly_attempts():
    user_id = int(get_jwt_identity())
    results = db.session.query(
        extract('year', Score.timestamp).label('year'),
        extract('month', Score.timestamp).label('month'),
        db.func.count(Score.id).label('attempts')
    ).filter(Score.user_id == user_id
    ).group_by('year', 'month').order_by('year', 'month').all()

    response = [
        {
            'month': f"{int(r.month):02}/{int(r.year)}",
            'attempts': r.attempts
        }
        for r in results
    ]
    return jsonify(response)

@user_routes.route('/user/summary/avg-score', methods=['GET'])
@user_required
def average_score():
    user_id = int(get_jwt_identity())

    result = db.session.query(
        db.func.avg(Score.total_score).label('average_score')
    ).filter(Score.user_id == user_id).first()

    average_score = round(result.average_score or 0, 2)  # Defaults to 0 if None

    return jsonify({'average_score': average_score})
