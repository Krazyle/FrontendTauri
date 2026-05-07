# Project Mapping

- Reference @package.json for Svelte + Tauri frontend and desktop env.
- Reference @src-fastapi/pyproject.toml for Python backend deps + tooling config.

# GitMCP-Docs

- Use `match_common_libs_owner_repo_mapping` to resolve unknown library owner and repo paths.
- Use owner + project name with `fetch_generic_documentation` for full repo docs.
- Use `search_generic_documentation` for specific repo-doc info via semantic queries.
- Use `search_generic_code` to find relevant files and code segments for implementation requests.
- Use `fetch_generic_url_content` for external absolute URLs from docs; respect robots.txt.

# Development Rules

- Follow instructions strictly.
- Keep changes minimal and within scope.
- Do not add or modify anything unrelated to the task.
- Ask before making out-of-scope changes.