from faker import Faker

from scalekit.common.exceptions import ScalekitBadRequestException, ScalekitNotFoundException, ScalekitException
from tests.basetest import BaseTest

from scalekit.v1.roles.roles_pb2 import CreatePermission, CreateRole
from scalekit.v1.organizations.organizations_pb2 import CreateOrganization


class TestPermissions(BaseTest):
    """ Class definition for Test Permissions Class """

    def setUp(self):
        """ """
        self.permission_name = None
        self.role_name = None
        self.faker = Faker()

        # Always create a test organization for this test
        org_display_name = f"Test Organization {self.faker.unique.random_number()}"
        org = CreateOrganization(
            display_name=org_display_name,
            external_id=f"ext_{self.faker.uuid4()}"
        )
        org_response = self.scalekit_client.organization.create_organization(organization=org)
        self.org_id = org_response[0].organization.id

    def test_create_permission(self):
        """ Method to test create permission """
        permission_name = f"test_permission_{self.faker.unique.random_number()}"
        description = "Test permission for unit testing"

        permission = CreatePermission(
            name=permission_name,
            description=description
        )

        response = self.scalekit_client.permissions.create_permission(permission=permission)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].permission.name, permission_name)
        self.assertEqual(response[0].permission.description, description)
        
        # Store for cleanup
        self.permission_name = permission_name

    def test_get_permission(self):
        """ Method to test get permission by name """
        # First create a permission
        permission_name = f"test_permission_{self.faker.unique.random_number()}"
        
        permission = CreatePermission(
            name=permission_name,
            description="Test permission for get test"
        )
        
        create_response = self.scalekit_client.permissions.create_permission(permission=permission)
        self.permission_name = permission_name

        # Now test get permission
        response = self.scalekit_client.permissions.get_permission(permission_name=permission_name)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].permission.name, permission_name)

    def test_get_permission_not_found(self):
        """ Method to test get permission with non-existent name """
        with self.assertRaises(ScalekitNotFoundException):
            self.scalekit_client.permissions.get_permission(permission_name="non_existent_permission")

    def test_list_permissions(self):
        """ Method to test list all permissions """
        response = self.scalekit_client.permissions.list_permissions()
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(hasattr(response[0], 'permissions'))

    def test_list_permissions_with_pagination(self):
        """ Method to test list permissions with pagination """
        response = self.scalekit_client.permissions.list_permissions(page_size=10)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)

    def test_update_permission(self):
        """ Method to test update permission """
        # First create a permission
        permission_name = f"test_permission_{self.faker.unique.random_number()}"
        
        permission = CreatePermission(
            name=permission_name,
            description="Original description"
        )
        
        create_response = self.scalekit_client.permissions.create_permission(permission=permission)
        self.permission_name = permission_name

        # Update the permission
        updated_permission = CreatePermission(
            name=permission_name,
            description="Updated description"
        )

        response = self.scalekit_client.permissions.update_permission(
            permission_name=permission_name,
            permission=updated_permission
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)

        # Verify the update
        get_response = self.scalekit_client.permissions.get_permission(permission_name=permission_name)
        self.assertEqual(get_response[0].permission.description, "Updated description")

    def test_delete_permission(self):
        """ Method to test delete permission """
        # First create a permission
        permission_name = f"test_permission_{self.faker.unique.random_number()}"
        
        permission = CreatePermission(
            name=permission_name,
            description="Permission to be deleted"
        )
        
        create_response = self.scalekit_client.permissions.create_permission(permission=permission)

        # Delete the permission
        response = self.scalekit_client.permissions.delete_permission(permission_name=permission_name)
        self.assertEqual(response[1].code().name, "OK")

        # Verify permission is deleted
        with self.assertRaises(ScalekitNotFoundException):
            self.scalekit_client.permissions.get_permission(permission_name=permission_name)

    def test_list_role_permissions(self):
        """ Method to test list permissions for a role """
        # First create a role
        role_display_name = f"Test Role {self.faker.random_number(digits=8)}"
        self.role_name = role_display_name.lower().replace(' ', '_')
        
        role = CreateRole(
            name=self.role_name,
            display_name=role_display_name,
            description="Test role for permission testing")
        self.scalekit_client.roles.create_role(role=role)

        # List permissions for the role
        response = self.scalekit_client.permissions.list_role_permissions(role_name=self.role_name)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(hasattr(response[0], 'permissions'))

    def test_add_permissions_to_role(self):
        """ Method to test adding permissions to a role """
        # Create a permission
        self.permission_name = f"test_permission_{self.faker.unique.random_number()}"
        permission = CreatePermission(
            name=self.permission_name,
            description="Permission for role testing"
        )
        self.scalekit_client.permissions.create_permission(permission=permission)

        # Create a role
        role_display_name = f"Test Role {self.faker.random_number(digits=8)}"
        role_name = role_display_name.lower().replace(' ', '_')
        role = CreateRole(
            name=role_name,
            display_name=role_display_name,
            description="Role for permission testing"
        )
        role_response = self.scalekit_client.roles.create_role(role=role)
        self.role_name = role_name

        # Add permission to role
        response = self.scalekit_client.permissions.add_permissions_to_role(
            role_name=role_name,
            permission_names=[self.permission_name]
        )
        self.assertEqual(response[1].code().name, "OK")

        # Verify permission was added
        list_response = self.scalekit_client.permissions.list_role_permissions(role_name=role_name)
        permission_names = [perm.name for perm in list_response[0].permissions]
        self.assertIn(self.permission_name, permission_names)

    def test_remove_permission_from_role(self):
        """ Method to test removing a permission from a role """
        # Create a permission
        self.permission_name = f"test_permission_{self.faker.unique.random_number()}"
        permission = CreatePermission(
            name=self.permission_name,
            description="Permission for role testing"
        )
        self.scalekit_client.permissions.create_permission(permission=permission)

        # Create a role
        role_display_name = f"Test Role {self.faker.random_number(digits=8)}"
        role_name = role_display_name.lower().replace(' ', '_')
        role = CreateRole(
            name=role_name,
            display_name=role_display_name,
            description="Role for permission testing"
        )
        role_response = self.scalekit_client.roles.create_role(role=role)
        self.role_name = role_name

        # Add permission to role first
        add_response = self.scalekit_client.permissions.add_permissions_to_role(
            role_name=role_name,
            permission_names=[self.permission_name]
        )

        # Remove permission from role
        response = self.scalekit_client.permissions.remove_permission_from_role(
            role_name=role_name,
            permission_name=self.permission_name
        )
        self.assertEqual(response[1].code().name, "OK")

        # Verify permission was removed
        list_response = self.scalekit_client.permissions.list_role_permissions(role_name=role_name)
        permission_names = [perm.name for perm in list_response[0].permissions]
        self.assertNotIn(self.permission_name, permission_names)

    def test_list_effective_role_permissions(self):
        """ Method to test listing effective permissions for a role """
        # Create a role
        role_display_name = f"Test Role {self.faker.random_number(digits=8)}"
        self.role_name = role_display_name.lower().replace(' ', '_')
        role = CreateRole(
            name=self.role_name,
            display_name=role_display_name,
            description="Role for effective permissions testing"
        )
        role_response = self.scalekit_client.roles.create_role(role=role)

        # List effective permissions for the role
        response = self.scalekit_client.permissions.list_effective_role_permissions(role_name=self.role_name)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(hasattr(response[0], 'permissions'))

    def test_add_multiple_permissions_to_role(self):
        """ Method to test adding multiple permissions to a role """
        # Create multiple permissions
        permission_names = []
        for i in range(2):
            permission_name = f"test_permission_{self.faker.unique.random_number()}"
            permission = CreatePermission(
                name=permission_name,
                description=f"Permission {i} for role testing"
            )
            self.scalekit_client.permissions.create_permission(permission=permission)
            permission_names.append(permission_name)

        # Store first permission for cleanup
        self.permission_name = permission_names[0]

        # Create a role
        role_display_name = f"Test Role {self.faker.random_number(digits=8)}"
        self.role_name = role_display_name.lower().replace(' ', '_')
        role = CreateRole(
            name=self.role_name,
            display_name=role_display_name,
            description="Role for multiple permissions testing"
        )
        self.scalekit_client.roles.create_role(role=role)

        # Add multiple permissions to role
        response = self.scalekit_client.permissions.add_permissions_to_role(
            role_name=self.role_name,
            permission_names=permission_names
        )
        self.assertEqual(response[1].code().name, "OK")

        # Verify permissions were added
        list_response = self.scalekit_client.permissions.list_role_permissions(role_name=self.role_name)
        role_permission_names = [perm.name for perm in list_response[0].permissions]
        for perm_name in permission_names:
            self.assertIn(perm_name, role_permission_names)

        # Clean up additional permissions
        for perm_name in permission_names[1:]:
            try:
                self.scalekit_client.permissions.delete_permission(permission_name=perm_name)
            except ScalekitNotFoundException:
                pass

    def test_create_permission_duplicate_name(self):
        """ Method to test creating permission with duplicate name """
        self.permission_name = f"test_permission_{self.faker.unique.random_number()}"
        
        permission1 = CreatePermission(
            name=self.permission_name,
            description="First permission"
        )
        
        permission2 = CreatePermission(
            name=self.permission_name,
            description="Second permission with same name"
        )

        # Create first permission
        self.scalekit_client.permissions.create_permission(permission=permission1)

        # Try to create second permission with same name - should fail
        with self.assertRaises(ScalekitBadRequestException):
            self.scalekit_client.permissions.create_permission(permission=permission2)

    def tearDown(self):
        """ Method to clean up """
        errors = []
        if self.permission_name:
            try:
                self.scalekit_client.permissions.delete_permission(permission_name=self.permission_name)
            except Exception as exp:
                errors.append(exp)

        if self.role_name:
            try:
                self.scalekit_client.roles.delete_role(role_name=self.role_name)
            except Exception as exp:
                errors.append(exp)

        if self.org_id:
            try:
                self.scalekit_client.organization.delete_organization(organization_id=self.org_id)
            except Exception as exp:
                errors.append(exp)

        if errors:
            raise Exception(f"Errors during cleanup: {errors}")
