## Installation

## Lancer un inspecteur (server) mcp

```shell
uv run mcp dev .\src\msgraph_mcp\main.py
```

A partir de cette interface il faut configurer `Transport Type` et les autres champs. Cela ne lance qu'un inspecteur, pas le mcp server.

### stdio
La commande sera appelée lors de la connexion par le client MCP.
Configurer:
- `command`: `uv`
- `arguments`: `--directory C:\\Users\\AlexandreFenneteau\\Travail\\perso\\msgrah_mcp run src\\msgraph_mcp\\main.py`
Cette commande permet de lancer le server avec `uv` (python) à partir du bon dossier `C:\\Users\\AlexandreFenneteau\\Travail\\perso\\msgrah_mcp` en executant le bon fichier `src\\msgraph_mcp\\main.py`


### SSE & Streamable Http
1. Vous devez configurer dans le `src\\msgraph_mcp\\main.py`
    - `host`
    - `port`
    - si http:
        - `streamable_http_path`
        - `mcp.run(transport="streamable-http")` (dans le `if __name__: ...`)
    - si sse
        - `sse_path`
        - `mcp.run(transport="sse")` (dans le `if __name__: ...`)
2. Vous pouvez alors renseigner avec ces infos dans l'inspecteur pour se connecter:
    - `Transport Type`
    - `URL`: `http:\\host:port\path` où `path` est ce que vous avez fourni comme `streamable_http_path` ou `sse_path`

## Utilisation de l'inspecteur

Une fois configuré, lancer la connexion au serveur en cliquant sur `Connect`.
- Vous pouvez voir ce qui est à disposition de votre LLM en navigant sur les onglets `Resources`, `Prompts`, `Tools`, ...