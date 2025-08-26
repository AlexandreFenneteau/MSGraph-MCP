from azure.identity import DeviceCodeCredential, InteractiveBrowserCredential
from msgraph import GraphServiceClient
import sys
from pathlib import Path

# Add the src directory to Python path to enable absolute imports
src_path = Path(__file__).parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from msgraph_mcp.config import APP_AUTH_SETTINGS

__CREDENTIALS = InteractiveBrowserCredential(
    client_id=APP_AUTH_SETTINGS.client_id,
    tenant_id=APP_AUTH_SETTINGS.tenant_id,
    redirect_uri=APP_AUTH_SETTINGS.redirect_uri
)

GRAPH_CLIENT = GraphServiceClient(
    credentials=__CREDENTIALS,
    scopes=APP_AUTH_SETTINGS.scopes
)

if __name__ == "__main__":
    import asyncio
    async def get_me():
        me = await GRAPH_CLIENT.me.get()
        if me:
            print(me.display_name)

    asyncio.run(get_me())
