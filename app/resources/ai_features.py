from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import os
import requests
import json
from dotenv import load_dotenv
from ..extensions import db
from ..models.course import Course
from ..models.lesson import Lesson
from ..models.assessment import Assessment
from ..models.question import Question
from ..models.option import Option
from ..models.enrollment import Enrollment
from ..models.user import User
from ..models.module import Module
from ..utils.rbac import role_required

load_dotenv()

def register(api):
    api.add_resource(QuizGeneratorResource, "/ai/generate-quiz")
    api.add_resource(SaveQuizResource, "/ai/save-quiz")
    api.add_resource(UnpublishQuizResource, "/ai/unpublish-quiz")
    api.add_resource(CourseRecommendationsResource, "/ai/recommendations")
    api.add_resource(PublicCourseRecommendationsResource, "/ai/recommendations/public")


class QuizGeneratorResource(Resource):
    """Generate quiz questions from lesson content using AI - Instructor/Admin only"""
    @jwt_required()
    @role_required(['Admin', 'Instructor'])
    def post(self):
        try:
            data = request.get_json() or {}
            lesson_id = data.get('lesson_id')
            num_questions = data.get('num_questions', 5)
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not lesson_id:
                return {"message": "lesson_id is required"}, 400
            
            lesson = Lesson.query.get_or_404(lesson_id)
            
            # Check if user has permission (admin or course creator)
            if not user.has_role('Admin'):
                # For instructors, check if they created the course
                # Get course through module relationship
                from ..models.module import Module
                module = Module.query.get(lesson.module_id) if lesson.module_id else None
                if module:
                    course = Course.query.get(module.course_id)
                    if not course or course.created_by != user_id:
                        return {"message": "You can only generate quizzes for your own courses"}, 403
                else:
                    return {"message": "Lesson module not found"}, 404
            
            # Get AI API key
            groq_api_key = os.getenv('GROQ_API_KEY') or os.environ.get('GROQ_API_KEY')
            hf_api_key = os.getenv('HUGGINGFACE_API_KEY') or os.environ.get('HUGGINGFACE_API_KEY')
            
            if not groq_api_key and not hf_api_key:
                return {"message": "AI API key not configured"}, 400
            
            # Generate quiz using AI
            quiz_data = self.generate_quiz_ai(lesson.content or lesson.title, num_questions, groq_api_key or hf_api_key, bool(groq_api_key))
            
            return {
                "questions": quiz_data,
                "lesson_id": lesson_id,
                "lesson_title": lesson.title
            }, 200
            
        except Exception as e:
            print(f"Quiz generation error: {e}")
            import traceback
            traceback.print_exc()
            return {"message": "Failed to generate quiz"}, 500
    
    def generate_quiz_ai(self, content, num_questions, api_key, use_groq=True):
        """Generate quiz questions from content using AI"""
        try:
            if use_groq:
                return self.generate_quiz_groq(content, num_questions, api_key)
            else:
                return self.generate_quiz_hf(content, num_questions, api_key)
        except Exception as e:
            print(f"AI quiz generation error: {e}")
            return []
    
    def generate_quiz_groq(self, content, num_questions, api_key):
        """Generate quiz using Groq"""
        prompt = f"""Generate {num_questions} multiple-choice quiz questions based on the following content. 
        Return ONLY a valid JSON array with this exact format:
        [
            {{
                "question": "Question text here",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": 0
            }}
        ]
        Where correct_answer is the index (0-3) of the correct option.
        
        Content:
        {content[:2000]}
        
        Return ONLY the JSON array, no other text."""
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are a quiz generator. Return only valid JSON arrays."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=20
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content'].strip()
            
            # Try to extract JSON from response
            try:
                # Remove markdown code blocks if present
                if "```json" in ai_response:
                    ai_response = ai_response.split("```json")[1].split("```")[0].strip()
                elif "```" in ai_response:
                    ai_response = ai_response.split("```")[1].split("```")[0].strip()
                
                questions = json.loads(ai_response)
                if isinstance(questions, list):
                    return questions[:num_questions]  # Limit to requested number
            except json.JSONDecodeError:
                print(f"Failed to parse JSON: {ai_response}")
                return []
        
        return []
    
    def generate_quiz_hf(self, content, num_questions, api_key):
        """Generate quiz using Hugging Face (fallback)"""
        # Hugging Face is less reliable for structured output, so return empty
        # In production, you might use a different approach
        return []


class SaveQuizResource(Resource):
    """Save generated quiz questions as an assessment - Instructor/Admin only"""
    @jwt_required()
    @role_required(['Admin', 'Instructor'])
    def post(self):
        """Save generated quiz questions as an assessment and link to lesson"""
        try:
            data = request.get_json() or {}
            lesson_id = data.get('lesson_id')
            questions_data = data.get('questions', [])
            assessment_title = data.get('assessment_title', 'Quiz')
            update_existing = data.get('update_existing', False)
            assessment_id = data.get('assessment_id')  # If updating existing
            
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not lesson_id:
                return {"message": "lesson_id is required"}, 400
            
            if not questions_data or len(questions_data) == 0:
                return {"message": "At least one question is required"}, 400
            
            lesson = Lesson.query.get_or_404(lesson_id)
            
            # Check permissions
            if not user.has_role('Admin'):
                module = Module.query.get(lesson.module_id) if lesson.module_id else None
                if module:
                    course = Course.query.get(module.course_id)
                    if not course or course.created_by != user_id:
                        return {"message": "You can only save quizzes for your own courses"}, 403
                else:
                    return {"message": "Lesson module not found"}, 404
            
            # Get course_id from lesson
            module = Module.query.get(lesson.module_id) if lesson.module_id else None
            if not module:
                return {"message": "Lesson module not found"}, 404
            course_id = module.course_id
            
            # Create or update assessment
            if update_existing and assessment_id:
                assessment = Assessment.query.get(assessment_id)
                if not assessment:
                    return {"message": "Assessment not found"}, 404
                # Delete existing questions
                Question.query.filter_by(assessment_id=assessment_id).delete()
            else:
                # Create new assessment
                assessment = Assessment(
                    course_id=course_id,
                    title=assessment_title,
                    type='quiz',
                    total_points=len(questions_data) * 10  # 10 points per question
                )
                db.session.add(assessment)
                db.session.flush()
            
            # Create questions and options
            for idx, q_data in enumerate(questions_data):
                question = Question(
                    assessment_id=assessment.id,
                    prompt=q_data.get('question', ''),
                    type='mcq',
                    points=10,
                    position=idx + 1
                )
                db.session.add(question)
                db.session.flush()
                
                # Create options
                options = q_data.get('options', [])
                correct_answer_idx = q_data.get('correct_answer', 0)
                
                # Handle both string and index correct_answer
                if isinstance(correct_answer_idx, str):
                    # Find index of correct answer string
                    correct_answer_idx = options.index(correct_answer_idx) if correct_answer_idx in options else 0
                
                for opt_idx, option_text in enumerate(options):
                    option = Option(
                        question_id=question.id,
                        text=option_text,
                        is_correct=(opt_idx == correct_answer_idx)
                    )
                    db.session.add(option)
            
            # Link assessment to lesson
            lesson.assessment_id = assessment.id
            db.session.add(lesson)
            
            db.session.commit()
            
            return {
                "message": "Quiz saved successfully",
                "assessment_id": assessment.id,
                "assessment": assessment.to_dict()
            }, 200
            
        except Exception as e:
            print(f"Save quiz error: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return {"message": "Failed to save quiz"}, 500


class UnpublishQuizResource(Resource):
    """Unpublish/Delete quiz from a lesson - Instructor/Admin only"""
    @jwt_required()
    @role_required(['Admin', 'Instructor'])
    def post(self):
        """Unpublish quiz by removing link from lesson, optionally delete assessment"""
        try:
            data = request.get_json() or {}
            lesson_id = data.get('lesson_id')
            delete_assessment = data.get('delete_assessment', False)  # If True, delete assessment entirely
            
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not lesson_id:
                return {"message": "lesson_id is required"}, 400
            
            lesson = Lesson.query.get_or_404(lesson_id)
            
            if not lesson.assessment_id:
                return {"message": "This lesson does not have a quiz"}, 400
            
            assessment_id = lesson.assessment_id
            
            # Check permissions
            if not user.has_role('Admin'):
                module = Module.query.get(lesson.module_id) if lesson.module_id else None
                if module:
                    course = Course.query.get(module.course_id)
                    if not course or course.created_by != user_id:
                        return {"message": "You can only unpublish quizzes from your own courses"}, 403
                else:
                    return {"message": "Lesson module not found"}, 404
            
            # Remove link from lesson
            lesson.assessment_id = None
            db.session.add(lesson)
            
            # Optionally delete the assessment entirely
            if delete_assessment:
                assessment = Assessment.query.get(assessment_id)
                if assessment:
                    # Delete all questions and options (cascade should handle this, but explicit is safer)
                    questions = Question.query.filter_by(assessment_id=assessment_id).all()
                    for question in questions:
                        Option.query.filter_by(question_id=question.id).delete()
                    Question.query.filter_by(assessment_id=assessment_id).delete()
                    db.session.delete(assessment)
            
            db.session.commit()
            
            return {
                "message": "Quiz unpublished successfully" + (" and deleted" if delete_assessment else ""),
                "deleted": delete_assessment
            }, 200
            
        except Exception as e:
            print(f"Unpublish quiz error: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return {"message": "Failed to unpublish quiz"}, 500


class CourseRecommendationsResource(Resource):
    """Get AI-powered course recommendations for a user - Learners only"""
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            user = User.query.get_or_404(user_id)
            
            # Only learners can get AI recommendations
            if user.has_role('Admin') or user.has_role('Instructor'):
                return {"message": "Course recommendations are only available for learners"}, 403
            
            # Get user's enrollments and progress
            enrollments = Enrollment.query.filter_by(user_id=user_id).all()
            enrolled_course_ids = [e.course_id for e in enrollments]
            
            # Get all published courses
            all_courses = Course.query.filter_by(published=True, approved=True).all()
            
            # Get AI API key
            groq_api_key = os.getenv('GROQ_API_KEY') or os.environ.get('GROQ_API_KEY')
            hf_api_key = os.getenv('HUGGINGFACE_API_KEY') or os.environ.get('HUGGINGFACE_API_KEY')
            
            if not groq_api_key and not hf_api_key:
                # Fallback to simple recommendations
                return self.get_simple_recommendations(all_courses, enrolled_course_ids), 200
            
            # Get AI recommendations
            recommendations = self.get_ai_recommendations(
                user, enrollments, all_courses, enrolled_course_ids,
                groq_api_key or hf_api_key, bool(groq_api_key)
            )
            
            return {
                "recommendations": recommendations,
                "user_interests": self.extract_interests(enrollments)
            }, 200
            
        except Exception as e:
            print(f"Recommendations error: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to simple recommendations
            user_id = get_jwt_identity()
            enrollments = Enrollment.query.filter_by(user_id=user_id).all()
            enrolled_course_ids = [e.course_id for e in enrollments]
            all_courses = Course.query.filter_by(published=True, approved=True).all()
            return self.get_simple_recommendations(all_courses, enrolled_course_ids), 200
    
    def extract_interests(self, enrollments):
        """Extract user interests from enrollments"""
        categories = {}
        for enrollment in enrollments:
            if enrollment.course:
                cat = enrollment.course.category
                categories[cat] = categories.get(cat, 0) + 1
        return list(categories.keys())
    
    def get_simple_recommendations(self, all_courses, enrolled_course_ids):
        """Simple recommendation algorithm (fallback)"""
        # Get courses not enrolled
        available_courses = [c for c in all_courses if c.id not in enrolled_course_ids]
        
        # Sort by enrollments count (popularity)
        available_courses.sort(key=lambda x: getattr(x, 'enrollments_count', 0), reverse=True)
        
        return [c.to_dict() for c in available_courses[:6]]
    
    def get_ai_recommendations(self, user, enrollments, all_courses, enrolled_course_ids, api_key, use_groq=True):
        """Get AI-powered recommendations"""
        try:
            if use_groq:
                return self.get_recommendations_groq(user, enrollments, all_courses, enrolled_course_ids, api_key)
            else:
                return self.get_simple_recommendations(all_courses, enrolled_course_ids)
        except Exception as e:
            print(f"AI recommendations error: {e}")
            return self.get_simple_recommendations(all_courses, enrolled_course_ids)
    
    def get_recommendations_groq(self, user, enrollments, all_courses, enrolled_course_ids, api_key):
        """Get recommendations using Groq"""
        # Build context about user
        enrolled_courses_info = []
        for enrollment in enrollments[:5]:  # Last 5 courses
            if enrollment.course:
                enrolled_courses_info.append({
                    "title": enrollment.course.title,
                    "category": enrollment.course.category,
                    "difficulty": enrollment.course.difficulty,
                    "progress": enrollment.progress
                })
        
        available_courses = [c for c in all_courses if c.id not in enrolled_course_ids]
        courses_info = [{"id": c.id, "title": c.title, "category": c.category, "difficulty": c.difficulty, "description": (c.description or "")[:200]} for c in available_courses]
        
        prompt = f"""Based on a user's learning history, recommend 6 courses they would like.
        
        User's enrolled courses:
        {json.dumps(enrolled_courses_info, indent=2)}
        
        Available courses:
        {json.dumps(courses_info[:20], indent=2)}  # Limit to 20 for context
        
        Return ONLY a JSON array of course IDs (numbers) that you recommend, like: [1, 5, 12, 8, 15, 3]
        Consider:
        - Similar categories they're interested in
        - Appropriate difficulty progression
        - Diverse topics for well-rounded learning
        
        Return ONLY the JSON array of IDs, no other text."""
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are a course recommendation system. Return only valid JSON arrays of course IDs."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content'].strip()
            
            try:
                # Extract JSON
                if "```json" in ai_response:
                    ai_response = ai_response.split("```json")[1].split("```")[0].strip()
                elif "```" in ai_response:
                    ai_response = ai_response.split("```")[1].split("```")[0].strip()
                
                recommended_ids = json.loads(ai_response)
                if isinstance(recommended_ids, list):
                    # Get courses by IDs
                    recommended_courses = [c for c in available_courses if c.id in recommended_ids]
                    # Sort by recommendation order
                    recommended_courses.sort(key=lambda x: recommended_ids.index(x.id) if x.id in recommended_ids else 999)
                    return [c.to_dict() for c in recommended_courses[:6]]
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Failed to parse recommendations: {ai_response}")
        
        # Fallback
        return self.get_simple_recommendations(available_courses, [])


class PublicCourseRecommendationsResource(Resource):
    """Get popular courses for landing page - No authentication, simple algorithm (no AI)"""
    def get(self):
        """Get popular courses for landing page visitors - uses simple popularity algorithm"""
        try:
            # Get all published courses
            all_courses = Course.query.filter_by(published=True, approved=True).all()
            
            # Simple popularity-based recommendations (no AI, no user data needed)
            # Sort by enrollment count (popularity) - you may need to add this field
            # For now, use created_at as a proxy for popularity
            popular_courses = sorted(
                all_courses,
                key=lambda x: x.created_at if x.created_at else datetime.min,
                reverse=True
            )
            
            # Return top 6 courses
            recommendations = popular_courses[:6]
            
            return {
                "recommendations": [c.to_dict() for c in recommendations],
                "type": "popular",  # Indicates this is not AI-powered
                "message": "Popular courses"
            }, 200
            
        except Exception as e:
            print(f"Public recommendations error: {e}")
            import traceback
            traceback.print_exc()
            return {
                "recommendations": [],
                "type": "popular",
                "message": "Unable to load recommendations"
            }, 200

