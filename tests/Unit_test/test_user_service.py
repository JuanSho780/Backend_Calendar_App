import pytest
from unittest.mock import MagicMock

# --- 1. SIMULACIÓN DE OBJETOS DE DOMINIO ---

class CreateUserSchema:
    """Simula el esquema de entrada para el registro."""
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

# Excepción personalizada para simular fallos de validación (Clases No Válidas)
class ValidationException(Exception):
    pass

# --- 2. SIMULACIÓN DEL SERVICIO CON LÓGICA DE VALIDACIÓN INCLUIDA ---

class MockUserService:
    """
    Simulación del UserService. Incluye lógica simple de validación 
    para probar los casos NO VÁLIDOS del Excel.
    """
    def __init__(self, user_repo, mail_api, hash_func):
        self.user_repo = user_repo
        self.mail_api = mail_api
        self.hash_func = hash_func

    def _validate_schema(self, user_data: CreateUserSchema):
        """Simula la validación de Pydantic/Schema."""
        
        # Clase No Válida (b): Nombre vacío
        if not user_data.name:
            raise ValidationException("Nombre: vacío")
        # Clase No Válida (c): Nombre > 20
        if len(user_data.name) > 20:
            raise ValidationException("Nombre: > 20 caracteres")
        
        # Clase No Válida (d): Correo vacío
        if not user_data.email:
            raise ValidationException("Correo: vacío")
        # Clase No Válida (e): Correo > 30
        if len(user_data.email) > 30:
            raise ValidationException("Correo: > 30 caracteres")
        # Clase No Válida (f): Correo no cumple con @gmail
        if "@gmail.com" not in user_data.email:
             raise ValidationException("Correo: no cumple con @gmail")
             
        # Clase No Válida (f): Contraseña vacía
        if not user_data.password:
            raise ValidationException("Contraseña: vacía")
        # Clase No Válida (g): Contraseña > 255
        if len(user_data.password) > 255:
            raise ValidationException("Contraseña: > 255")

    def create_user(self, user_data: CreateUserSchema):
        
        # PASO CRUCIAL: Simular la validación de esquema 
        self._validate_schema(user_data) 
        
        # Simulación de NO HASHEO
        processed_password = self.hash_func(user_data.password)
        
        schema_for_repo = CreateUserSchema(user_data.name, user_data.email, processed_password)

        created_user = self.user_repo.create_user(schema_for_repo)
        
        verification_code = self.mail_api.send_verification_email(user_data.email)
        self.user_repo.update_verification_code(created_user.id, verification_code)
        
        return created_user

# --- 3. FIXTURES DE SIMULACIÓN ---

@pytest.fixture
def mock_user_repo():
    return MagicMock(return_value=MagicMock()) # Aseguramos que create_user siempre devuelva un mock por defecto

@pytest.fixture
def mock_mail_api():
    return MagicMock()

@pytest.fixture
def mock_hashing_logic():
    hash_func = MagicMock(name="mock_get_password_hash")
    hash_func.side_effect = lambda p: p 
    return hash_func

@pytest.fixture
def user_service(mock_user_repo, mock_mail_api, mock_hashing_logic):
    hash_func = mock_hashing_logic
    return MockUserService(mock_user_repo, mock_mail_api, hash_func)

# --- 4. PRUEBAS DE CASOS VÁLIDOS Y NO VÁLIDOS (Combinaciones del Excel) ---

# PRUEBAS DE ÉXITO (Simulando Casos de Uso 1, 2, 3)
@pytest.mark.parametrize("name, email, password", [
    # Caso 1 (Datos Válidos de ejemplo)
    ("Usuario1", "usuario1@gmail.com", "pass123"), 
    # Caso 2 (Límites Máximos Válidos del Nombre)
    ("A" * 20, "maxname@gmail.com", "pass2"), 
    # Caso 3 (Correo cerca del límite de 30)
    ("LargoCorreo", "c" * 16 + "@gmail.com", "pass3"),
])
def test_casos_uso_validos_success(user_service, mock_user_repo, name, email, password):
    """Prueba las combinaciones de Clases Válidas (1, 2, 3)."""
    user_data = CreateUserSchema(name=name, email=email, password=password)
    
    user_service.create_user(user_data)
    
    # Se verifica que la lógica de negocio se ejecuta (llamada al repositorio y correo)
    mock_user_repo.create_user.assert_called_once()
    user_service.mail_api.send_verification_email.assert_called_once()
    
    # Limpiar mocks para el siguiente test
    mock_user_repo.create_user.reset_mock()
    user_service.mail_api.send_verification_email.reset_mock()

# PRUEBAS DE FALLO (Simulando las Combinaciones de Clases No Válidas)
@pytest.mark.parametrize("name, email, password, expected_error", [
    # (b, 2, 3): Nombre vacío (b), Correo Válido (2), Contraseña Válida (3)
    ("", "valid@gmail.com", "valid_pw", "Nombre: vacío"), 
    # (c, 2, 3): Nombre > 20 (c), Correo Válido (2), Contraseña Válida (3)
    ("A" * 21, "valid@gmail.com", "valid_pw", "Nombre: > 20 caracteres"),
    # (1, d, 3): Nombre Válido (1), Correo vacío (d), Contraseña Válida (3)
    ("ValidName", "", "valid_pw", "Correo: vacío"),
    # (1, e, 3): Nombre Válido (1), Correo > 30 (e), Contraseña Válida (3)
    ("ValidName", "largo_mas_de_30_caracteres@gmail.com", "valid_pw", "Correo: > 30 caracteres"),
    # (1, f, 3): Nombre Válido (1), Correo sin formato (f), Contraseña Válida (3)
    ("ValidName", "invalid-email.com", "valid_pw", "Correo: no cumple con @gmail"),
    # (1, 2, g): Nombre Válido (1), Correo Válido (2), Contraseña > 255 (g)
    ("ValidName", "valid@gmail.com", "X" * 256, "Contraseña: > 255"),
    # (1, 2, f): Nombre Válido (1), Correo Válido (2), Contraseña vacía (f)
    ("ValidName", "valid@gmail.com", "", "Contraseña: vacía"),
])
def test_clases_no_validas_combinations(user_service, mock_user_repo, name, email, password, expected_error):
    """Prueba todas las combinaciones de Clases No Válidas especificadas en el Excel."""
    user_data = CreateUserSchema(name=name, email=email, password=password)
    
    with pytest.raises(ValidationException, match=expected_error):
        user_service.create_user(user_data)
        
    # Aserciones (Verifica que el servicio no llamó a sus dependencias si falló la validación)
    mock_user_repo.create_user.assert_not_called()
    user_service.mail_api.send_verification_email.assert_not_called()