from faker import Faker
from tests.basetest import BaseTest

from scalekit.v1.roles.roles_pb2 import CreateRole, UpdateRole
from scalekit.v1.users.users_pb2 import CreateUser, CreateUserProfile, CreateMembership
from scalekit.v1.commons.commons_pb2 import Role
from scalekit.v1.organizations.organizations_pb2 import CreateOrganization


class TestRoles(BaseTest):
    """ Class definition for Test Roles Class """

    def setUp(self):
        """ """
        self.role_id = None
        self.faker = Faker()
        self.user_id = None
        
        # Always create a test organization for this test
        org_display_name = f"Test Organization {self.faker.unique.random_number()}"
        org = CreateOrganization(
            display_name=org_display_name,
            external_id=f"ext_{self.faker.unique.random_number()}"
        )
        org_response = self.scalekit_client.organization.create_organization(organization=org)
        self.org_id = org_response[0].organization.id

    def test_create_role(self):
        """ Method to test create role """
        role_name = f"test_role_{self.faker.unique.random_number()}"
        display_name = f"Test Role {self.faker.unique.random_number()}"
        description = "Test role for unit testing"
        
        role = CreateRole(
            name=role_name,
            display_name=display_name,
            description=description,
            default_creator=False,
            default_member=False
        )
        
        response = self.scalekit_client.roles.create_role(role=role)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].role.name, role_name)
        self.assertEqual(response[0].role.display_name, display_name)
        self.assertEqual(response[0].role.description, description)
        self.assertEqual(response[0].role.default_creator, False)
        self.assertEqual(response[0].role.default_member, False)
        self.role_id = response[0].role.id

    def test_create_role_with_default_flags(self):
        """ Method to test create role with default flags """
        role_name = f"test_default_role_{self.faker.unique.random_number()}"
        display_name = f"Test Default Role {self.faker.unique.random_number()}"
        
        role = CreateRole(
            name=role_name,
            display_name=display_name,
            description="Test default role",
            default_creator=False,
            default_member=False
        )
        print("CreateRole", role)
        
        response = self.scalekit_client.roles.create_role(role=role)
        print("CreateRole response", response)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].role.name, role_name)
        self.assertEqual(response[0].role.default_creator, False)
        self.assertEqual(response[0].role.default_member, False)
        self.role_id = response[0].role.id

    def test_get_role(self):
        """ Method to test get role """
        role_name = f"test_role_{self.faker.unique.random_number()}"
        display_name = f"Test Role {self.faker.unique.random_number()}"
        
        role = CreateRole(
            name=role_name,
            display_name=display_name,
            description="Test role for get operation"
        )
        
        create_response = self.scalekit_client.roles.create_role(role=role)
        self.role_id = create_response[0].role.id

        response = self.scalekit_client.roles.get_role(role_id=self.role_id)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].role.id, self.role_id)
        self.assertEqual(response[0].role.name, role_name)
        self.assertEqual(response[0].role.display_name, display_name)
        self.assertEqual(response[0].role.description, "Test role for get operation")

    def test_list_roles(self):
        """ Method to test list roles """
        role_name = f"test_role_{self.faker.unique.random_number()}"
        display_name = f"Test Role {self.faker.unique.random_number()}"
        
        role = CreateRole(
            name=role_name,
            display_name=display_name,
            description="Test role for list operation"
        )
        
        create_response = self.scalekit_client.roles.create_role(role=role)
        self.role_id = create_response[0].role.id

        response = self.scalekit_client.roles.list_roles()
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(len(response[0].roles) > 0)
        
        # Verify our created role is in the list
        found_role = None
        for role_item in response[0].roles:
            if role_item.id == self.role_id:
                found_role = role_item
                break
        
        self.assertIsNotNone(found_role)
        self.assertEqual(found_role.name, role_name)
        self.assertEqual(found_role.display_name, display_name)

    def test_update_role(self):
        """ Method to test update role """
        role_name = f"test_role_{self.faker.unique.random_number()}"
        display_name = f"Test Role {self.faker.unique.random_number()}"
        
        role = CreateRole(
            name=role_name,
            display_name=display_name,
            description="Original description"
        )
        
        create_response = self.scalekit_client.roles.create_role(role=role)
        self.role_id = create_response[0].role.id
        print("CreateRole for update response", create_response)

        # Update the role
        updated_display_name = f"Updated Role {self.faker.unique.random_number()}"
        updated_description = "Updated description for testing"
        
        update_role = UpdateRole(
            display_name=updated_display_name,
            description=updated_description,
            default_creator=False,
            default_member=False
        )
        print("UpdateRole", update_role)
        
        response = self.scalekit_client.roles.update_role(
            role_id=self.role_id,
            role=update_role
        )
        print("UpdateRole response", response)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].role.id, self.role_id)
        self.assertEqual(response[0].role.name, role_name)  # Name should not change
        self.assertEqual(response[0].role.display_name, updated_display_name)
        self.assertEqual(response[0].role.description, updated_description)
        self.assertEqual(response[0].role.default_creator, False)
        self.assertEqual(response[0].role.default_member, False)

    def test_update_role_partial(self):
        """ Method to test update role with partial fields """
        role_name = f"test_role_{self.faker.unique.random_number()}"
        display_name = f"Test Role {self.faker.unique.random_number()}"
        
        role = CreateRole(
            name=role_name,
            display_name=display_name,
            description="Original description"
        )
        
        create_response = self.scalekit_client.roles.create_role(role=role)
        self.role_id = create_response[0].role.id

        # Update only display name
        updated_display_name = f"Partial Update Role {self.faker.unique.random_number()}"
        update_role = UpdateRole(display_name=updated_display_name)
        
        response = self.scalekit_client.roles.update_role(
            role_id=self.role_id,
            role=update_role
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].role.id, self.role_id)
        self.assertEqual(response[0].role.display_name, updated_display_name)
        self.assertEqual(response[0].role.description, "Original description")  # Should remain unchanged

    def test_delete_role(self):
        """ Method to test delete role """
        role_name = f"test_role_{self.faker.unique.random_number()}"
        display_name = f"Test Role {self.faker.unique.random_number()}"
        
        role = CreateRole(
            name=role_name,
            display_name=display_name,
            description="Test role for deletion"
        )
        
        create_response = self.scalekit_client.roles.create_role(role=role)
        self.role_id = create_response[0].role.id

        response = self.scalekit_client.roles.delete_role(role_id=self.role_id)
        self.assertEqual(response[1].code().name, "OK")

        # Verify role is deleted by trying to get it
        try:
            self.scalekit_client.roles.get_role(role_id=self.role_id)
            self.fail("Role should have been deleted")
        except Exception as exp:
            # Expected behavior - role should not be found
            self.assertTrue("not found" in str(exp) or "does not exist" in str(exp))
            self.role_id = None

    def test_delete_role_with_reassignment(self):
        """ Method to test delete role with reassignment """
        # Create first role
        role1_name = f"test_role_1_{self.faker.unique.random_number()}"
        role1 = CreateRole(
            name=role1_name,
            display_name=f"Test Role 1 {self.faker.unique.random_number()}",
            description="First test role"
        )
        
        create_response1 = self.scalekit_client.roles.create_role(role=role1)
        role1_id = create_response1[0].role.id

        # Create user and assign to the first role
        user1_profile = CreateUserProfile(
            first_name="Test",
            last_name="User1",
            name="Test User 1",
            locale="en-US"
        )
        user1 = CreateUser(
            email=f"test.user1.{self.faker.unique.random_number()}@example.com",
            user_profile=user1_profile,
            membership=CreateMembership(
                roles=[Role(id=role1_id, name=role1_name)]
            )
        )
        
        user1_response = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id,
            user=user1
        )
        self.user_id = user1_response[0].user.id

        # Try to delete the first role WITHOUT reassignment - this should fail
        try:
            self.scalekit_client.roles.delete_role(role_id=role1_id)
            self.fail("Role deletion should have failed because it has users assigned")
        except Exception as exp:
            # Expected behavior - should fail because role has users
            print(f"Expected error when deleting role with users: {exp}")
            # Assert the specific error message
            self.assertEqual(str(exp), "role cannot be deleted as it is assigned to users")

        # Create second role for reassignment
        role2_name = f"test_role_2_{self.faker.unique.random_number()}"
        role2 = CreateRole(
            name=role2_name,
            display_name=f"Test Role 2 {self.faker.unique.random_number()}",
            description="Second test role for reassignment"
        )
        
        create_response2 = self.scalekit_client.roles.create_role(role=role2)
        role2_id = create_response2[0].role.id

        # Delete first role with reassignment to second role 
        response = self.scalekit_client.roles.delete_role(
            role_id=role1_id,
            reassign_role_id=role2_id
        )
        self.assertEqual(response[1].code().name, "OK")

        # Verify first role is deleted
        try:
            self.scalekit_client.roles.get_role(role_id=role1_id)
            self.fail("Role should have been deleted")
        except Exception as exp:
            # Expected behavior - role should not be found
            self.assertTrue("not found" in str(exp) or "does not exist" in str(exp))

        # Verify second role still exists
        get_response = self.scalekit_client.roles.get_role(role_id=role2_id)
        self.assertEqual(get_response[1].code().name, "OK")
        self.assertEqual(get_response[0].role.id, role2_id)

        # Clean up user
        if self.user_id:
            try:
                self.scalekit_client.users.delete_membership(
                    organization_id=self.org_id,
                    user_id=self.user_id
                )
            except Exception as exp:
                exp_message = str(exp).lower()
                if "not found" in exp_message or "does not exist" in exp_message:
                    # User already deleted or doesn't exist
                    pass
                else:
                    # Log warning but don't fail the test
                    print(f"Warning: Could not clean up user {self.user_id}: {exp}")
            self.user_id = None

        # Clean up second role
        self.scalekit_client.roles.delete_role(role_id=role2_id)

    def test_create_role_validation(self):
        """ Method to test role creation validation """
        # Test with missing required fields
        role = CreateRole(
            display_name="Test Role without name"
            # Missing name field
        )
        
        try:
            self.scalekit_client.roles.create_role(role=role)
            self.fail("Should have failed due to missing name")
        except Exception as exp:
            # Expected behavior - validation error
            self.assertTrue("name" in str(exp).lower() or "required" in str(exp).lower())

    def test_role_name_uniqueness(self):
        """ Method to test role name uniqueness """
        role_name = f"unique_test_role_{self.faker.unique.random_number()}"
        
        role1 = CreateRole(
            name=role_name,
            display_name=f"Test Role 1 {self.faker.unique.random_number()}",
            description="First role with same name"
        )
        
        role2 = CreateRole(
            name=role_name,  # Same name
            display_name=f"Test Role 2 {self.faker.unique.random_number()}",
            description="Second role with same name"
        )
        
        # Create first role
        create_response1 = self.scalekit_client.roles.create_role(role=role1)
        self.assertEqual(create_response1[1].code().name, "OK")
        role1_id = create_response1[0].role.id

        # Try to create second role with same name
        try:
            self.scalekit_client.roles.create_role(role=role2)
            self.fail("Should have failed due to duplicate name")
        except Exception as exp:
            # Expected behavior - duplicate name error
            self.assertTrue("already exists" in str(exp) or "duplicate" in str(exp) or "unique" in str(exp))

        # Clean up first role
        self.scalekit_client.roles.delete_role(role_id=role1_id)

    def test_get_role_users_count(self):
        """ Method to test get role users count """
        role_name = f"test_role_{self.faker.unique.random_number()}"
        display_name = f"Test Role {self.faker.unique.random_number()}"
        
        role = CreateRole(
            name=role_name,
            display_name=display_name,
            description="Test role for user count"
        )
        
        create_response = self.scalekit_client.roles.create_role(role=role)
        self.role_id = create_response[0].role.id

        # Get user count for the role
        response = self.scalekit_client.roles.get_role_users_count(role_id=self.role_id)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertIsInstance(response[0].count, int)
        self.assertGreaterEqual(response[0].count, 0)

    def tearDown(self):
        """ Method to clean up """
        if self.role_id:
            try:
                self.scalekit_client.roles.delete_role(role_id=self.role_id)
            except Exception as exp:
                exp_message = str(exp).lower()
                
                # Check for expected "not found" scenarios
                if "not found" in exp_message or "does not exist" in exp_message:
                    # Role already deleted or doesn't exist 
                    pass
                else:
                    # Fail the test for unexpected exceptions during cleanup
                    raise Exception(f"Unexpected exception during role cleanup: {exp}") from exp
        
        # Clean up created organization
        try:
            self.scalekit_client.organization.delete_organization(organization_id=self.org_id)
        except Exception as exp:
            exp_message = str(exp).lower()
            if "not found" in exp_message or "does not exist" in exp_message:
                # Organization already deleted or doesn't exist
                pass
            else:
                print(f"Warning: Could not clean up organization {self.org_id}: {exp}") 