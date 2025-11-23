import pytest
from unittest.mock import MagicMock
from datetime import datetime, time

# ====================================================================
# 1. SIMULACIÓN DE OBJETOS DE DOMINIO Y EXCEPCIONES
# ====================================================================

class CreateScheduleEntrySchema:
    """Simula el esquema de entrada."""
    def __init__(self, calendar_id: int, title: str, description: str, location: str, schedule_blocks: list):
        self.calendar_id = calendar_id
        self.title = title
        self.description = description
        self.location = location
        self.schedule_blocks = schedule_blocks

# Excepción personalizada para simular fallos de validación o negocio
class CustomException(Exception):
    pass

# ====================================================================
# 2. SIMULACIÓN DEL SERVICIO (MockScheduleEntryService)
# ====================================================================

class MockScheduleEntryService:
    """Simulación del servicio, incluyendo lógica de validación."""
    def __init__(self, schedule_repo: MagicMock):
        self.schedule_repo = schedule_repo

    def _validate_schema(self, entry_data: CreateScheduleEntrySchema):
        """Simula la validación de esquema basada en las reglas del Excel."""
        
        # 1. Validación de Calendario [1-60]
        if entry_data.calendar_id is None: 
            raise CustomException("VALIDATION_CALENDAR_EMPTY")
        if not (1 <= entry_data.calendar_id <= 60): 
            raise CustomException("VALIDATION_CALENDAR_RANGE")

        # 2. Validación de Título [1-60]
        if not entry_data.title: 
            raise CustomException("VALIDATION_TITLE_EMPTY")
        if not (1 <= len(entry_data.title) <= 60): 
            raise CustomException("VALIDATION_TITLE_RANGE")

        # 3. Validación de Descripción [1-200]
        if not entry_data.description: 
            raise CustomException("VALIDATION_DESCRIPTION_EMPTY")
        if not (1 <= len(entry_data.description) <= 200): 
            raise CustomException("VALIDATION_DESCRIPTION_RANGE")
        
        # 4. Validación de Ubicación [1-40]
        if not entry_data.location: 
            raise CustomException("VALIDATION_LOCATION_EMPTY")
        if not (1 <= len(entry_data.location) <= 40): 
            raise CustomException("VALIDATION_LOCATION_RANGE")

        # 5. Validación de Bloque de horario [fechas validas]
        if not entry_data.schedule_blocks: 
            raise CustomException("VALIDATION_BLOCKS_EMPTY")
        
        for block in entry_data.schedule_blocks:
            # Simulación de falla en la lógica de tiempo (start < end)
            if 'start_time' in block and 'end_time' in block:
                try:
                    start = time.fromisoformat(block['start_time'])
                    end = time.fromisoformat(block['end_time'])
                    if start >= end:
                        raise CustomException("VALIDATION_BLOCKS_TIME_INVALID")
                except ValueError:
                    raise CustomException("VALIDATION_BLOCKS_FORMAT_INVALID")


    def create_schedule_entry(self, entry_data: CreateScheduleEntrySchema):
        
        self._validate_schema(entry_data)
        
        created_entry = self.schedule_repo.create_entry(entry_data)
        
        # Simular fallo de negocio (ej. el calendario no existe en DB)
        if isinstance(created_entry, Exception):
            raise created_entry
            
        return created_entry

# ====================================================================
# 3. FIXTURES DE SIMULACIÓN
# ====================================================================

@pytest.fixture
def mock_schedule_repo():
    return MagicMock(create_entry=MagicMock(return_value=MagicMock()))

@pytest.fixture
def schedule_service(mock_schedule_repo: MagicMock):
    return MockScheduleEntryService(mock_schedule_repo)

# Datos de Bloque de Horario Válido
VALID_SCHEDULE_BLOCKS = [
    {"date": "2023-11-23", "start_time": "09:00:00", "end_time": "10:00:00"}
]

# ====================================================================
# 4. PRUEBAS DE CASOS VÁLIDOS (ÉXITO)
# ====================================================================

@pytest.mark.parametrize("calendar_id, title, description, location", [
    # Caso (1,2,3,4,5): Todos los campos válidos
    (1, "Reunión Semanal", "Discutir el progreso del proyecto.", "Oficina Principal"),
    # Caso (a,2,3,4,5): Calendar ID Válido, Título y descripción válidos
    (60, "Presentación", "Presentación de resultados trimestrales.", "Sala de Conferencias"),
    # Caso (1,c,3,4,5): Título y Descripción en límites
    (1, "A" * 60, "B" * 200, "C" * 40), 
])
def test_casos_uso_validos_success(schedule_service: MockScheduleEntryService, mock_schedule_repo: MagicMock, 
                                   calendar_id: int, title: str, description: str, location: str):
    
    entry_data = CreateScheduleEntrySchema(calendar_id, title, description, location, VALID_SCHEDULE_BLOCKS)
    
    # Simular que el repositorio devuelve un objeto exitoso
    mock_schedule_repo.create_entry.return_value = MagicMock()

    schedule_service.create_schedule_entry(entry_data)
    
    mock_schedule_repo.create_entry.assert_called_once_with(entry_data)
    mock_schedule_repo.create_entry.reset_mock()


# ====================================================================
# 5. PRUEBAS DE CASOS NO VÁLIDOS (FALLO)
# ====================================================================

@pytest.mark.parametrize("calendar_id, title, description, location, schedule_blocks, expected_error", [
    # (b,2,3,4,5): Calendario > 60
    (61, "Titulo A", "Desc A", "Loc A", VALID_SCHEDULE_BLOCKS, "VALIDATION_CALENDAR_RANGE"),
    # (1,c,3,4,5): Título vacío
    (1, "", "Desc B", "Loc B", VALID_SCHEDULE_BLOCKS, "VALIDATION_TITLE_EMPTY"),
    # (1,d,3,4,5): Título > 60
    (1, "T" * 61, "Desc C", "Loc C", VALID_SCHEDULE_BLOCKS, "VALIDATION_TITLE_RANGE"),
    # (1,2,e,4,5): Descripción vacío
    (1, "Titulo D", "", "Loc D", VALID_SCHEDULE_BLOCKS, "VALIDATION_DESCRIPTION_EMPTY"),
    # (1,2,f,4,5): Descripción > 200
    (1, "Titulo E", "D" * 201, "Loc E", VALID_SCHEDULE_BLOCKS, "VALIDATION_DESCRIPTION_RANGE"),
    # (1,2,3,h,5): Ubicación vacío
    (1, "Titulo F", "Desc F", "", VALID_SCHEDULE_BLOCKS, "VALIDATION_LOCATION_EMPTY"),
    # (1,2,3,g,5): Ubicación > 40
    (1, "Titulo G", "Desc G", "L" * 41, VALID_SCHEDULE_BLOCKS, "VALIDATION_LOCATION_RANGE"),
    # (1,2,3,4,5) pero Bloque de horario no válido (ej. vacío)
    (1, "Titulo H", "Desc H", "Loc H", [], "VALIDATION_BLOCKS_EMPTY"),
    # Caso extra: Bloque de horario con hora inválida (Start >= End)
    (1, "Titulo I", "Desc I", "Loc I", [{"date": "2023-11-23", "start_time": "10:00:00", "end_time": "09:00:00"}], 
     "VALIDATION_BLOCKS_TIME_INVALID"),
])
def test_clases_no_validas_combinations(schedule_service: MockScheduleEntryService, mock_schedule_repo: MagicMock,
                                        calendar_id: int, title: str, description: str, location: str, 
                                        schedule_blocks: list, expected_error: str):
    """Prueba todas las combinaciones de Clases No Válidas especificadas en el Excel."""
    
    entry_data = CreateScheduleEntrySchema(calendar_id, title, description, location, schedule_blocks)
    
    with pytest.raises(CustomException, match=expected_error):
        schedule_service.create_schedule_entry(entry_data)
        
    mock_schedule_repo.create_entry.assert_not_called()

# ====================================================================
# 6. PRUEBA DE FALLO DE NEGOCIO (Repositorio)
# ====================================================================

def test_fallo_de_negocio_repo_error(schedule_service: MockScheduleEntryService, mock_schedule_repo: MagicMock):
    """
    Simula una falla en el repositorio (ej. el calendar_id no existe en la DB).
    """
    valid_data = CreateScheduleEntrySchema(1, "Valid", "Valid", "Valid", VALID_SCHEDULE_BLOCKS)
    
    # Simular que el repositorio devuelve una excepción (fallo de negocio)
    mock_schedule_repo.create_entry.return_value = Exception("CALENDAR_NOT_FOUND_DB")
    
    with pytest.raises(Exception, match="CALENDAR_NOT_FOUND_DB"):
        schedule_service.create_schedule_entry(valid_data)
    
    mock_schedule_repo.create_entry.assert_called_once()