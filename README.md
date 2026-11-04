# Speaking Coach

Speaking Coach is a mobile app for practicing spoken English and reviewing pronunciation, fluency, grammar, and vocabulary feedback. The product requirements and planned phases are in [SPEC.md](./SPEC.md).

## Current status

This repository is an early Phase 1 scaffold:

- The Expo app has a starter screen and can run on iOS, Android, or web.
- The FastAPI app exposes health, recording, analysis, and vocabulary routes.
- The API currently returns sample data. Authentication, persistence, signed uploads, background analysis, and real speech/LLM providers are not implemented yet.
- The mobile app is not connected to the API, and its recording controls are UI-only.

## Requirements

- Node.js and npm
- Python 3.12 (the version specified by the project)
- Docker and Docker Compose, if running the local infrastructure

## Run the API locally

From the repository root:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r apps/api/requirements.txt
cd apps/api
uvicorn app.main:app --reload
```

The API is available at <http://127.0.0.1:8000>. Interactive API documentation is at <http://127.0.0.1:8000/docs>.

Useful routes:

- `GET /health`
- `POST /recordings`
- `POST /recordings/{recording_id}/process`
- `GET /analyses/{recording_id}`
- `POST /vocab`

Recording and vocabulary routes currently return sample responses rather than saving data.

## Run the mobile app

From the repository root:

```sh
npm install
npm run dev:mobile
```

Use the Expo terminal prompt to open the app on a simulator or physical device. To run the browser preview:

```sh
npm run web --workspace apps/mobile
```

The mobile app currently runs independently from the API.

## Local infrastructure

The Compose file defines PostgreSQL, Redis, MinIO, the API, and the worker. Create a local environment file and start the services with:

```sh
cp .env.example .env
docker compose up --build
```

Local service endpoints:

- API: <http://localhost:8000>
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`
- MinIO API: <http://localhost:9000>
- MinIO console: <http://localhost:9001>

The API and worker are still scaffolds; the current sample API routes do not yet persist data or run the analysis pipeline.

## Tests and checks

From the repository root:

```sh
npm run test:api
npm run test:mobile
npm run typecheck:mobile
```

For the API, activate the Python virtual environment first. The backend tests cover initial scoring, word parsing/statistics, and placeholder review scheduling logic. The mobile test covers a sample analysis-summary utility.

## Project layout

```text
apps/
  api/       FastAPI backend and worker scaffold
  mobile/    Expo Router mobile app
docker-compose.yml
SPEC.md
```
