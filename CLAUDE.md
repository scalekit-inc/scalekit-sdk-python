# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is the official Python SDK for Scalekit, an Enterprise Authentication Platform for B2B applications. The SDK provides functionality for implementing Single Sign-On (SSO) via SAML or OIDC, managing organizations, users, connections, and more.

## Development Commands

### Installation and Setup
```bash
# Install dependencies
python3 setup.py install

# Install from PyPI
pip install scalekit-sdk-python
```

### Testing
```bash
# Run all tests
python3 -m unittest discover -s tests

# Run specific test file
python3 -m unittest discover -s tests -p "test_file_name.py"
```

### Protocol Buffer Generation
```bash
# Generate protobuf files (requires proto directory path)
make all
```

The makefile handles:
- Copying proto files from specified directory
- Running `buf generate --include-imports` to generate Python protobuf files
- Creating `__init__.py` files for proper Python module structure
- Cleaning up temporary files

## Architecture

### Core Components

1. **ScalekitClient** (`scalekit/client.py`): Main SDK entry point
   - Handles authentication flows (OAuth/OIDC)
   - Manages JWT token validation
   - Provides webhook verification
   - Coordinates all sub-clients

2. **CoreClient** (`scalekit/core.py`): Low-level HTTP/gRPC client
   - Manages authentication with Scalekit API
   - Handles gRPC secure channel setup
   - Provides common headers and error handling
   - Manages JWKS key retrieval

3. **Domain-specific Clients**: Each handles specific API domains
   - `DomainClient`: Domain management
   - `ConnectionClient`: SSO connection management
   - `OrganizationClient`: Organization CRUD operations
   - `DirectoryClient`: Directory/user provisioning
   - `UserClient`: User management
   - `RoleClient`: Role-based access control
   - `M2MClient`: Machine-to-machine authentication
   - `ConnectedAccountsClient`: Connected accounts management

### Protocol Buffers Structure
- `scalekit/v1/`: Generated protobuf files organized by domain
- Each domain has `*_pb2.py` (messages), `*_pb2.pyi` (type stubs), and `*_pb2_grpc.py` (gRPC stubs)
- Common types in `scalekit/v1/commons/`

### Key Design Patterns

1. **Client Composition**: ScalekitClient composes domain-specific clients
2. **Shared CoreClient**: All clients use the same CoreClient instance for consistency
3. **gRPC with HTTP fallback**: Primary communication via gRPC with REST endpoints for auth
4. **JWT Validation**: Built-in token validation using JWKS
5. **Error Handling**: Structured error responses with validation details

## Environment Setup

### Required Environment Variables
```bash
DEV_SCALEKIT_ENV_URL=https://your-env.scalekit.com
DEV_SCALEKIT_CLIENT_ID=your_client_id
DEV_SCALEKIT_CLIENT_SECRET=your_client_secret
```

### Typical Usage Pattern
```python
from scalekit import ScalekitClient

# Initialize client
sc = ScalekitClient(env_url, client_id, client_secret)

# Use domain-specific functionality
auth_url = sc.get_authorization_url(redirect_uri, options)
token_response = sc.authenticate_with_code(code, redirect_uri, options)
organizations = sc.organization.list_organizations()
connected_accounts = sc.connected_accounts.list_connected_accounts(org_id, user_id)
```

## Dependencies
- **grpcio**: gRPC communication
- **protobuf**: Protocol buffer serialization  
- **PyJWT**: JWT token handling
- **requests**: HTTP client
- **cryptography**: Cryptographic operations
- **python-dotenv**: Environment variable management

## Testing Notes
- Tests require environment variables to be set
- Uses Python unittest framework
- Test files follow `test_*.py` naming convention
- Base test class in `tests/basetest.py` provides common setup