import pytest
from unittest.mock import MagicMock

# ====================================================================
# 1. SIMULACIÓN DE OBJETOS DE DOMINIO Y EXCEPCIONES
# ====================================================================

# Excepción para simular fallos de la API del LLM/Chatbot
class LLMConnectionError(Exception):
    pass

class OptimizationRequestSchema:
    """Simula el esquema de entrada para la solicitud de optimización."""
    def __init__(self, user_id: int, tasks: list, constraints: dict):
        self.user_id = user_id
        self.tasks = tasks
        self.constraints = constraints

class OptimizationResponse:
    """Simula la respuesta del LLM/Chatbot."""
    def __init__(self, status: str, message: str, optimized_schedule: list = None):
        self.status = status
        self.message = message
        self.optimized_schedule = optimized_schedule

# ====================================================================
# 2. SIMULACIÓN DEL SERVICIO (MockOptimizationService)
# ====================================================================

class MockOptimizationService:
    """
    Servicio simulado que orquesta la generación del horario optimizado 
    mediante la integración con el MockChatbotAPI.
    """
    def __init__(self, chatbot_api: MagicMock):
        self.chatbot_api = chatbot_api

    def generate_optimized_schedule(self, request_data: OptimizationRequestSchema) -> OptimizationResponse:
        
        # Validación de campos requeridos (ej. user_id)
        if not request_data.user_id:
            raise ValueError("User ID es requerido.")

        try:
            # Llamada al Chatbot simulado
            response = self.chatbot_api.send_optimization_request(request_data)
            
            # Lógica de manejo de fallos del LLM
            if response.status != "SUCCESS":
                 raise LLMConnectionError(f"LLM API falló: {response.message}")

            return response
            
        except Exception as e:
            # Capturar y propagar cualquier error de comunicación
            raise LLMConnectionError(f"Error durante la comunicación con el LLM: {e}")

# ====================================================================
# 3. FIXTURES Y DATOS DE PRUEBA
# ====================================================================

@pytest.fixture
def mock_chatbot_api():
    """Mock para la conexión externa al LLM/Chatbot."""
    return MagicMock()

@pytest.fixture
def optimization_service(mock_chatbot_api: MagicMock):
    """Fixture para el servicio de optimización."""
    return MockOptimizationService(mock_chatbot_api)

# Datos de prueba válidos para la solicitud
VALID_REQUEST_DATA = OptimizationRequestSchema(
    user_id=123,
    tasks=[{"name": "Estudio IS2", "duration": "2h"}],
    constraints={"start_day": "Monday"}
)

# Mensaje de éxito específico que debe devolver el chatbot
EXPECTED_LLM_MESSAGE = "generando horario"

# ====================================================================
# 4. PRUEBAS DE CHATBOT/LLM
# ====================================================================

def test_llm_chatbot_responds_generando_horario_success(optimization_service: MockOptimizationService, mock_chatbot_api: MagicMock):
    """
    Caso de Éxito: Verifica que la prueba pase SOLO si el chatbot responde 
    exactamente con 'generando horario' y el status es SUCCESS.
    """
    # 1. Configurar el Mock para devolver el mensaje de éxito deseado
    mock_response = OptimizationResponse(
        status="SUCCESS",
        message=EXPECTED_LLM_MESSAGE,
        optimized_schedule=[{"time": "09:00", "task": "Estudio"}]
    )
    mock_chatbot_api.send_optimization_request.return_value = mock_response

    # 2. Ejecutar el servicio
    result = optimization_service.generate_optimized_schedule(VALID_REQUEST_DATA)

    # 3. Aserciones
    assert result.message == EXPECTED_LLM_MESSAGE
    assert result.status == "SUCCESS"
    mock_chatbot_api.send_optimization_request.assert_called_once_with(VALID_REQUEST_DATA)


def test_llm_chatbot_returns_api_error(optimization_service: MockOptimizationService, mock_chatbot_api: MagicMock):
    """
    Caso de Fallo: Simula un error interno o de conexión en la API del LLM.
    """
    # 1. Configurar el Mock para devolver un fallo de status
    mock_error_response = OptimizationResponse(
        status="FAILED",
        message="Token expirado.",
    )
    mock_chatbot_api.send_optimization_request.return_value = mock_error_response

    # 2. Ejecutar y esperar la excepción (Customizada para el LLM)
    with pytest.raises(LLMConnectionError, match="LLM API falló: Token expirado."):
        optimization_service.generate_optimized_schedule(VALID_REQUEST_DATA)
        
    mock_chatbot_api.send_optimization_request.assert_called_once()