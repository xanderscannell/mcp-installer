# MCP Plugin Template (Python)

A GitHub template for packaging any Python MCP server as an installable plugin for GitHub Copilot in VS Code.

## For plugin authors

### 1. Use this template

Click **"Use this template"** on GitHub to create your own repo.

### 2. Add your MCP server

Edit `server/server.py` — add tools and resources to the dicts at the top of the file. The included server implements the MCP protocol directly using only the Python standard library.

If you need pip packages, just add them to `requirements.txt` — the dependency workflow is already configured. A `SessionStart` hook in `hooks/hooks.json` auto-installs packages, and `.mcp.json` sets `PYTHONPATH` so your server can find them.

### 3. Fill in the placeholders

Search for `YOUR_` across the repo and replace:

| Placeholder        | Where                                       | What                              |
|--------------------|---------------------------------------------|-----------------------------------|
| `YOUR_PLUGIN_NAME` | `plugin.json`, `.mcp.json`, `package.json`, `server/server.py` | Your plugin's name (kebab-case)   |
| `YOUR_DESCRIPTION` | `plugin.json`                               | What your plugin does             |
| `YOUR_NAME`        | `plugin.json`                               | Your name                         |
| `YOUR_EMAIL`       | `plugin.json`                               | Your email                        |
| `YOUR_USERNAME`    | `plugin.json`                               | Your GitHub username              |
| `YOUR_REPO`        | `plugin.json`                               | Your GitHub repo name             |

### 4. Distribute

Share your repo — users install the plugin directly from the GitHub URL.

> **Important:** The plugin is read from the repository's default branch. Make sure your changes are merged to `main`/`master` before distributing.

## Try it yourself

Want to test your plugin before sharing it? Here's how:

1. **Fill in the placeholders** — follow [step 3 above](#3-fill-in-the-placeholders) to replace all `YOUR_` values with your own info.

2. **Push to GitHub** — commit your changes and push the repo to GitHub. Make sure it's on your default branch (`main` or `master`).

3. **Install your own plugin** — open the VS Code command palette (`F1` or `Ctrl+Shift+P`), select **"Chat: Install Plugin from Source"**, and paste your repo URL:
   ```
   https://github.com/YOUR_USERNAME/YOUR_REPO
   ```
   Hit enter and the plugin is installed.

4. **Test it** — ask GitHub Copilot:
   > Test the connection with my-plugin-name

   Copilot should call the `hello` tool and return:
   > "Hello from your MCP plugin!"

   Replace `my-plugin-name` with whatever you set `YOUR_PLUGIN_NAME` to.

If that works, your plugin is wired up correctly and ready to distribute.

## For users installing a plugin built from this template

1. Open the VS Code command palette (`F1` or `Ctrl+Shift+P`)
2. Select **"Chat: Install Plugin from Source"**
3. Paste the plugin's GitHub repo URL (e.g. `https://github.com/AUTHOR/REPO`) and hit enter

That's it — GitHub Copilot can now access the plugin's tools.

## How it works

```
your-plugin/
├── .claude-plugin/
│   └── plugin.json       # Plugin metadata
├── .mcp.json             # MCP server declaration (with PYTHONPATH)
├── hooks/
│   └── hooks.json        # Auto-installs pip deps on session start
├── server/
│   └── server.py         # Your MCP server (edit this)
├── requirements.txt      # Python dependencies
├── package.json          # Plugin metadata
└── README.md
```

- `.mcp.json` tells Claude Code to start your server via `python3 server/server.py`
- The server implements the MCP protocol (JSON-RPC over stdio) using only the standard library
- `${CLAUDE_PLUGIN_ROOT}` points to the plugin's install directory

## How dependencies work

This template comes with pip dependency support pre-configured. Just add packages to `requirements.txt` and they'll be available in your server.

- **`hooks/hooks.json`** — A `SessionStart` hook compares `requirements.txt` against a cached copy. If it's changed (or missing), it runs `pip install -r requirements.txt -t <data>/python_modules` to install packages.
- **`.mcp.json`** — Sets `PYTHONPATH` to the data directory's `python_modules`, so `import` statements in your server resolve correctly.

No manual setup needed — just add packages to `requirements.txt` and your server can `import` them.
