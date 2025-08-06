from typing import Generator
from app.application.use_cases.user_use_cases import UserUseCases
from app.application.use_cases.event_use_cases import EventUseCases
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.event_repository_impl import EventRepositoryImpl

# Aquí se configurarían las dependencias reales cuando se implementen los repositorios
# Por ahora son placeholders

def get_user_repository() -> UserRepositoryImpl:
    # Aquí se configuraría la conexión a la base de datos
    return UserRepositoryImpl()

def get_event_repository() -> EventRepositoryImpl:
    # Aquí se configuraría la conexión a la base de datos
    return EventRepositoryImpl()

def get_user_use_cases() -> UserUseCases:
    user_repository = get_user_repository()
    return UserUseCases(user_repository)

def get_event_use_cases() -> EventUseCases:
    event_repository = get_event_repository()
    return EventUseCases(event_repository) 