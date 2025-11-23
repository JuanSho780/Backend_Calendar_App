import pytest
from unittest.mock import MagicMock
from datetime import datetime

# ====================================================================
# 1. SIMULACIÓN DE OBJETOS DE DOMINIO Y EXCEPCIONES
# ====================================================================

class LoginUserSchema:
    """Simula el esquema de entrada para Iniciar Sesión."""
    def __init__(self, username_or_email: str, password: str):
        self.username_or_email = username_or_email
        self.password = password

class MockUser:
    """Simula la entidad User devuelta por el repositorio para Login."""
    def __init__(self, id, username, email, hashed_password):
        self.id = id
        self.username = username
        self.email = email
        self.hashed_password = hashed_password

# Excepción personalizada para simular fallos de validación o negocio
class CustomException(Exception):
    pass

# ====================================================================
# 2. SIMULACIÓN DEL SERVICIO (MockLoginService)
# ====================================================================

class MockLoginService:
    """
    Simulación del servicio para Iniciar Sesión.
    Incluye lógica de validación para probar los casos NO VÁLIDOS del Excel.
    """
    def __init__(self, user_repo: MagicMock, verify_func: callable):
        self.user_repo = user_repo
        self.verify_func = verify_func

    def _validate_schema(self, login_data: LoginUserSchema):
        """Simula la validación de esquema basada en las reglas del Excel."""
        
        # 1. Validación de Nombre/Correo [1-20]
        if not login_data.username_or_email: # Clase No Válida (b): vacío
            raise CustomException("VALIDATION_USERNAME_EMPTY")
        if not (1 <= len(login_data.username_or_email) <= 20): # Clase No Válida (c): >20
            raise CustomException("VALIDATION_USERNAME_RANGE")

        # 2. Validación de Contraseña [hasta 30]
        if not login_data.password: # Clase No Válida (d): vacío
            raise CustomException("VALIDATION_PASSWORD_EMPTY")
        if len(login_data.password) > 30: # Clase No Válida (e): >30
            raise CustomException("VALIDATION_PASSWORD_RANGE")
        
        # Clase No Válida (f): No cumpla con el formato de correo. 
        # NOTA: En login, el formato es flexible (puede ser username O email). 
        # Simularemos una regla simple para cubrir el caso 'f'.
        if "@" in login_data.username_or_email and ".com" not in login_data.username_or_email:
             raise CustomException("VALIDATION_USERNAME_EMAIL_FORMAT")


    def login_user(self, login_data: LoginUserSchema):
        
        # 🚨 PASO 1: Simular la validación de esquema 🚨
        self._validate_schema(login_data)
        
        # Simular búsqueda de usuario (usando user_repo.get_by_email_or_username)
        user = self.user_repo.get_by_email_or_username(login_data.username_or_email)
        
        # Simular fallo de negocio: Usuario no encontrado
        if user is None:
            raise CustomException("LOGIN_USER_NOT_FOUND")

        # Simular verificación de contraseña
        if not self.verify_func(login_data.password, user.hashed_password):
            raise CustomException("LOGIN_INVALID_PASSWORD")
            
        # Retorna el usuario si el login es exitoso
        return user

# ====================================================================
# 3. FIXTURES DE SIMULACIÓN
# ====================================================================

@pytest.fixture
def mock_user_repo():
    return MagicMock()

@pytest.fixture
def mock_verify_password():
    """Simula la función de verificación de contraseña."""
    # Por defecto, simula que la verificación es exitosa
    return MagicMock(return_value=True)

@pytest.fixture
def login_service(mock_user_repo: MagicMock, mock_verify_password: MagicMock):
    return MockLoginService(mock_user_repo, mock_verify_password)

# Datos de usuario mockeado
VALID_MOCK_USER = MockUser(
    id=1, 
    username="testuser", 
    email="test@gmail.com", 
    hashed_password="hashed_pw_valid"
)

# ====================================================================
# 4. PRUEBAS DE CASOS VÁLIDOS (Clases Válidas 1, 2)
# ====================================================================

@pytest.mark.parametrize("username_or_email, password", [
    # Caso (1,2): Nombre de usuario y Contraseña Válidos
    ("testuser", "short_password"), 
    # Caso (1,2) con límites: Nombre de usuario max 20, Contraseña max 30
    ("A" * 20, "B" * 30), 
    # Caso con email (asumiendo que email es < 20 caracteres)
    ("test@gmail.com", "valid_pw_1"), 
])
def test_casos_uso_validos_success(login_service: MockLoginService, mock_user_repo: MagicMock, 
                                   username_or_email: str, password: str):
    """Prueba las combinaciones de Clases Válidas (1, 2)."""
    
    login_data = LoginUserSchema(username_or_email, password)
    
    # Simular que el repositorio encuentra al usuario
    mock_user_repo.get_by_email_or_username.return_value = VALID_MOCK_USER

    result = login_service.login_user(login_data)
    
    # Aserciones de éxito
    assert result == VALID_MOCK_USER
    mock_user_repo.get_by_email_or_username.assert_called_once_with(username_or_email)
    login_service.verify_func.assert_called_once()
    
    # Limpieza de mocks
    mock_user_repo.get_by_email_or_username.reset_mock()
    login_service.verify_func.reset_mock()


# ====================================================================
# 5. PRUEBAS DE CLASES NO VÁLIDAS (FALLO DE VALIDACIÓN y NEGOCIO)
# ====================================================================

@pytest.mark.parametrize("username_or_email, password, expected_error", [
    # (1, d): Nombre/Correo Válido (1), Contraseña vacía (d)
    ("validuser", "", "VALIDATION_PASSWORD_EMPTY"),
    # (1, e): Nombre/Correo Válido (1), Contraseña > 30 (e)
    ("validuser", "P" * 31, "VALIDATION_PASSWORD_RANGE"),
    # (1, f): Nombre/Correo Válido (1), Contraseña formato (f) 
    ("valid@invalid", "valid_pw", "VALIDATION_USERNAME_EMAIL_FORMAT"),
    # (b, 2): Nombre/Correo vacío (b), Contraseña Válida (2)
    ("", "valid_pw", "VALIDATION_USERNAME_EMPTY"),
    # (c, 2): Nombre/Correo > 20 (c), Contraseña Válida (2)
    ("U" * 21, "valid_pw", "VALIDATION_USERNAME_RANGE"),
])
def test_clases_no_validas_combinations(login_service: MockLoginService, mock_user_repo: MagicMock,
                                        username_or_email: str, password: str, expected_error: str):
    """Prueba las combinaciones de Clases No Válidas especificadas en el Excel."""
    
    login_data = LoginUserSchema(username_or_email, password)
    
    with pytest.raises(CustomException, match=expected_error):
        login_service.login_user(login_data)
        
    # Verifica que el repositorio NO fue llamado si falló la validación
    mock_user_repo.get_by_email_or_username.assert_not_called()
    login_service.verify_func.assert_not_called()


def test_fallo_de_negocio_user_not_found(login_service: MockLoginService, mock_user_repo: MagicMock):
    """
    Simula el fallo de negocio: El usuario no existe.
    """
    login_data = LoginUserSchema("nonexistent", "pw")
    mock_user_repo.get_by_email_or_username.return_value = None
    
    with pytest.raises(CustomException, match="LOGIN_USER_NOT_FOUND"):
        login_service.login_user(login_data)
        
    mock_user_repo.get_by_email_or_username.assert_called_once()
    login_service.verify_func.assert_not_called()


def test_fallo_de_negocio_invalid_password(login_service: MockLoginService, mock_user_repo: MagicMock):
    """
    Simula el fallo de negocio: La contraseña es incorrecta.
    """
    login_data = LoginUserSchema("testuser", "wrong_pw")
    mock_user_repo.get_by_email_or_username.return_value = VALID_MOCK_USER
    
    # Simular que la verificación de contraseña falla
    login_service.verify_func.return_value = False
    
    with pytest.raises(CustomException, match="LOGIN_INVALID_PASSWORD"):
        login_service.login_user(login_data)
        
    mock_user_repo.get_by_email_or_username.assert_called_once()
    login_service.verify_func.assert_called_once()