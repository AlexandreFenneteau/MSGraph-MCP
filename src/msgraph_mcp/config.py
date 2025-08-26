from pydantic_settings import BaseSettings, SettingsConfigDict

class AppAuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, env_prefix="MS_GRAPH_MCP_", extra="ignore")

    client_id: str # get the MS_GRAPH_MCP_CLIENT_ID env variable set in .env
    tenant_id: str
    redirect_uri: str
    scopes: list[str]


class DateTimeSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, env_prefix="MS_GRAPH_MCP_", extra="ignore")

    timezone: str
    datetime_format: str
    date_format: str


APP_AUTH_SETTINGS = AppAuthSettings()
DATE_TIME_SETTINGS = DateTimeSettings()


if __name__ == "__main__":
    import os
    print(os.path.abspath("."))
    print(APP_AUTH_SETTINGS)
    print(DATE_TIME_SETTINGS)