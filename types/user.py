

class User:
    def __init__(self):
        """ """
        self.id = str
        self.username = str | None
        self.name = str
        self.given_name = str
        self.family_name = str | None
        self.email = ''
        self.email_verified = bool
        self.phone_number = str | None
        self.phone_number_verified = bool | None
        self.profile = str | None
        self.picture = str | None
        self.gender = str | None
        self.birth_date = str | None
        self.zone_info = str | None
        self.locale = str | None
        self.updated_at = str | None
        self.identities = Identity()
        self.metadata = str | None


class Identity:
    def __init__(self):
        """ """
        self.connection_id = str
        self.organization_id = str
        self.connection_type = str
        self.provider_name = str
        self.social = bool
        self.provider_raw_attributes = str


class IdTokenClaimIdentity:
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
        """ """
        self.sub = str
        self.name = str
        self.preferred_username = str | None
        self.given_name = str
        self.family_name = str | None
        self.email = str
        self.email_verified = bool
        self.phone_number = str | None
        self.phone_number_verified = bool | None
        self.profile = str | None
        self.picture = str | None
        self.gender = str | None
        self.birth_date = str | None
        self.zone_info = str | None
        self.locale = str | None
        self.updated_at = str | None
        self.identities: IdTokenClaimIdentity()
        self.metadata = str | None
