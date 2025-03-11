from .models import ApprovalSettings

class TemplateApprovalService:
    @staticmethod
    def check_approval(content):
        """
        Check template against configured rejection keywords
        Returns: (approved: bool, message: str)
        """
        try:
            settings = ApprovalSettings.objects.latest('created_at')
            keywords = settings.get_keywords_list()
            content = content.lower()
            
            for keyword in keywords:
                if keyword in content:
                    return False, f"Template rejected - contains prohibited word: {keyword}"
            
            return True, "Template approved automatically"
        except ApprovalSettings.DoesNotExist:
            return True, "Template approved (no rejection rules configured)"
