
from typing import Optional, Union

from scalekit.core import CoreClient
from scalekit.v1.domains.domains_pb2 import *
from scalekit.v1.domains.domains_pb2_grpc import DomainServiceStub


# String to enum mapping for domain types
_DOMAIN_TYPE_MAP = {
    "UNSPECIFIED": DomainType.DOMAIN_TYPE_UNSPECIFIED,
    "ALLOWED_EMAIL_DOMAIN": DomainType.ALLOWED_EMAIL_DOMAIN,
    "ORGANIZATION_DOMAIN": DomainType.ORGANIZATION_DOMAIN,
}

def _convert_domain_type(domain_type: Union[str, "DomainType", None]) -> Optional["DomainType"]:
    """Convert string or enum to DomainType enum"""
    if domain_type is None:
        return None
    if isinstance(domain_type, str):
        domain_type_upper = domain_type.upper()
        if domain_type_upper in _DOMAIN_TYPE_MAP:
            return _DOMAIN_TYPE_MAP[domain_type_upper]
        else:
            raise ValueError(f"Invalid domain type: {domain_type}. Valid options are: {list(_DOMAIN_TYPE_MAP.keys())}")
    return domain_type


class DomainClient:
    """Class definition for Domain Client"""

    def __init__(self, core_client: CoreClient):
        """
        Initializer for Domain Client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.domain_service = DomainServiceStub(
            self.core_client.grpc_secure_channel
        )

    def create_domain(
        self, organization_id: str, domain_name: str, domain_type: Optional[Union[str, "DomainType"]] = None
    ) -> CreateDomainResponse:
        """
        Method to create domain

        :param organization_id  : Organization id to create domain for
        :type                   : ``` str ```
        :param domain_name      : Domain name for new creation
        :type                   : ``` str ```
        :param domain_type      : Type of domain ("ALLOWED_EMAIL_DOMAIN", "ORGANIZATION_DOMAIN", or "UNSPECIFIED")
        :type                   : ``` str or DomainType ```

        :returns
            Domain Response
        """
        # Convert domain_type string to enum if needed
        domain_type_enum = _convert_domain_type(domain_type)
        
        return self.core_client.grpc_exec(
            self.domain_service.CreateDomain.with_call,
            CreateDomainRequest(
                organization_id=organization_id,
                domain=CreateDomain(
                    domain=domain_name,
                    domain_type=domain_type_enum
                ),
            ),
        )

    def list_domains(self, organization_id: str) -> ListDomainResponse:
        """
        Method to list existing domains

        :param organization_id  : Organization id to list domains for
        :type                   : ``` str ```
        :returns
            List Domain Response
        """
        return self.core_client.grpc_exec(
            self.domain_service.ListDomains.with_call,
            ListDomainRequest(organization_id=organization_id),
            )

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
        return self.core_client.grpc_exec(
            self.domain_service.GetDomain.with_call,
            GetDomainRequest(organization_id=organization_id, id=domain_id),
        )
    
    def delete_domain(self, organization_id: str, domain_id: str): 
        """
        Method to delete domain

        :param organization_id  : Organization id to delete domain for
        :type                   : ``` str ```
        :param domain_id        : Domain id to delete
        :type                   : ``` str ```
        :returns
            None
        """
        return self.core_client.grpc_exec(
            self.domain_service.DeleteDomain.with_call,
            DeleteDomainRequest(organization_id=organization_id, id=domain_id),
        )
