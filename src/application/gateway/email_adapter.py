import abc

class Email:
    def __init__(self, to: str, subject: str, body: str, attachment_path: str = None):
        self.to = to
        self.subject = subject
        self.body = body
        self.attachment_path = attachment_path

    def __str__(self):
        return f"Email(to={self.to}, subject={self.subject}, body={self.body}, attachment_path={self.attachment_path})"

class EmailAdapter(abc.ABC):
    """Interface pura para envio de emails - apenas declara os métodos"""
    
    @abc.abstractmethod
    def send_email(self, email: Email) -> None:
        """Envia um email simples"""
        pass

    @abc.abstractmethod
    def send_email_with_attachment(self, to: str, subject: str, body: str, attachment_path: str) -> None:
        """Envia um email com anexo"""
        pass
    
    @abc.abstractmethod
    def send_email_with_attachment_and_cc(self, to: str, cc: str, subject: str, body: str, attachment_path: str) -> None:
        """Envia um email com anexo e cópia"""
        pass
