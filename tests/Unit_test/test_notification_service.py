import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta

# ====================================================================
# 1. SIMULACIÓN DE OBJETOS DE DOMINIO Y EXCEPCIONES
# ====================================================================

# Excepción personalizada para simular fallos en el envío de correo
class EmailSendingError(Exception):
    pass

class MockEvent:
    """Simula una entrada de evento en la base de datos."""
    def __init__(self, title: str, user_email: str, start_time: datetime, notification_minutes_before: int):
        self.title = title
        self.user_email = user_email
        self.start_time = start_time
        self.notification_minutes_before = notification_minutes_before # Cuántos minutos antes notificar

# ====================================================================
# 2. SIMULACIÓN DEL SERVICIO (MockNotificationService)
# ====================================================================

class MockNotificationService:
    """
    Servicio simulado para enviar recordatorios por correo.
    Orquesta la obtención de eventos y el envío del email.
    """
    def __init__(self, event_repo: MagicMock, mail_api: MagicMock, current_time: datetime):
        self.event_repo = event_repo
        self.mail_api = mail_api
        self.current_time = current_time

    def check_and_send_notifications(self):
        """
        Lógica para verificar eventos que están a punto de ocurrir
        basado en la hora actual (self.current_time) y enviar el correo.
        """
        
        # 1. Obtener todos los eventos activos (simulación)
        events_to_check = self.event_repo.get_all_active_events()
        
        notifications_sent = []
        
        for event in events_to_check:
            
            # Calcular la hora en la que se debe enviar la notificación
            notification_time = event.start_time - timedelta(minutes=event.notification_minutes_before)
            
            # Determinar si la hora actual está DENTRO de la ventana de notificación
            is_time_to_notify = (
                self.current_time >= notification_time and
                self.current_time < event.start_time
            )
            
            if is_time_to_notify:
                
                subject = f"Recordatorio: {event.title}"
                body = f"Tienes el evento '{event.title}' programado para las {event.start_time.strftime('%H:%M')}."
                
                try:
                    # 2. Llamar al MockMailAPI para enviar el correo
                    self.mail_api.send_email(event.user_email, subject, body)
                    
                    # El test pasa si se llegó a este punto (True)
                    notifications_sent.append(True) 
                    
                except EmailSendingError:
                    # Reportar fallo si la API de correo falla
                    notifications_sent.append(False) 
                    
        return notifications_sent

# ====================================================================
# 3. FIXTURES Y DATOS DE PRUEBA
# ====================================================================

@pytest.fixture
def mock_event_repo():
    """Mock del repositorio de eventos."""
    return MagicMock()

@pytest.fixture
def mock_mail_api():
    """Mock de la API de envío de correos. Se inicializa sin efecto lateral."""
    mail_api = MagicMock()
    return mail_api

@pytest.fixture
def current_time():
    """Hora actual simulada para las pruebas (Ejemplo: 2025-11-23 10:00:00)."""
    return datetime(2025, 11, 23, 10, 0, 0)

@pytest.fixture
def notification_service(mock_event_repo: MagicMock, mock_mail_api: MagicMock, current_time: datetime):
    """Servicio de notificación con dependencias inyectadas."""
    return MockNotificationService(mock_event_repo, mock_mail_api, current_time)

# --- DATOS DE EVENTOS ---

# Evento 1: Notificación en el momento justo (10:00 es 15 minutos antes de 10:15)
EVENT_READY_TO_NOTIFY = MockEvent(
    title="Reunión de Proyecto", 
    user_email="user1@example.com", 
    start_time=datetime(2025, 11, 23, 10, 15, 0), 
    notification_minutes_before=15 
)

# Evento 2: Todavía NO es hora de notificar (La notificación se debe enviar 5 minutos antes, a las 10:30)
EVENT_TOO_EARLY = MockEvent(
    title="Clase de Ingeniería", 
    user_email="user2@example.com", 
    start_time=datetime(2025, 11, 23, 10, 35, 0), 
    notification_minutes_before=5
)

# ====================================================================
# 4. PRUEBAS
# ====================================================================

def test_notification_sent_successfully(notification_service: MockNotificationService, mock_event_repo: MagicMock, mock_mail_api: MagicMock):
    """
    Caso de Éxito Principal: Verifica que la prueba pase SOLO si se llama a la API de correo
    para el evento que cumple la condición de tiempo.
    """
    # 1. Configurar el Mock para devolver el evento listo
    mock_event_repo.get_all_active_events.return_value = [EVENT_READY_TO_NOTIFY, EVENT_TOO_EARLY]
    
    # 2. Ejecutar el servicio
    results = notification_service.check_and_send_notifications()
    
    # 3. Aserciones
    
    # 🚨 Condición de éxito: Se verifica que la función de envío de correo fue llamada UNA vez
    mock_mail_api.send_email.assert_called_once() 
    
    # Se asegura que la función devuelve un resultado de éxito
    assert results == [True]


def test_notification_not_sent_if_too_early(notification_service: MockNotificationService, mock_event_repo: MagicMock, mock_mail_api: MagicMock):
    """
    Verifica que NO se envíe el correo si el evento aún no está en la ventana de notificación.
    """
    # 1. Configurar el Mock para devolver eventos que NO deben ser notificados
    mock_event_repo.get_all_active_events.return_value = [EVENT_TOO_EARLY]
    
    # 2. Ejecutar el servicio
    results = notification_service.check_and_send_notifications()
    
    # 3. Aserciones
    
    # Aserción clave: La prueba pasa si la API de correo NO fue llamada
    mock_mail_api.send_email.assert_not_called()
    
    # La lista de resultados debe estar vacía
    assert results == []


def test_notification_handles_email_sending_error(notification_service: MockNotificationService, mock_event_repo: MagicMock, mock_mail_api: MagicMock):
    """
    Simula un fallo en la API de correo y verifica que el servicio lo reporte como fallo (False)
    sin detener la ejecución (si hubiera más eventos).
    """
    # 1. Configurar el Mock para devolver el evento listo para notificar
    mock_event_repo.get_all_active_events.return_value = [EVENT_READY_TO_NOTIFY]

    # 2. Configurar el MockMailAPI para que lance la excepción al ser llamado
    mock_mail_api.send_email.side_effect = EmailSendingError("SMTP connection refused")
    
    # 3. Ejecutar el servicio
    results = notification_service.check_and_send_notifications()
    
    # 4. Aserciones
    mock_mail_api.send_email.assert_called_once()
    
    # Verificar que el resultado reportado sea un fallo (False)
    assert results == [False]