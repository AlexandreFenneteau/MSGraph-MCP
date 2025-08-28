# MSGraph MCP Server

An MCP (Model Context Protocol) server that allows language models to interact with Microsoft Graph to access emails and calendar events.

## Project Overview

This project implements an MCP server that exposes Microsoft Graph functionalities as tools usable by language models (LLMs). It enables:

- **Search and retrieve emails** based on search criteria
- **Query calendar events** for specific date ranges
- **Extract email addresses** from search results
- **Access current temporal information**

## Architecture

The project is structured around three main components:

1. **MCP Server**: Based on the [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk), exposes Microsoft Graph tools
2. **Microsoft Graph Client**: Uses the Microsoft Graph SDK for Python with Azure AD authentication
3. **Azure Infrastructure**: Terraform configuration for Azure AD application deployment

## Prerequisites

- Python 3.12+
- [UV](https://docs.astral.sh/uv/) for dependency management
- An Azure Active Directory tenant
- Terraform (optional, for automated deployment)

## Installation

### 1. Clone the repository

```bash
git clone <repo-url>
cd msgrah_mcp
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Azure AD Configuration

#### Option A: Automated deployment with Terraform

1. Copy the variables example file:
   ```bash
   cp terraform/dev.tfvars.exemple terraform/dev.tfvars
   ```

2. Edit `terraform/dev.tfvars` with your Azure values

3. Deploy the infrastructure:
   ```bash
   cd terraform
   terraform init
   terraform plan -var-file="dev.tfvars" -out="dev.tfplan"
   terraform apply "dev.tfplan"
   ```

#### Option B: Manual configuration

Manually create an Azure AD application with the following permissions:
- `Mail.Read`
- `Calendar.Read`
- `User.Read`

### 4. Environment variables configuration

Create a `.env` file at the project root:

```env
MS_GRAPH_MCP_CLIENT_ID=your-client-id
MS_GRAPH_MCP_TENANT_ID=your-tenant-id
MS_GRAPH_MCP_REDIRECT_URI=http://localhost:8080
MS_GRAPH_MCP_SCOPES=["https://graph.microsoft.com/Mail.Read", "https://graph.microsoft.com/Calendar.Read"]
MS_GRAPH_MCP_TIMEZONE=Europe/Paris
MS_GRAPH_MCP_DATETIME_FORMAT=%Y-%m-%d %H:%M:%S
MS_GRAPH_MCP_DATE_FORMAT=%Y-%m-%d
```

## Usage

### Development and testing with MCP inspector

To test the server in development mode:

```bash
uv run mcp dev .\src\msgraph_mcp\main.py
```

This command launches the MCP inspector which allows testing available tools.

### Transport configuration

The MCP server supports multiple transport modes:

#### 1. STDIO (recommended for integration with MCP clients)

Configuration in the inspector:
- **Command**: `uv`
- **Arguments**: `--directory C:\path\to\msgrah_mcp run src\msgraph_mcp\main.py`

For MCP client configuration files, use one of the following formats:

**YAML Configuration:**
```yaml
msgraph-mcp:
  command: "uv"
  args: [
    "--directory",
    "C:\\path\\to\\msgrah_mcp",
    "run",
    "src\\msgraph_mcp\\main.py"
  ]
```

**JSON Configuration:**
```json
{
  "msgraph-mcp": {
    "command": "uv",
    "args": [
      "--directory",
      "C:\\path\\to\\msgrah_mcp",
      "run",
      "src\\msgraph_mcp\\main.py"
    ]
  }
}
```

Replace `C:\\path\\to\\msgrah_mcp` with the actual path to your project directory.

#### 2. HTTP Streamable

1. Modify `src\msgraph_mcp\main.py`:
   ```python
   mcp = FastMCP(
       name=USER_AGENT,
       host="localhost",
       port=8182,
       streamable_http_path="/mcp",
   )
   
   # In the main function
   mcp.run(transport="streamable-http")
   ```

2. Configure the inspector:
   - **Transport Type**: HTTP Streamable
   - **URL**: `http://localhost:8182/mcp`

#### 3. Server-Sent Events (SSE)

1. Modify `src\msgraph_mcp\main.py`:
   ```python
   mcp = FastMCP(
       name=USER_AGENT,
       host="localhost",
       port=8182,
       sse_path="/sse",
   )
   
   # In the main function
   mcp.run(transport="sse")
   ```

2. Configure the inspector:
   - **Transport Type**: SSE
   - **URL**: `http://localhost:8182/sse`

## Available Tools

The server exposes the following tools to language models:

### `get_current_datetime()`
Returns the current date and time in the configured timezone.

### `get_calendar_events_by_date_range(start_year, start_month, start_day, end_year, end_month, end_day)`
Retrieves calendar events for a specific date range.

### `get_upcoming_week_calendar_events()`
Retrieves all events for the upcoming week (Monday to Sunday).

### `search_email_messages(search_term, n_emails=5)`
Searches for emails matching a term and returns message details.

### `extract_email_addresses_from_search(search_term, n_searched_messages=3)`
Extracts email addresses from messages matching a search term.

## Project Structure

```
msgrah_mcp/
├── src/msgraph_mcp/          # Main MCP server code
│   ├── mg/                   # Microsoft Graph modules
│   │   ├── calendar.py       # Calendar management
│   │   ├── client.py         # Microsoft Graph client
│   │   └── mail.py           # Email management
│   ├── main.py               # MCP server entry point
│   ├── config.py             # Application configuration
│   ├── models.py             # Data models
│   └── utils.py              # Utilities
├── terraform/                # Infrastructure as Code
├── notebooks/                # Jupyter notebooks for testing
└── lib/                      # Auxiliary modules
```

## Testing and Validation

After configuration, use the MCP inspector to:

1. **Connect to the server**: Click "Connect" in the interface
2. **Explore tools**: Navigate through "Tools", "Resources", "Prompts" tabs
3. **Test functionalities**: Execute tools with different parameters

## Security

- Azure secrets are stored in environment variables
- Authentication uses Azure AD "on behalf of" flow
- Permissions are limited to read-only operations

## Contributing

This project serves as an example of MCP and Microsoft Graph integration. Contributions to extend functionalities are welcome.