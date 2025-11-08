from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import requests
import json
from dotenv import load_dotenv

# Ensure .env is loaded
load_dotenv()

def register(api):
    api.add_resource(AIChatResource, "/ai/chat")
    api.add_resource(AIChatTestResource, "/ai/test")


class AIChatResource(Resource):
    def post(self):
        """Chat with AI assistant"""
        try:
            data = request.get_json() or {}
            message = data.get('message', '')
            conversation_history = data.get('conversation_history', [])
            
            if not message:
                return {"message": "Message is required"}, 400
            
            # Get AI response
            ai_response, is_ai = self.get_ai_response(message, conversation_history)
            
            return {
                "response": ai_response,
                "status": "success" if is_ai else "fallback"
            }, 200
            
        except Exception as e:
            print(f"AI Chat Error: {e}")
            import traceback
            traceback.print_exc()
            # Return fallback response
            message_text = data.get('message', '') if 'data' in locals() else 'Unknown'
            return {
                "response": self.get_fallback_response(message_text),
                "status": "fallback"
            }, 200
    
    def get_ai_response(self, message, conversation_history):
        """Get AI response from free AI services (Groq/Hugging Face) or fallback. Returns (response, is_ai)"""
        # Try Groq first (free, fast)
        groq_api_key = os.getenv('GROQ_API_KEY') or os.environ.get('GROQ_API_KEY')
        
        if groq_api_key:
            print("Using Groq AI (free tier)")
            return self.get_groq_response(message, conversation_history, groq_api_key)
        
        # Try Hugging Face as backup (free tier)
        hf_api_key = os.getenv('HUGGINGFACE_API_KEY') or os.environ.get('HUGGINGFACE_API_KEY')
        
        if hf_api_key:
            print("Using Hugging Face AI (free tier)")
            return self.get_huggingface_response(message, conversation_history, hf_api_key)
        
        # No free API keys found, use fallback
        print("No free AI API keys found. Using fallback responses.")
        print("To enable AI: Get a free API key from https://console.groq.com/ or https://huggingface.co/settings/tokens")
        return self.get_fallback_response(message), False
        
    def get_groq_response(self, message, conversation_history, api_key):
        """Get AI response from Groq (free, fast)"""
        try:
            # Prepare messages for Groq
            messages = [
                {
                    "role": "system",
                    "content": """You are a helpful AI assistant for MinistryLearn, a Christian ministry learning platform. 
                    You help users with questions about:
                    - Courses, enrollment, certifications, dashboards, and platform features
                    - Biblical questions and ministry-related topics
                    - General questions about faith, Christianity, and ministry
                    
                    Be friendly, concise, and helpful. Answer questions knowledgeably about biblical topics and ministry matters.
                    For platform-specific questions, guide users to the appropriate sections."""
                }
            ]
            
            # Add conversation history (last 5 messages for context)
            for msg in conversation_history[-5:]:
                if msg.get('role') and msg.get('content'):
                    messages.append({
                        "role": msg['role'],
                        "content": msg['content']
                    })
            
            # Add current message
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Call Groq API (free tier, very fast)
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "llama-3.1-8b-instant",  # Free, fast model
                "messages": messages,
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            print(f"Calling Groq API with message: {message[:50]}...")
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=15
            )
            
            print(f"Groq API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content'].strip()
                print(f"✓ Groq AI Response received: {ai_response[:100]}...")
                return ai_response, True
            else:
                error_text = response.text
                print(f"✗ Groq API Error: {response.status_code} - {error_text}")
                return self.get_fallback_response(message), False
                
        except requests.exceptions.Timeout:
            print("✗ Groq API timeout")
            return self.get_fallback_response(message), False
        except Exception as e:
            print(f"✗ Error calling Groq: {e}")
            import traceback
            traceback.print_exc()
            return self.get_fallback_response(message), False
    
    def get_huggingface_response(self, message, conversation_history, api_key):
        """Get AI response from Hugging Face (free tier)"""
        try:
            # Prepare prompt with conversation history
            system_prompt = """You are a helpful AI assistant for MinistryLearn, a Christian ministry learning platform. 
            You help users with questions about courses, enrollment, certifications, biblical topics, and ministry matters.
            Be friendly, concise, and helpful."""
            
            conversation_text = system_prompt + "\n\n"
            for msg in conversation_history[-3:]:  # Last 3 messages for Hugging Face
                if msg.get('role') and msg.get('content'):
                    role = "User" if msg['role'] == 'user' else "Assistant"
                    conversation_text += f"{role}: {msg['content']}\n"
            
            conversation_text += f"User: {message}\nAssistant:"
            
            # Call Hugging Face Inference API
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": conversation_text,
                "parameters": {
                    "max_new_tokens": 300,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }
            
            print(f"Calling Hugging Face API with message: {message[:50]}...")
            response = requests.post(
                "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
                headers=headers,
                json=payload,
                timeout=20
            )
            
            print(f"Hugging Face API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                # Hugging Face returns different formats
                if isinstance(result, list) and len(result) > 0:
                    ai_response = result[0].get('generated_text', '').strip()
                elif isinstance(result, dict):
                    ai_response = result.get('generated_text', '').strip()
                else:
                    ai_response = str(result).strip()
                
                if ai_response:
                    print(f"✓ Hugging Face AI Response received: {ai_response[:100]}...")
                    return ai_response, True
                else:
                    return self.get_fallback_response(message), False
            else:
                error_text = response.text
                print(f"✗ Hugging Face API Error: {response.status_code} - {error_text}")
                return self.get_fallback_response(message), False
                
        except requests.exceptions.Timeout:
            print("✗ Hugging Face API timeout")
            return self.get_fallback_response(message), False
        except Exception as e:
            print(f"✗ Error calling Hugging Face: {e}")
            import traceback
            traceback.print_exc()
            return self.get_fallback_response(message), False
    
    def get_fallback_response(self, message):
        """Fallback response when AI is not available"""
        lower_message = message.lower()
        
        if 'course' in lower_message or 'enroll' in lower_message:
            return "To enroll in a course, go to the Course Catalog and click 'View Details' on any course you're interested in. You can filter courses by campus, category, or difficulty level."
        
        if 'certificate' in lower_message or 'certification' in lower_message:
            return "Certifications are awarded when you complete a course. You can view your certifications in the Certifications section of your dashboard."
        
        if 'dashboard' in lower_message or 'progress' in lower_message:
            return "Your dashboard shows your enrolled courses, progress, and certifications. Navigate to Dashboard from the main menu to view your learning journey."
        
        if 'instructor' in lower_message or 'teacher' in lower_message:
            return "Instructors create and manage courses. If you're an instructor, you can access the Instructor Dashboard to create courses, grade submissions, and manage your content."
        
        if 'admin' in lower_message or 'administrator' in lower_message:
            return "Admins manage the platform, approve courses, send announcements, and oversee user management. Access the Admin Dashboard for administrative functions."
        
        if 'help' in lower_message or 'support' in lower_message:
            return "I can help you with questions about courses, enrollment, certifications, dashboards, and platform features. What would you like to know?"
        
        return f"I understand you're asking about: '{message}'. For specific help, you can browse the Course Catalog, check your Dashboard for progress, or contact support for detailed assistance."


class AIChatTestResource(Resource):
    """Test endpoint to check if API keys are configured"""
    def get(self):
        groq_api_key = os.getenv('GROQ_API_KEY')
        hf_api_key = os.getenv('HUGGINGFACE_API_KEY')
        
        return {
            "groq_configured": bool(groq_api_key),
            "groq_preview": f"{groq_api_key[:10]}..." if groq_api_key else "Not set",
            "huggingface_configured": bool(hf_api_key),
            "huggingface_preview": f"{hf_api_key[:10]}..." if hf_api_key else "Not set",
            "any_ai_available": bool(groq_api_key or hf_api_key),
            "instructions": {
                "groq": "Get free API key at https://console.groq.com/ (recommended - fast and free)",
                "huggingface": "Get free API key at https://huggingface.co/settings/tokens"
            }
        }, 200

