from factories.base import BaseFactory
from communication_services.base import BaseCommunicationService


class CommunicationServiceFactory(BaseFactory):
    registry = {}
    discovery_path = 'communication_services'
    base_class = BaseCommunicationService
