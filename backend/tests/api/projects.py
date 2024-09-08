import httpx

from .base import ApiBase


class ApiProjects(ApiBase):

    def create_project(
        self,
        project_name: str,
        user_init_data: str,
    ) -> httpx.Response:
        """
        Creates a new project on the `/projects` endpoint.

        Args:
            project_name (str): The name of the new project.
            user_init_data (str): User-specific initialization data required by the API.

        Returns:
            httpx.Response: The response object.
        """

        url = self.PROJECTS
        json = {"name": project_name}
        headers = {"user-init-data": user_init_data}

        return self.post(url=url, json=json, headers=headers)

    def get_projects_by_user(
        self,
        user_id: str,
        user_init_data: str,
    ) -> httpx.Response:
        """
        Retrieves all projects associated with a specific user from the API.

        Args:
            user_id (str): The unique identifier of the user whose projects to retrieve.
            user_init_data (str): User-specific initialization data required by the API.

        Returns:
            httpx.Response: The response object from the API \
                containing a list of user projects.
        """

        url = self.PROJECT_BY_USER.format(user_id=user_id)
        headers = {"user-init-data": user_init_data}

        return self.get(url=url, headers=headers)

    def get_project_by_id(
        self,
        project_id: str,
        user_init_data: str,
    ) -> httpx.Response:
        """
        Retrieves a specific project from the API.

        Args:
            project_id (str): The unique identifier of the project to retrieve.
            user_init_data (str): User-specific initialization data required by the API.

        Returns:
            httpx.Response: The response object from the API containing project \
                information.
        """

        url = self.PROJECT.format(project_id=project_id)
        headers = {"user-init-data": user_init_data}

        return self.get(url=url, headers=headers)

    def delete_project(
        self,
        project_id: str,
        user_init_data: str,
    ) -> httpx.Response:
        """
        Deletes a specific project from the API.

        Args:
            project_id (str): The unique identifier of the project to delete.
            user_init_data (str): User-specific initialization data required by the API.

        Returns:
            httpx.Response: The response object.

        Raises:
            httpx.HTTPError: If the API request fails.
        """

        url = self.PROJECT.format(project_id=project_id)
        headers = {"user-init-data": user_init_data}

        return self.delete(url=url, headers=headers)

    def update_project(
        self,
        project_id: str,
        name: str,
        user_init_data: str,
    ) -> httpx.Response:
        """
        Updates the details of an existing project on the API.

        Args:
            project_id (str): The unique identifier of the project to update.
            name (str): The new name for the project.
            user_init_data (str): User-specific initialization data required by the API.

        Returns:
            httpx.Response: The response object.
        """

        url = self.PROJECT.format(project_id=project_id)
        json = {"name": name}
        headers = {"user-init-data": user_init_data}

        return self.patch(url=url, json=json, headers=headers)
