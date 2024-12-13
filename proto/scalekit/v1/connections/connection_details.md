 Connection represents a unique Single Sign-on instance for an Organization. Connection has the configuration needed to establish an SSO and exchange user information securely between Scalekit and your customer's Identity Provider. Depending on the connection type parameter, the corresponding configuration details are found in `oidc_config` or `saml_config` parameter.

**Connection Attributes**

| Attribute Name | Attribute Description |
|---|---|
| `id`<br>_string_ | Unique ID of an SSO Connection. This attribute is required for all API operations to be performed against this connection.  |
| `provider`<br>_ENUM_ | Name of the Identity Provider. Possible Values are: `OKTA`, `GOOGLE`, `MICROSOFT_AD`, `AUTH0`, `ONELOGIN`, `PING_IDENTITY`, `JUMPCLOUD`, `CUSTOM` |
| `type`<br>_ENUM_ | Protocol type that is used for this connection. Possible values are `SAML` or `OIDC` |
| `status`<br>_ENUM_ | Indicates the configuration progress status of the SSO Connection. Possible Values are `DRAFT`, `INPROGRESS`, `COMPLETED`. <br>_Note_: This doesn't indicate whether this connection is active or not. |
| `enabled`<br>_boolean_ | Indicates whether this connection is active or not. Users can only login via active SSO connections. |
| `organization_id`<br>_string_ | Organization ID to which this SSO connection belongs to. |
| `saml_config`<br>_Object_ | If this connection is of type `SAML`, the configuration details are found in this object. |
| `oidc_config`<br>_Object_ | If this connection is of type `OIDC`, the configuration details are found in this object. |
| `attribute_mapping`<br>_Object_ | Array of attribute mappings using which the user information received from the Identity Provider is normalized. Example: <code> <br/>{ <br/>&nbsp;&nbsp; "email": "email",<br/>&nbsp;&nbsp; "family_name": "lastName", <br/>&nbsp;&nbsp; "given_name": "firstName",<br/>&nbsp;&nbsp;&nbsp;"sub": "nameid" <br/>} </code> |
| `create_time` | Timestamp at which this connection record was created in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format. For Example: `2021-10-05T14:48:00.000Z` |
| `update_time`<br>_string_ | Timestamp at which this connection record was last updated in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format. For Example: `2021-10-10T14:48:00.000Z` |