Organization represents a customer or a tenant of your product. This is the top level entity and all the resources are mapped to this Organization object. Each organization will be uniquely identified by `organization_id`. You can use this service to create and manage Enterprise SSO Connections for an organization.

**Attributes**

| Attribute Name | Attribute Description |
|---|---|
| `id`<br>_string_ | Unique ID of an Organization. This attribute is required for all API operations to be performed against this organization.  |
| `display_name`<br>_string_ | Name of the Organization |
| `create_time`<br>_string_ | Timestamp at which this organization record was created in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format. For Example: `2011-10-05T14:48:00.000Z` |
| `update_time`<br>_string_ | Timestamp at which this organization record was last updated in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format. For Example: <br>`2021-10-05T14:48:00.000Z` |
| `external_id`<br>_string_ | Unique ID of this organization according to your system. You can store your unique ID for this organization in Scalekit's system and later use this to fetch Organization and Connection details. This is helpful if you don't want to persist Scalekit's Unique Identifiers in your database. |
| `metadata`<br>_object_ | JSON representation of any additional organization information that you want to store in Scalekit's system. Example: `{"key":"value"}` |
| `region_code`<br>_string_ | Represents the Data Center region in which this organization's data is stored. Currently, it always returns `US` |