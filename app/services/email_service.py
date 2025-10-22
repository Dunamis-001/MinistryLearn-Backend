import sendgrid
from sendgrid.helpers.mail import Mail
from ..config import Config

class EmailService:
    def __init__(self):
        self.sg = sendgrid.SendGridAPIClient(api_key=Config.SENDGRID_API_KEY)
    
    def send_enrollment_confirmation(self, user_email, course_title):
        """Send enrollment confirmation email"""
        try:
            message = Mail(
                from_email="noreply@ministrylearn.com",
                to_emails=user_email,
                subject=f"Enrolled in {course_title}",
                html_content=f"""
                <h2>Welcome to {course_title}!</h2>
                <p>You have successfully enrolled in the course. You can now start learning.</p>
                <p>Visit your dashboard to begin.</p>
                """
            )
            response = self.sg.send(message)
            return response.status_code == 202
        except Exception as e:
            print(f"Email send failed: {str(e)}")
            return False
    
    def send_certification_awarded(self, user_email, certification_name):
        """Send certification awarded email"""
        try:
            message = Mail(
                from_email="noreply@ministrylearn.com",
                to_emails=user_email,
                subject=f"Certification Awarded: {certification_name}",
                html_content=f"""
                <h2>Congratulations!</h2>
                <p>You have been awarded the {certification_name} certification.</p>
                <p>You can view and download your certificate from your dashboard.</p>
                """
            )
            response = self.sg.send(message)
            return response.status_code == 202
        except Exception as e:
            print(f"Email send failed: {str(e)}")
            return False
    
    def send_due_reminder(self, user_email, assessment_title, due_date):
        """Send assessment due reminder"""
        try:
            message = Mail(
                from_email="noreply@ministrylearn.com",
                to_emails=user_email,
                subject=f"Assessment Due: {assessment_title}",
                html_content=f"""
                <h2>Assessment Reminder</h2>
                <p>The assessment "{assessment_title}" is due on {due_date}.</p>
                <p>Please complete it before the deadline.</p>
                """
            )
            response = self.sg.send(message)
            return response.status_code == 202
        except Exception as e:
            print(f"Email send failed: {str(e)}")
            return False