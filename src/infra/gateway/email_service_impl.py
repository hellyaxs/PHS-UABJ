from datetime import datetime, timedelta
from src.application.gateway.email_adapter import Email, EmailAdapter
import smtplib
from email.message import EmailMessage
from src.domain.models.enums.status_de_uso import StatusUsoEquipamento
from src.domain.repositories.uso_equipamento_repository import UsoEquipamentoRepository
from src.infra.config.settings import email_settings

html_template = """
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <title>Prazo Ultrapassado</title>
  </head>
  <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
    <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.05);">
      <h2 style="color: #d32f2f;">⚠️ Prazo Ultrapassado</h2>
      <p style="font-size: 16px; color: #333333;">
        Olá <strong>{nome_usuario}</strong>,
      </p>
      <p style="font-size: 16px; color: #333333;">
        Informamos que o prazo para devolução do equipamento abaixo foi ultrapassado:
      </p>
      <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
        <tr>
          <td style="padding: 8px; background-color: #f0f0f0;"><strong>Equipamento</strong></td>
          <td style="padding: 8px;">{nome_equipamento}</td>
        </tr>
        <tr>
          <td style="padding: 8px; background-color: #f0f0f0;"><strong>Data de Retirada</strong></td>
          <td style="padding: 8px;">{data_retirada}</td>
        </tr>
        <tr>
          <td style="padding: 8px; background-color: #f0f0f0;"><strong>Data Limite</strong></td>
          <td style="padding: 8px; color: #d32f2f;"><strong>{data_limite}</strong></td>
        </tr>
      </table>
      <p style="font-size: 16px; color: #333333; margin-top: 20px;">
        Pedimos que realize a devolução o quanto antes ou entre em contato com a equipe responsável.
      </p>
      <p style="font-size: 16px; color: #333333;">
        Em caso de dúvidas, estamos à disposição.
      </p>
      <hr style="margin: 30px 0;" />
      <p style="font-size: 14px; color: #888888;">
        Este é um aviso automático, por favor, não responda este e-mail.
      </p>
    </div>
  </body>
</html>
"""

class EmailServiceImpl(EmailAdapter):
    """Implementação concreta do EmailAdapter usando SMTP"""
    
    def __init__(self, uso_equipamento_repository: UsoEquipamentoRepository):
        self.smtp_server = email_settings.EMAIL_HOST
        self.port = email_settings.EMAIL_PORT
        self.username = email_settings.EMAIL_USERNAME
        self.password = email_settings.EMAIL_PASSWORD
        self.uso_equipamento_repository = uso_equipamento_repository
    def send_email(self, email: Email) -> None:
        pass
    
    def send_email_with_attachment(self, to: str, subject: str, body: str, attachment_path: str) -> None:
        pass
    
    def send_email_with_attachment_and_cc(self, to: str, cc: str, subject: str, body: str, attachment_path: str) -> None:
        pass
    
    def _send_via_smtp(self, email: Email) -> None:
        pass
    
    def _send_with_attachment_via_smtp(self) -> None:
        """Método privado para envio com anexo via SMTP"""
        if not self.username or not self.password:
            print("ERRO: Credenciais SMTP não configuradas")
            return
        try:
            _, usos = self.uso_equipamento_repository.get_equipamentos_pendentes()
            for uso in usos:
                if uso.data_aluguel + timedelta(hours=8) < datetime.now() and uso.status != StatusUsoEquipamento.EMAIL_ENVIADO:
                    html_content = html_template.format(
                        nome_usuario=uso.funcionario.nome,
                        nome_equipamento=f"{uso.equipamento.modelo} - {uso.equipamento.marca}",
                        data_retirada=uso.data_aluguel.strftime("%d/%m/%Y"),
                        data_limite=(uso.data_aluguel + timedelta(days=1)).strftime("%d/%m/%Y")
                    )
                    msg = EmailMessage()
                    msg["Subject"] = "⚠️ Prazo de Devolução Ultrapassado - GESTÃO UFRPE"
                    msg["From"] = email_settings.EMAIL_FROM
                    msg["To"] = uso.funcionario.email
                    msg.set_content("Seu cliente de e-mail não suporta HTML.")
                    msg.add_alternative(html_content, subtype="html")
                    with smtplib.SMTP(email_settings.EMAIL_HOST, email_settings.EMAIL_PORT) as smtp:
                        smtp.starttls()
                        smtp.login(email_settings.EMAIL_USERNAME, email_settings.EMAIL_PASSWORD)
                        smtp.send_message(msg)
                        
                    uso.status = StatusUsoEquipamento.EMAIL_ENVIADO
                    self.uso_equipamento_repository.update_uso_equipamento(uso)

        except Exception as e:
            print(f"Erro ao enviar email com anexo: {e}")


