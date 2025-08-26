from azure.identity import DeviceCodeCredential, DefaultAzureCredential, InteractiveBrowserCredential
from msgraph import GraphServiceClient
import json
import os

if __name__ == "__main__":
    import asyncio

    # MSAL
    # credentials = DeviceCodeCredential (
    #     client_id="6b01dd77-1984-4bf8-bec6-e5a85829fe2c",
    #     tenant_id="9ffc6712-5ed6-4651-9b81-51f454114654"
    # )
    credentials = InteractiveBrowserCredential(
        client_id="6b01dd77-1984-4bf8-bec6-e5a85829fe2c",
        tenant_id="9ffc6712-5ed6-4651-9b81-51f454114654",
        redirect_uri="http://localhost:8080"
    )

    # scopes = ['Calendars.Read', 'User.Read']
    scopes = ["Calendars.Read"]
    client = GraphServiceClient(credentials=credentials, scopes=scopes)

    # async def get_token():
    #     return await credentials.get_token("User.Read", "Mail.Read", )

    async def get_me():
        me = await client.me.get()
        if me:
            print(me.display_name)

    async def get_calendar():
        calendar = await client.me.calendar.get()
        if calendar:
            print(calendar.events)
        client.me.calendar_view.get(
            client.me.calendar_view.CalendarViewRequestBuilderGetRequestConfiguration(
                query_parameters=client.me.calendar_view.CalendarViewRequestBuilderGetQueryParameters(
                    start_date_time="2025-08-19T08:24:24.309Z",
                    end_date_time="2025-08-26T08:24:24.309Z"
                )
            )
        )
        

    async def get_things():
        await get_me()
        await get_calendar()
    
    asyncio.run(get_things())