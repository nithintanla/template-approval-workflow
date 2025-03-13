from .models import ApprovalSettings

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
