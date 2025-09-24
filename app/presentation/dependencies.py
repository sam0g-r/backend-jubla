from typing import Generator
from app.application.use_cases.user_use_cases import UserUseCases
from app.application.use_cases.event_use_cases import EventUseCases
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.event_repository_impl import EventRepositoryImpl
from app.application.use_cases.location_use_cases import LocationUseCases
from app.infrastructure.repositories.country_repository_impl import CountryRepositoryImpl
from app.infrastructure.repositories.state_repository_impl import StateRepositoryImpl
from app.infrastructure.repositories.city_repository_impl import CityRepositoryImpl
from app.infrastructure.services.supertokens_user_signup import SuperTokensUserSignUp

# Aquí se configurarían las dependencias reales cuando se implementen los repositorios
# Por ahora son placeholders

def get_user_repository() -> UserRepositoryImpl:
    # Aquí se configuraría la conexión a la base de datos
    return UserRepositoryImpl()

def get_event_repository() -> EventRepositoryImpl:
    # Aquí se configuraría la conexión a la base de datos
    return EventRepositoryImpl()

def get_user_sevice() -> SuperTokensUserSignUp:
    return SuperTokensUserSignUp()

def get_user_use_cases() -> UserUseCases:
    user_repository = get_user_repository()
    user_service = get_user_sevice()
    return UserUseCases(user_repository, user_service)

def get_event_use_cases() -> EventUseCases:
    event_repository = get_event_repository()
    return EventUseCases(event_repository) 


def get_location_use_cases() -> LocationUseCases:
    country_repo = CountryRepositoryImpl()
    state_repo = StateRepositoryImpl()
    city_repo = CityRepositoryImpl()
    return LocationUseCases(country_repo, state_repo, city_repo)