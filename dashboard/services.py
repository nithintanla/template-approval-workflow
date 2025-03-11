class TemplateApprovalService:
    @staticmethod
    def check_approval(content):
        """
        Mock API service to check template approval
        Returns: (approved: bool, message: str)
        """
        content = content.lower()
        if "good" in content:
            return True, "Template approved automatically"
        elif "bad" in content:
            return False, "Template rejected due to inappropriate content"
        return False, "Template rejected - does not meet approval criteria"
