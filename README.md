# MCP Plugin Template

A GitHub template for packaging any MCP server as an installable plugin for GitHub Copilot in VS Code.

## For plugin authors

### 1. Use this template

Click **"Use this template"** on GitHub to create your own repo.

### 2. Add your MCP server

Edit `server/index.js` — add tools and resources to the objects at the top of the file. The included server implements the MCP protocol directly with no dependencies.

If you need npm packages, add them to `package.json` and see [Adding dependencies](#adding-dependencies) below.

### 3. Fill in the placeholders

Search for `YOUR_` across the repo and replace:

| Placeholder        | Where                                       | What                              |
|--------------------|---------------------------------------------|-----------------------------------|
| `YOUR_PLUGIN_NAME` | `plugin.json`, `.mcp.json`, `package.json`, `server/index.js` | Your plugin's name (kebab-case)   |
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
├── .mcp.json             # MCP server declaration
├── server/
│   └── index.js          # Your MCP server (edit this)
├── package.json          # Plugin metadata
└── README.md
```

- `.mcp.json` tells Claude Code to start your server via `node server/index.js`
- The server implements the MCP protocol (JSON-RPC over stdio) with no external dependencies
- `${CLAUDE_PLUGIN_ROOT}` points to the plugin's install directory

## Adding dependencies

If your server needs npm packages:

1. Add them to `package.json`
2. Create `hooks/hooks.json` with a `SessionStart` hook to auto-install them:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && cp \"${CLAUDE_PLUGIN_ROOT}/package.json\" . && npm install --production) || rm -f \"${CLAUDE_PLUGIN_DATA}/package.json\""
          }
        ]
      }
    ]
  }
}
```

3. Add `NODE_PATH` to `.mcp.json` so your server can find the installed modules:

```json
{
  "mcpServers": {
    "your-plugin": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server/index.js"],
      "env": {
        "NODE_PATH": "${CLAUDE_PLUGIN_DATA}/node_modules"
      }
    }
  }
}
```
