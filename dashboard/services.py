from .models import ApprovalSettings

class TemplateApprovalService:
    @staticmethod
    def check_approval(content):
        """
        Check template against configured rejection keywords
        Returns: (approved: bool, message: str)
        """
        settings = ApprovalSettings.objects.latest('created_at')
        rejection_keywords = settings.get_keywords_list('rejection_keywords')
        keywords_approve = settings.get_keywords_list('keywords_approve')
        keywords_manual = settings.get_keywords_list('keywords_manual')
        content = content.lower()
        
        for keyword in rejection_keywords:
            if keyword in content:
                return False, f"Template rejected - contains word: {keyword}"
        
        for keyword in keywords_approve:
            if keyword in content:
                return True, "Template approved automatically"
        
        for keyword in keywords_manual:
            if keyword in content:
                return False, f"Template sent for manual approval - contains word: {keyword}"
        
        return False, "Template sent for manual approval (no matching keywords)"
