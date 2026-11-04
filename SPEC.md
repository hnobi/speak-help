# Speaking Coach — Build Spec

You are building a mobile app that helps a non-native English speaker improve spoken English: pronunciation, fluency, grammar (will/would, in/on/at, articles, tenses) and active vocabulary. The user records or uploads themselves speaking and gets detailed, continuous feedback. Treat this file as the source of truth. If something here is unclear or conflicts with what you find while building, stop and ask rather than guess.

## How to work

- Read this whole file first. Then propose a plan for Phase 1 only: repo layout, key files, and the order you'll build in. Wait for my go-ahead before writing code.
- Build one phase at a time. At the end of each phase: run it, run the tests, list what works, what's stubbed, and anything you'd change in the spec.
- Ask before adding any dependency not listed here.
- Keep external AI/speech providers behind interfaces (`TranscriptionProvider`, `PronunciationProvider`, `LLMProvider`, `TTSProvider`) so they can be swapped or mocked.
- Every LLM call returns structured JSON validated with Pydantic. Retry once on validation failure, then surface an error.
- Never commit secrets. Use `.env` files with a checked-in `.env.example`.
- Tests: pytest for backend logic (scoring, FSRS scheduling, word stats, parsers), Jest for key mobile hooks/utils. No need to test third-party APIs directly; mock providers.

## Stack

**Mobile** (`apps/mobile`)
- React Native + Expo (latest SDK), TypeScript, Expo Router
- expo-audio for recording, expo-image-picker / expo-document-picker for video upload
- TanStack Query for server state, Zustand for small local state
- iOS and Android
- Home/lock screen widgets: iOS via WidgetKit (Swift, added through an Expo config plugin/target, e.g. `@bacons/apple-targets`), Android via `react-native-android-widget`. Widgets read from shared storage that the app writes to.
- Push notifications via expo-notifications

**Backend** (`apps/api`)
- Python 3.12, FastAPI, SQLAlchemy 2 + Alembic, Pydantic v2
- PostgreSQL
- Background jobs: Redis + arq (analysis of a recording must never block a request)
- ffmpeg for extracting/normalising audio from video (16 kHz mono WAV)
- spaCy (`en_core_web_sm`, upgrade later if needed) for POS tagging, lemmatisation, word frequency
- py-fsrs for spaced repetition scheduling
- Object storage: S3-compatible interface; MinIO locally, GCS in production

**AI / speech providers**
- Pronunciation: Azure AI Speech Pronunciation Assessment (phoneme/word/sentence accuracy, fluency, completeness, prosody). Prefer en-GB; fall back to en-US for any feature not supported in en-GB, and record which locale was used.
- Transcription: a model that returns word-level timestamps (e.g. OpenAI `whisper-1` with word timestamp granularity). Prompt it to keep disfluencies ("um", "uh", "like") because many transcription models strip them by default; verify this works.
- LLM: OpenAI or Anthropic, behind `LLMProvider`. Used for grammar feedback, rewrites, word enrichment, synonym suggestions, prompts and roleplay.
- TTS: for word audio and "native version" playback, behind `TTSProvider`.
- Realtime voice roleplay (Phase 4): a realtime speech API behind its own interface.

**Infra**
- `docker-compose.yml` for local: Postgres, Redis, MinIO, API, worker
- Deployable to GCP Cloud Run (API + worker), Cloud SQL, Memorystore, GCS. Terraform in `infra/` (Phase 4).

## Repo layout

```
apps/
  mobile/        Expo app
  api/           FastAPI app + arq worker
    app/
      routers/
      models/       SQLAlchemy
      schemas/      Pydantic
      services/     business logic
      providers/    external API adapters + fakes
      jobs/         arq tasks
    tests/
infra/
docker-compose.yml
SPEC.md
```

## Auth

Multi-user ready from day one, though I'll be the first user. Sign in with Apple and Google via Expo AuthSession; backend verifies the ID token and issues its own JWT. Every table that holds user data has `user_id`, and every query is scoped by it.

## Data model (starting point; refine as needed)

- **users**: id, email, display_name, accent_target (en-GB default), daily_goal_minutes, timezone, created_at
- **recordings**: id, user_id, source (audio | video | prompt | shadowing | roleplay), prompt_id?, storage_key, duration_s, status (uploaded | processing | done | failed), error?, created_at
- **analyses**: id, recording_id, transcript, words_json (word, start, end, confidence), pronunciation_json (per word + per phoneme scores), fluency_json (wpm, pauses, filler counts), grammar_issues_json, native_rewrite, overall scores, provider/locale metadata
- **grammar_issues**: id, user_id, analysis_id, category (modal_will_would, preposition, article, tense, agreement, word_order, other), original, corrected, explanation, created_at
- **word_usage**: user_id, lemma, pos, count, last_used_at — aggregated from every analysis
- **vocab_words**: id, user_id, word, lemma, pos (noun, verb, adj, adv, phrasal_verb, idiom, …), ipa, audio_key, definition, examples_json, collocations_json, register (formal | neutral | casual | workplace), user_sentence?, user_sentence_feedback?, status (learning | known | active), tags[], created_at
- **vocab_reviews**: FSRS card state per vocab_word plus review log (rating, reviewed_at)
- **drills**: id, user_id, type (grammar | minimal_pair | vocab_use), source_issue_ids[], content_json, status, created_at
- **prompts**: id, category (daily_life | work_standup | interview | tech_explainer | small_talk | opinion), text, difficulty
- **shadowing_clips**: id, text, audio_key, source/licence, difficulty
- **daily_stats**: user_id, date, minutes_spoken, recordings, avg_pronunciation, filler_rate, wpm, new_words, words_activated

## Features

### 1. Record & analyse (core loop)
- Record audio in-app, or upload a video/audio file. Upload directly to storage via a signed URL; API creates the recording and enqueues analysis.
- Worker pipeline: extract audio (ffmpeg) → transcribe with word timestamps → pronunciation assessment against the transcript → fluency metrics (WPM, pause lengths, filler words from a configurable list) → LLM grammar pass → native-style rewrite → TTS of the rewrite → update word_usage, grammar_issues, daily_stats.
- Mobile shows processing state (poll or push), then a results screen:
  - Transcript with each word coloured by pronunciation score; tap a word to see phoneme breakdown and hear the correct pronunciation
  - Fluency card: WPM, filler count with timestamps, longest pauses
  - Grammar list: original → corrected → one-line explanation, grouped by category
  - "Native version": rewritten text + audio, played next to the user's original
- Video playback synced to the transcript (tap a word to seek).

### 2. Word habits
- Overused words screen: top lemmas by frequency over 7/30 days, excluding stopwords.
- For each overused word, LLM suggests 3–5 alternatives with when to use each and an example. It should also say plainly when the word is fine and doesn't need replacing.
- Filler word trend over time.

### 3. Vocabulary bank
- Add a word manually, from an analysis, or via the OS share sheet (share selected text from any app into the app).
- On add, auto-enrich: lemma, POS tag(s), IPA, TTS audio, plain-English definition, 3–4 example sentences in different contexts, common collocations, register.
- User writes their own sentence; LLM checks it and explains any problem.
- Tags (auto POS + user-defined), search, filter by tag/status.

### 4. Daily practice
- FSRS review queue for vocab. Review modes: meaning → word, word → use it in a spoken sentence (recorded and checked), listen → spell.
- Daily goal and streak.
- Word of the day pushed to widgets and an optional morning notification.

### 5. Active vs passive vocabulary
- After each analysis, mark any vocab_word whose lemma appears in the user's speech as used; after N uses across different recordings, status → active.
- "Words you know but never say" list, and these words are deliberately worked into daily prompts and review ("Use *mitigate* in your answer").

### 6. Mistake bank → drills
- Cluster recurring grammar_issues by category and pattern.
- Generate short drills targeting the user's own mistakes: fill the gap, choose the right option, then say the corrected sentence aloud (graded by pronunciation + transcript match).
- Dedicated focus packs for will/would, in/on/at, articles, present perfect vs past simple.

### 7. Daily speaking prompt
- One 60–120 second prompt per day from the categories above, weighted toward work/interview topics. Same analysis pipeline, results saved to history.

### 8. Shadowing
- Short native clips (start with TTS-generated clips; leave room for licensed recordings).
- Play → record → compare: both waveforms and pitch contours side by side, word-level pronunciation scores, timing differences.

### 9. Minimal pairs
- Detect frequently mispronounced phonemes from pronunciation_json.
- Generate minimal-pair drills for confused sounds (e.g. ship/sheep, west/vest, think/sink): listen-and-pick, then say-and-score.

### 10. AI conversation roleplay
- Realtime voice conversation for scenarios: job interview, standup, client call, small talk, disagreeing politely.
- Full session is recorded; afterwards it goes through the normal analysis pipeline and a summary card lists top 3 things to work on.

### 11. Progress dashboard
- Charts over 7/30/90 days: pronunciation score, filler rate, WPM, active vocab size, grammar issues per minute by category, minutes spoken, streak.
- Weekly summary notification.

### 12. Widgets & notifications
- Home screen widget (small/medium): word of the day with POS and example; tap opens the word.
- iOS lock screen widget: word + IPA.
- Android home screen widget equivalent.
- Notifications: daily practice reminder at a user-set time, word of the day, weekly progress.

### 13. Settings
- Target accent, daily goal, reminder time, filler word list, data export (JSON), delete account + all recordings.

## Phases

**Phase 1 — Foundation + core loop**
Monorepo, docker-compose, auth, recordings upload (audio only), full analysis pipeline, results screen, basic vocab bank with enrichment, CI (lint, typecheck, tests).

**Phase 2 — Learning engine**
Word habits, FSRS daily review, mistake bank + drills, daily prompt, streaks, daily_stats.

**Phase 3 — Video, active vocab, widgets**
Video upload with synced playback, active vs passive vocab, share-sheet capture, iOS + Android widgets, notifications, progress dashboard.

**Phase 4 — Advanced practice + production**
Shadowing, minimal pairs, AI roleplay, weekly summaries, Terraform for GCP, production deploy, cost tracking per provider call.

## Non-functional

- Analysis of a 2-minute recording should finish in under ~60 seconds; show progress stages.
- Log provider latency and cost per analysis.
- Recordings are private; signed URLs with short expiry.
- Handle failures per stage: if pronunciation fails, still return transcript + grammar, and mark the missing part.
- UI: clean, calm, readable. Dark mode. Large tap targets. Feedback should sound like a good teacher, direct and specific, not cheerleading.
