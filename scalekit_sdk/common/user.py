from typing import Optional


class User:
    def __init__(self):
        """Class definition for user params"""
        self.id: str
        self.username: Optional[str] = None
        self.name: Optional[str] = None
        self.given_name: Optional[str] = None
        self.family_name: Optional[str] = None
        self.email: str
        self.email_verified = bool
        self.phone_number: Optional[str] = None
        self.phone_number_verified = bool | None
        self.profile: Optional[str] = None
        self.picture: Optional[str] = None
        self.gender: Optional[str] = None
        self.birth_date: Optional[str] = None
        self.zone_info: Optional[str] = None
        self.locale: Optional[str] = None
        self.updated_at: Optional[str] = None
        self.identities = Identity()
        self.metadata: Optional[str] = None


class Identity:
    """Class definition for identity params"""

    def __init__(self):
        """ """
        self.connection_id = str
        self.organization_id = str
        self.connection_type = str
        self.provider_name = str
        self.social = bool
        self.provider_raw_attributes = str


class IdTokenClaimIdentity:
    """Class definition for ID token claim identity params"""

    def __init__(self):
        """ """
        self.connection_id = str
        self.organization_id = str
        self.connection_type = str
        self.provider_name = str
        self.social = bool
        self.provider_raw_attributes = str


class IdTokenClaim:
    """ """

    def __init__(self):
        """Class definition for ID token claim params"""
        self.sub = str
        self.name = str
        self.preferred_username: Optional[str] = None
        self.given_name = str
        self.family_name: Optional[str] = None
        self.email = str
        self.email_verified = bool
        self.phone_number: Optional[str] = None
        self.phone_number_verified = bool | None
        self.profile: Optional[str] = None
        self.picture: Optional[str] = None
        self.gender: Optional[str] = None
        self.birth_date: Optional[str] = None
        self.zone_info: Optional[str] = None
        self.locale: Optional[str] = None
        self.updated_at: Optional[str] = None
        self.identities: IdTokenClaimIdentity = None
        self.metadata: Optional[str] = None
