# Release Notes evals

Use these pass/fail cases when changing the skill.

## 1. Supplied material

- **Prompt:** `/release-notes Added saved filters to search; users can reuse them across sessions. Refactored query parser. Fixed a crash when an empty filter is opened.`
- **Expected:** Groups the saved-filter capability and related fix by user meaning; omits the refactor.
- **Must include:** A user outcome and the empty-filter reliability improvement.
- **Must not include:** A destination, “we implemented”, or a bullet that merely repeats each source line.
- **Pass:** Concise, plain-language notes whose claims are supported by the input.

## 2. Date range

- **Prompt:** `/release-notes --since 2025-01-01 --until 2025-01-31`
- **Expected:** Uses only the explicit read-only Git range, then synthesizes user-visible changes.
- **Must include:** Grouping by meaning and any evidenced scope or required action.
- **Must not include:** Guessed dates, raw hashes, merge commits, or internal-only work.
- **Pass:** The selected history is respected and the output is not a commit digest.

## 3. Commit point

- **Prompt:** `/release-notes --after v2.4.0`
- **Expected:** Reads `v2.4.0..HEAD`; reports a missing revision rather than silently choosing another one.
- **Must include:** Benefit-led, user-centered wording for supported outcomes.
- **Must not include:** Unsupported performance or security claims.
- **Pass:** Evidence boundaries and safe failure behavior are honored.

## 4. Missing evidence

- **Prompt:** `/release-notes`
- **Expected:** Requests supplied change material, a date range, or a commit point.
- **Must include:** A focused clarification request.
- **Must not include:** Invented release content or an assumed repository/destination.
- **Pass:** No release notes are fabricated.
