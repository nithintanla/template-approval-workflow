from .models import ApprovalSettings
from openai import OpenAI
from django.conf import settings
from typing import Tuple

class TemplateApprovalService:
    @staticmethod
    def check_approval(content):
        try:
            settings = ApprovalSettings.objects.latest('created_at')
            
            # Convert content to lowercase for case-insensitive matching
            content_lower = content.lower()
            
            # Get keywords lists
            rejection_keywords = [k.strip().lower() for k in settings.rejection_keywords.split(',') if k.strip()]
            approval_keywords = [k.strip().lower() for k in settings.keywords_approve.split(',') if k.strip()]
            manual_keywords = [k.strip().lower() for k in settings.keywords_manual.split(',') if k.strip()]
            
            # Check rejection keywords first
            for keyword in rejection_keywords:
                if keyword in content_lower:
                    return 'rejected_system', f"Template rejected - contains keyword: {keyword}"
            
            # Check auto-approval keywords
            for keyword in approval_keywords:
                if keyword in content_lower:
                    return 'approved_system', "Template automatically approved"
            
            # Check manual approval keywords
            for keyword in manual_keywords:
                if keyword in content_lower:
                    return 'pending', f"Template requires manual approval - contains keyword: {keyword}"
            
            # Default case: send for manual approval
            return 'pending', "Template requires manual approval"
            
        except ApprovalSettings.DoesNotExist:
            return 'pending', "No approval settings found - defaulting to manual approval"

class TemplateModeration:
    @staticmethod
    def analyze_content(content: str) -> Tuple[str, str]:
        """
        Analyze template content using OpenAI API, falls back to keyword-based analysis if API fails
        Returns: (decision, explanation)
        """
        # Check if API key is properly configured
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == 'your_actual_api_key_here':
            print("OpenAI API key not properly configured")
            return TemplateModeration._keyword_based_analysis(content, 
                   "OpenAI API key not configured - falling back to keyword analysis")

        # Try OpenAI analysis
        try:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            prompt = f"""
            Analyze the following marketing template content and decide if it should be:
            - "Approve" - if the content is safe and appropriate
            - "Manual" - if the content needs human review
            - "Reject" - if the content is inappropriate or harmful

            Content: {content}

            Provide your decision as a single word (Approve/Manual/Reject) followed by a brief explanation after a pipe symbol (|).
            Example: "Approve|Content is appropriate and safe for marketing"
            """
            
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a content moderation system. Respond only with a decision and brief explanation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=100
            )
            
            result = response.choices[0].message.content.strip()
            decision, explanation = result.split('|')
            return decision.strip(), explanation.strip()
            
        except Exception as e:
            error_msg = str(e)
            print(f"OpenAI API Error: {error_msg}")
            
            # Check for specific error types
            if "invalid_api_key" in error_msg or "401" in error_msg:
                error_explanation = "Invalid OpenAI API key - falling back to keyword analysis"
            elif "timeout" in error_msg:
                error_explanation = "OpenAI API timeout - falling back to keyword analysis"
            else:
                error_explanation = "OpenAI API error - falling back to keyword analysis"
            
            return TemplateModeration._keyword_based_analysis(content, error_explanation)

    @staticmethod
    def _keyword_based_analysis(content: str, error_context: str = None) -> Tuple[str, str]:
        """Fallback method using keyword-based analysis"""
        try:
            decision, explanation = TemplateApprovalService.check_approval(content)
            status_mapping = {
                'approved_system': ('Approve', f'Approved based on keywords. ({error_context if error_context else "OpenAI unavailable"})'),
                'rejected_system': ('Reject', f'Rejected based on keywords. ({error_context if error_context else "OpenAI unavailable"})'),
                'pending': ('Manual', f'Requires manual review based on keywords. ({error_context if error_context else "OpenAI unavailable"})')
            }
            return status_mapping.get(decision, ('Manual', explanation))
        except Exception as e:
            return 'Manual', f"Using manual review due to errors: {str(e)}"
