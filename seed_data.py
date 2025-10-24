
from app import create_app
from app.extensions import db
from app.models.role import Role
from app.models.user import User
from app.models.course import Course
from app.models.module import Module
from app.models.lesson import Lesson
from app.models.assessment import Assessment
from app.models.question import Question
from app.models.option import Option
from app.models.certification_rule import CertificationRule
from datetime import datetime, timedelta

def seed_roles():
    """Seed basic roles"""
    roles = ['Admin', 'Instructor', 'Learner']
    for role_name in roles:
        if not Role.query.filter_by(name=role_name).first():
            role = Role(name=role_name)
            db.session.add(role)
    db.session.commit()
    print("✓ Seeded roles")

def seed_users():
    """Seed demo users"""
    # Admin user
    if not User.query.filter_by(email='admin@ministrylearn.com').first():
        admin = User(email='admin@ministrylearn.com', username='admin')
        admin.set_password('admin123')
        admin_role = Role.query.filter_by(name='Admin').first()
        admin.roles.append(admin_role)
        db.session.add(admin)
    
    # Instructor user
    if not User.query.filter_by(email='instructor@ministrylearn.com').first():
        instructor = User(email='instructor@ministrylearn.com', username='instructor')
        instructor.set_password('instructor123')
        instructor_role = Role.query.filter_by(name='Instructor').first()
        instructor.roles.append(instructor_role)
        db.session.add(instructor)
    
    # Learner user
    if not User.query.filter_by(email='learner@ministrylearn.com').first():
        learner = User(email='learner@ministrylearn.com', username='learner')
        learner.set_password('learner123')
        learner_role = Role.query.filter_by(name='Learner').first()
        learner.roles.append(learner_role)
        db.session.add(learner)
    
    db.session.commit()
    print("✓ Seeded users")

def seed_courses():
    """Seed demo courses"""
    instructor = User.query.filter_by(email='instructor@ministrylearn.com').first()
    
    # Course 1: Ministry Basics
    if not Course.query.filter_by(title='Ministry Basics').first():
        course1 = Course(
            title='Ministry Basics',
            description='Learn the fundamentals of ministry work and service.',
            category='Ministry',
            difficulty='Beginner',
            campus='Main Campus',
            published=True,
            created_by=instructor.id
        )
        db.session.add(course1)
        db.session.flush()  # Get the ID
        
        # Add modules and lessons
        module1 = Module(course_id=course1.id, title='Introduction to Ministry', position=1)
        db.session.add(module1)
        db.session.flush()
        
        lesson1 = Lesson(
            module_id=module1.id,
            title='What is Ministry?',
            content='Ministry is the service of God through serving others...',
            position=1
        )
        db.session.add(lesson1)
        
        lesson2 = Lesson(
            module_id=module1.id,
            title='Types of Ministry',
            content='There are various types of ministry including...',
            position=2
        )
        db.session.add(lesson2)
        
        # Add assessment
        assessment1 = Assessment(
            course_id=course1.id,
            title='Ministry Basics Quiz',
            type='quiz',
            total_points=100,
            due_at=datetime.utcnow() + timedelta(days=7)
        )
        db.session.add(assessment1)
        db.session.flush()
        
        # Add questions
        question1 = Question(
            assessment_id=assessment1.id,
            prompt='What is the primary purpose of ministry?',
            type='mcq',
            points=25,
            position=1
        )
        db.session.add(question1)
        db.session.flush()
        
        # Add options
        options1 = [
            Option(question_id=question1.id, text='To serve God', is_correct=True),
            Option(question_id=question1.id, text='To make money', is_correct=False),
            Option(question_id=question1.id, text='To gain fame', is_correct=False),
            Option(question_id=question1.id, text='To avoid work', is_correct=False)
        ]
        for option in options1:
            db.session.add(option)
    
    # Course 2: Leadership in Ministry
    if not Course.query.filter_by(title='Leadership in Ministry').first():
        course2 = Course(
            title='Leadership in Ministry',
            description='Develop leadership skills for effective ministry.',
            category='Leadership',
            difficulty='Intermediate',
            campus='Main Campus',
            published=True,
            created_by=instructor.id
        )
        db.session.add(course2)
        db.session.flush()
        
        module2 = Module(course_id=course2.id, title='Leadership Principles', position=1)
        db.session.add(module2)
        db.session.flush()
        
        lesson3 = Lesson(
            module_id=module2.id,
            title='Servant Leadership',
            content='Servant leadership is about leading by serving...',
            position=1
        )
        db.session.add(lesson3)
    
    db.session.commit()
    print("✓ Seeded courses")

def seed_certification_rules():
    """Seed certification rules"""
    # Get course IDs
    ministry_basics = Course.query.filter_by(title='Ministry Basics').first()
    leadership = Course.query.filter_by(title='Leadership in Ministry').first()
    
    if not CertificationRule.query.filter_by(name='Ministry Fundamentals').first():
        rule1 = CertificationRule(
            name='Ministry Fundamentals',
            description='Basic certification for ministry volunteers',
            required_course_ids=[ministry_basics.id] if ministry_basics else [],
            min_score=70,
            expiry_months=12
        )
        db.session.add(rule1)
    
    if not CertificationRule.query.filter_by(name='Ministry Leadership').first():
        rule2 = CertificationRule(
            name='Ministry Leadership',
            description='Advanced certification for ministry leaders',
            required_course_ids=[ministry_basics.id, leadership.id] if ministry_basics and leadership else [],
            min_score=80,
            expiry_months=24
        )
        db.session.add(rule2)
    
    db.session.commit()
    print("✓ Seeded certification rules")

def main():
    """Run all seed functions"""
    app = create_app()
    with app.app_context():
        print("🌱 Seeding MinistryLearn database...")
        
        seed_roles()
        seed_users()
        seed_courses()
        seed_certification_rules()
        
        print("✅ Database seeding completed!")
        print("\nDemo accounts created:")
        print("Admin: admin@ministrylearn.com / admin123")
        print("Instructor: instructor@ministrylearn.com / instructor123")
        print("Learner: learner@ministrylearn.com / learner123")

if __name__ == '__main__':
    main()
