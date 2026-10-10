# Integration recovery notes

The original tracked prototype remains available at Git commit `3b16015`.
Git checkpoint creation was blocked because the workspace permits reading, but
not writing, `.git/index.lock`.

Before the block, only these incoming-file edits were made:

- `src/App (2).jsx`: its optional story request now uses the existing
  Vercel route `/api/generate-story` and never defaults to a localhost URL.
- `src/data.js`: structured, explicitly demonstration-only passport fields
  were added to each local sample record.
- `backend/.env.example`: a credential-like value was cleared deliberately;
  it must not be restored.

All other incoming variants remain in place for comparison.
