from apscheduler.schedulers.background import BackgroundScheduler
from src.domain.repositories.uso_equipamento import UsoEquipamentoRepository
from src.infra.gateway.email_service_impl import EmailServiceImpl
from src.infra.config.database.database import get_db


scheduler = BackgroundScheduler()
db = next(get_db())
uso_equipamento_repository = UsoEquipamentoRepository(db)
email_service = EmailServiceImpl(uso_equipamento_repository)


def start_scheduler():
    if not scheduler.running:
       scheduler.start()
    scheduler.add_job(email_service._send_with_attachment_via_smtp, 'interval', seconds=20, id='send_email_job')

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()

def add_job(func, trigger, args=None, kwargs=None):
    scheduler.add_job(func, trigger, args=args, kwargs=kwargs)
    