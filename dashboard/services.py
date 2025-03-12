from .models import ApprovalSettings

class TemplateApprovalService:
    @staticmethod
    def check_approval(content):
        """
        Check template against configured rejection keywords
        Returns: (approved: bool, message: str)
        """
        keywords_approve = ['good', 'hi']
        keywords_manual = ['bad', 'smoke', 'drink', 'earn fast money', 'you won 1cr']

        content = content.lower()

        for keyword in keywords_approve:
            if keyword in content:
                return True, "Template approved automatically"

        for keyword in keywords_manual:
            if keyword in content:
                return False, f"Template sent for manual approval - contains word: {keyword}"

        return False, "Template sent for manual approval (no matching keywords)"
