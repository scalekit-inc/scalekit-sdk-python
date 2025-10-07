#!/usr/bin/env python3
"""
Comprehensive examples of how to call ScaleKit User APIs
This file demonstrates all available user management operations.
"""

import os
from scalekit import ScalekitClient
from scalekit.v1.users.users_pb2 import (
    CreateUser, 
    CreateUserProfile, 
    UpdateUser, 
    UpdateUserProfile,
    CreateMembership,
    UpdateMembership
)
from scalekit.v1.commons.commons_pb2 import Role


def initialize_client():
    """Initialize the ScaleKit client"""
    env_url = os.environ.get('SCALEKIT_ENV_URL', 'https://your-env.scalekit.com')
    client_id = os.environ.get('SCALEKIT_CLIENT_ID', 'your_client_id')
    client_secret = os.environ.get('SCALEKIT_CLIENT_SECRET', 'your_client_secret')
    
    return ScalekitClient(env_url, client_id, client_secret)


def example_create_user_and_membership(client, organization_id):
    """Example: Create a new user and add them to an organization"""
    print("=== Creating User and Membership ===")
    
    # Create user profile
    profile = CreateUserProfile(
        first_name="John",
        last_name="Doe",
        name="John Doe",
        locale="en-US",
        phone_number="+14155552671"
    )
    
    # Create user
    user = CreateUser(
        email="john.doe@example.com",
        external_id="ext_user_12345",
        user_profile=profile,
        metadata={
            "department": "engineering",
            "location": "nyc-office",
            "employee_id": "EMP001"
        }
    )
    
    # Create user and add to organization
    response = client.users.create_user_and_membership(
        organization_id=organization_id,
        user=user,
        send_invitation_email=True
    )
    
    print(f"✅ User created successfully!")
    print(f"   User ID: {response.user.id}")
    print(f"   Email: {response.user.email}")
    print(f"   External ID: {response.user.external_id}")
    print(f"   Name: {response.user.user_profile.first_name} {response.user.user_profile.last_name}")
    
    return response.user.id


def example_get_user(client, user_id):
    """Example: Get user details by ID"""
    print("\n=== Getting User Details ===")
    
    response = client.users.get_user(user_id=user_id)
    
    print(f"✅ User retrieved successfully!")
    print(f"   User ID: {response.user.id}")
    print(f"   Email: {response.user.email}")
    print(f"   External ID: {response.user.external_id}")
    print(f"   Created: {response.user.create_time}")
    print(f"   Last Updated: {response.user.update_time}")
    print(f"   Metadata: {dict(response.user.metadata)}")
    
    return response.user


def example_get_user_by_external_id(client, external_id):
    """Example: Get user details by external ID"""
    print("\n=== Getting User by External ID ===")
    
    response = client.users.get_user_by_external_id(external_id=external_id)
    
    print(f"✅ User retrieved by external ID!")
    print(f"   User ID: {response.user.id}")
    print(f"   Email: {response.user.email}")
    print(f"   External ID: {response.user.external_id}")
    
    return response.user


def example_update_user(client, user_id):
    """Example: Update user information"""
    print("\n=== Updating User ===")
    
    # Create update profile
    update_profile = UpdateUserProfile(
        first_name="John Updated",
        last_name="Doe Updated",
        name="John Updated Doe",
        locale="en-GB",
        phone_number="+14155552672"
    )
    
    # Create update user object
    update_user = UpdateUser(
        external_id="ext_user_12345_updated",
        user_profile=update_profile,
        metadata={
            "department": "product",
            "location": "sf-office",
            "employee_id": "EMP001",
            "level": "senior"
        }
    )
    
    response = client.users.update_user(user_id=user_id, user=update_user)
    
    print(f"✅ User updated successfully!")
    print(f"   Updated Name: {response.user.user_profile.first_name} {response.user.user_profile.last_name}")
    print(f"   Updated External ID: {response.user.external_id}")
    print(f"   Updated Metadata: {dict(response.user.metadata)}")
    
    return response.user


def example_list_users(client):
    """Example: List all users in environment"""
    print("\n=== Listing All Users ===")
    
    response = client.users.list_users(page_size=10)
    
    print(f"✅ Users listed successfully!")
    print(f"   Total users: {response.total_size}")
    print(f"   Users in this page: {len(response.users)}")
    print(f"   Next page token: {response.next_page_token}")
    
    for user in response.users:
        print(f"   - {user.email} (ID: {user.id})")
    
    return response


def example_list_organization_users(client, organization_id):
    """Example: List users in a specific organization"""
    print("\n=== Listing Organization Users ===")
    
    response = client.users.list_organization_users(
        organization_id=organization_id,
        page_size=20
    )
    
    print(f"✅ Organization users listed successfully!")
    print(f"   Total users in org: {response.total_size}")
    print(f"   Users in this page: {len(response.users)}")
    
    for user in response.users:
        print(f"   - {user.email} (ID: {user.id})")
    
    return response


def example_create_membership(client, organization_id, user_id):
    """Example: Create membership for existing user"""
    print("\n=== Creating Membership ===")
    
    # Create membership with roles
    membership = CreateMembership(
        roles=[Role(name="admin"), Role(name="viewer")],
        metadata={
            "department": "engineering",
            "team": "backend"
        },
        inviter_email="admin@example.com"
    )
    
    response = client.users.create_membership(
        organization_id=organization_id,
        user_id=user_id,
        membership=membership,
        send_invitation_email=False
    )
    
    print(f"✅ Membership created successfully!")
    print(f"   User ID: {response.user.id}")
    print(f"   Memberships: {len(response.user.memberships)}")
    
    return response.user


def example_update_membership(client, organization_id, user_id):
    """Example: Update user membership"""
    print("\n=== Updating Membership ===")
    
    # Update membership
    membership = UpdateMembership(
        roles=[Role(name="admin"), Role(name="editor")],
        metadata={
            "department": "product",
            "team": "frontend",
            "level": "senior"
        }
    )
    
    response = client.users.update_membership(
        organization_id=organization_id,
        user_id=user_id,
        membership=membership
    )
    
    print(f"✅ Membership updated successfully!")
    print(f"   User ID: {response.user.id}")
    
    return response.user


def example_resend_invite(client, organization_id, user_id):
    """Example: Resend invitation email"""
    print("\n=== Resending Invitation ===")
    
    response = client.users.resend_invite(
        organization_id=organization_id,
        user_id=user_id
    )
    
    print(f"✅ Invitation resent successfully!")
    print(f"   Invite status: {response.invite.status}")
    print(f"   Resend count: {response.invite.resent_count}")
    
    return response.invite


def example_delete_membership(client, organization_id, user_id):
    """Example: Delete user membership"""
    print("\n=== Deleting Membership ===")
    
    client.users.delete_membership(
        organization_id=organization_id,
        user_id=user_id
    )
    
    print(f"✅ Membership deleted successfully!")
    
    return True


def example_delete_user(client, user_id):
    """Example: Delete user permanently"""
    print("\n=== Deleting User ===")
    
    client.users.delete_user(user_id=user_id)
    
    print(f"✅ User deleted successfully!")
    
    return True


def main():
    """Main function demonstrating all user API calls"""
    print("🚀 ScaleKit User API Examples")
    print("=" * 50)
    
    # Initialize client
    client = initialize_client()
    
    # You'll need to replace this with an actual organization ID
    organization_id = "org_your_organization_id"
    
    try:
        # 1. Create user and membership
        user_id = example_create_user_and_membership(client, organization_id)
        
        # 2. Get user details
        user = example_get_user(client, user_id)
        
        # 3. Get user by external ID
        example_get_user_by_external_id(client, user.external_id)
        
        # 4. Update user
        updated_user = example_update_user(client, user_id)
        
        # 5. List all users
        example_list_users(client)
        
        # 6. List organization users
        example_list_organization_users(client, organization_id)
        
        # 7. Create additional membership
        example_create_membership(client, organization_id, user_id)
        
        # 8. Update membership
        example_update_membership(client, organization_id, user_id)
        
        # 9. Resend invitation
        example_resend_invite(client, organization_id, user_id)
        
        # 10. Delete membership (optional - uncomment if needed)
        # example_delete_membership(client, organization_id, user_id)
        
        # 11. Delete user (optional - uncomment if needed)
        # example_delete_user(client, user_id)
        
        print("\n✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
