# Repository Guidelines

This repo ships the Krita script extension “Layer Finder.” Keep it lean and consistent by following these notes.

## Project Structure & Module Organization
- `layerfinder/`: Main Python package; all logic lives in `layerfinder.py`.
- `actions/`: Krita action/shortcut definition (`layerfinder.action`).
- `layerfinder.desktop`: Desktop file that registers the extension with Krita.
- No bundled tests or extra assets yet—add new folders as needed and update `README.md` when you do.

## Build, Test, and Development Commands
- No build step required. For local dev, copy files into your Krita resources folder.
- `cp -r actions layerfinder layerfinder.desktop ~/.local/share/krita/pykrita/` (Linux example). Adjust the path for your OS.
- After copying, run in Krita via `Tools > Scripts > Find layers colorizing the selection` or press `Ctrl+F`.

## Coding Style & Naming Conventions
- Python 3 with PyQt5 and Krita API; use 4-space indent and `snake_case` for functions/variables.
- The layer walk is recursive—avoid adding stateful globals. Reuse the shared label constants `NO_LABEL` and `GREEN_LABEL`.
- Preserve existing TODOs (non-rect selections, non-8-bit depths) and append related work nearby.

## Testing Guidelines
- No automated tests yet. Manual check:
  1. Create a rectangular selection in a test doc.
  2. Mix visible/hidden layers with paint, then run the action.
  3. Only layers affecting the selection should get the green label.
  4. Verify no errors when there’s no document or no selection.
- If adding automated tests, prefer `pytest` under a new `tests/` directory.

## Commit & Pull Request Guidelines
- Commit messages must use Conventional Commit style (e.g., `feat: add non-rect selection support`, `fix: prevent crash without selection`). Append related issue numbers like `(#123)` when relevant.
- PR titles must also use Conventional Commit style. PR bodies should include a brief summary, verification steps, and the Krita version used. Add screenshots or a short GIF for UI/behavior changes when clarity helps.

## Security & Configuration Tips
- Don’t hardcode resource paths; they’re OS-dependent. Point contributors to the README or inline comments for guidance.
- Keep the current early-return behavior when no active document or selection exists—avoid crashing Krita.
