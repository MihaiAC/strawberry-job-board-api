from graphql import GraphQLError


class ResourceNotFound(GraphQLError):
    def __init__(self, resource_name: str):
        message = f"{resource_name} not found."
        super().__init__(message=message)

    @staticmethod
    def get_message(resource_name: str) -> str:
        message = f"{resource_name} not found."
        return message
