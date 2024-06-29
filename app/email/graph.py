from configparser import ConfigParser
from azure.identity import DeviceCodeCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.item.mail_folders.item.messages.messages_request_builder import (
    MessagesRequestBuilder)

class Graph:
    def __init__(self, config_path='config.cfg'):
        config = ConfigParser()
        config.read(config_path)
        azure_settings = config['azure']

        self.client_id = azure_settings['clientId']
        self.tenant_id = azure_settings['tenantId']
        self.graph_scopes = azure_settings['graphUserScopes'].split(' ')

        self.device_code_credential = DeviceCodeCredential(self.client_id, tenant_id=self.tenant_id)
        self.client = GraphServiceClient(self.device_code_credential, scopes=self.graph_scopes)

    async def get_user_token(self):
        access_token = self.device_code_credential.get_token(*self.graph_scopes)
        return access_token.token

    async def get_inbox(self):
        query_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
            select=['from', 'body', 'sentDateTime'],
            top=25,
            orderby=['sentDateTime DESC']
        )
        request_config = MessagesRequestBuilder.MessagesRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )

        messages = await self.client.me.mail_folders.by_mail_folder_id('inbox').messages.get(
            request_configuration=request_config)
        return messages