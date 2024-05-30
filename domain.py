import grpc

from core import CoreClient
from pkg.scalekit.v1.domains.domains_pb2_grpc import DomainServiceStub
from pkg.scalekit.v1.domains.domains_pb2 import *


class DomainClient:
    """Class definition for Domain Client"""

    def __init__(self, coreClient: CoreClient):
        """
        Initializer for Domain Client

        :param env_url        : Environment URL
        :type                 : ``` str ```
        :param client_id      : Client ID
        :type                 : ``` str ```
        :param client_secret  : Client Secret
        :type                 : ``` str ```
        :returns
            None
        """
        self.core_client = coreClient
        self.organization_service = DomainServiceStub(
            self.core_client.grpc_secure_channel
        )

    def create_domain(
        self, organization_id: str, domain_name: str
    ) -> CreateDomainResponse:
        """
        Method to create domain

        :param organization_id  : Organization id to create domain for
        :type                   : ``` str ```
        :param domain_name      : Domain name for new creation
        :type                   : ``` str ```
        :returns
            Domain Response
        """
        try:
            return self.core_client.grpc_exec(
                self.domain_service.CreateDomain,
                CreateDomainRequest(
                    organization_id=organization_id,
                    domain=CreateDomain(domain=domain_name),
                ),
            )
        except Exception as exp:
            raise exp

    def list_domains(self, organization_id: str) -> ListDomainResponse:
        """
        Method to list existing domains

        :param organization_id  : Organization id to list domains for
        :type                   : ``` str ```
        :returns
            List Domain Response
        """
        try:
            return self.core_client.grpc_exec(
                self.domain_service.ListDomains,
                ListDomainRequest(organization_id=organization_id),
            )
        except Exception as exp:
            raise exp

    def get_domain(self, organization_id: str, domain_id: str) -> GetDomainResponse:
        """
        Method to list existing domains

        :param organization_id  : Organization id to list domains for
        :type                   : ``` str ```
        :param domain_id        : Domain name for new creation
        :type                   : ``` str ```
        :returns
            Get Domain Response
        """
        try:
            return self.core_client.grpc_exec(
                self.domain_service.GetDomain,
                GetDomainRequest(organization_id=organization_id, id=domain_id),
            )
        except Exception as exp:
            raise exp
