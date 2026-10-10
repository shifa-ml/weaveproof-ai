# LOOMTRACE AI

LOOMTRACE AI is a React and Vite demonstration of a digital weave passport for
Assam handloom textiles. It connects QR scanning to local sample product
records, craft stories, and clearly labelled demonstration provenance data.

> **Demonstration only:** A registered QR code proves only that the identifier
> exists in this local demo registry. It does not authenticate a physical
> textile, verify an artisan identity, prove a GI claim, or represent a
> blockchain transaction.

## Features

- Heritage-inspired LOOMTRACE AI catalogue and product passports.
- Three local demonstration product records for Muga, cotton/Gamosa-inspired,
  and Eri textiles.
- QR code generation, camera scanning, QR-image upload, and manual ID lookup.
- Safe rejection for unknown IDs and unrelated QR content.
- English, Assamese, and Hindi interface support, with saved stories used when
  optional AI story generation is unavailable.
- Vercel serverless endpoint for optional culturally respectful story drafts.

## Technology

- React 19
- Vite 7
- `html5-qrcode` for camera and image QR scanning
- `qrcode` for demonstration QR generation
- `lucide-react` for interface icons
- Vercel serverless function at `api/generate-story.js`

## Run locally

```powershell
npm.cmd install
npm.cmd run dev
```

Open the URL printed by Vite, usually `http://localhost:5173`.

Create a production build:

```powershell
npm.cmd run build
npm.cmd run preview
```

## QR testing

1. Select **Sample QR** and open or download the generated code.
2. Select **Scan a Weave**.
3. Start the camera, upload the QR image, or enter `WEAVE-001` manually.
4. Use the test bench to confirm that `LT-XX-9999-FAKE` and unrelated URLs are
   rejected rather than marked authentic.

Camera access is requested only after selecting **Start camera**. Browsers
normally require `localhost` or HTTPS for camera access.

## Optional AI story generation

The passport has an optional story-generation action. It falls back to the
saved local translation if the serverless API is unavailable or unconfigured.

For Vercel, configure these environment variables in the project settings:

```text
GEMMA_API_KEY=your_server-side_key
GEMMA_MODEL=gemma-4-26b-a4b-it
```

Do not expose API keys through `VITE_` variables or commit them to the
repository.

## Deploying to Vercel

The application uses Vite's default build command:

```text
Build Command: npm run build
Output Directory: dist
```

When Git integration is connected to the repository, push to the configured
production branch (normally `main`):

```powershell
git push origin main
```

If the deployment does not update, confirm in Vercel that the project is linked
to the correct GitHub repository and that its Production Branch is `main`.

## Project layout

```text
api/generate-story.js   Optional Vercel AI-story endpoint
src/App.jsx             Application entry wrapper
src/App (2).jsx         LOOMTRACE interface and QR interactions
src/data.js             Demonstration products and translations
src/styles.css          Responsive LOOMTRACE styling
src/download.png        Brand artwork
```

## Git workflow

```powershell
git add README.md
git commit -m "Add project documentation"
git push origin main
```
