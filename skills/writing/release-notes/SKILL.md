---
name: release-notes
description: Write concise, user-centered product release notes from supplied change material or Git commit messages selected by date range or commit point.
category: writing
---

# Release Notes

Turn change evidence into clear product communication. Explain what changed, why it matters, and what a user can now do; do not publish a technical commit digest.

## Inputs

Use one or both of these evidence sources:

- Optional material supplied by the caller: draft notes, tickets, changelog items, launch context, audience, product terminology, or constraints.
- Git commit messages from an explicitly requested selector:
  - date range: `git log --no-merges --since=<start> --until=<end> --format=%x1e%s%x1f%b`
  - after a commit point: `git log --no-merges <commit>..HEAD --format=%x1e%s%x1f%b`

Treat record separator `0x1e` as the start of each commit and unit separator `0x1f` as the boundary between its subject and body. For date-only input, treat both dates as inclusive and normalize the end to `23:59:59` in the caller's stated timezone; ask for the timezone when ambiguity could change the selected commits. Preserve explicit timestamps as given.

The caller may provide equivalent commit output instead of repository access. Do not choose a date range, commit point, repository, audience, version, or destination by guessing.

## Prerequisites

- No tools are required when the caller supplies the change material.
- To collect commits: Git, read access to the target repository and history, and permission to run read-only `git log` commands.

## Commands

### `/release-notes [change material | --since <date> --until <date> | --after <commit>]`

- **Input:** Optional supplied content and/or exactly identified Git history. Audience, tone, version, and product vocabulary are optional.
- **Action:** Gather evidence, remove internal-only noise, group related changes, assess the user meaning and intent of each group, then write and quality-check the notes.
- **Output:** Release-note content only. The caller owns where, how, and whether it is saved or published; never assume a file, path, platform, or delivery channel.
- **Failure:** If no usable material or selector is available, ask for supplied content, a start and end date, or a commit point. If Git access or a revision fails, report the exact problem and request equivalent commit output. If a potentially user-visible change has uncertain meaning, stop and ask a focused clarification question before returning any notes; never mix questions or uncertainty markers into publishable copy.

## Workflow

1. **Collect evidence.** Use supplied material first and augment it only with the explicitly selected commits. Treat commit text as evidence, not publishable prose.
2. **Filter safely.** Exclude merges, chores, refactors, dependency bumps, test-only work, and implementation details unless they produce a user-visible outcome. Never expose secrets, internal links, incident details, or unsupported claims.
3. **Synthesize.** Combine duplicates and related changes into a small number of coherent themes. Infer category, meaning, and product intention only when supported by evidence. Keep distinct user outcomes separate.
4. **Prioritize.** Lead with the highest user value or broadest impact. Use progressive disclosure: outcome first, necessary detail second. Mention migration, availability, permissions, limitations, or action required when supported.
5. **Write.** Use a benefit-led title and short entries in the pattern below. Prefer categories that describe the release (`New`, `Improved`, `Fixed`, `Action required`) rather than forcing empty sections.
6. **Check.** Apply the language guide and evidence check before returning the notes.

## User-centered structure

For each meaningful group, use:

> **Outcome-led heading** — What users can now do or experience. Add why it matters and any essential condition, limitation, or next step.

Follow established product communication patterns:

- **Benefit before feature:** lead with the job or outcome, then name the capability.
- **Jobs-to-be-done framing:** describe progress in the user's task, not the team's implementation.
- **Inverted pyramid:** put the most important information first.
- **Progressive disclosure:** keep the scan concise; add only details needed to act or understand impact.
- **Transparent change communication:** state availability, rollout, breaking behavior, and required action plainly when known.

Do not turn every commit into a bullet. A good note may summarize many commits in one entry or omit commits with no user-visible meaning.

## Language guide

### Positive hints

- Start with an active user outcome: “Find…”, “Create…”, “Stay…”, “You can now…”.
- Use plain, concrete words and short sentences.
- Say who benefits and under what conditions when scope is limited.
- Connect the change to saved time, reduced effort, confidence, control, access, or another evidenced benefit.
- Use calm, factual language and preserve the caller's product terminology.

### Red flags

Revise text that:

- repeats commit subjects or ticket titles without explaining meaning;
- leads with internals such as API names, database changes, refactors, libraries, or architecture;
- uses team-centered phrasing such as “we added”, “we implemented”, or “our engineers”;
- claims “faster”, “easier”, “secure”, “best”, or similar benefits without evidence;
- uses vague hype such as “exciting”, “revolutionary”, “seamless”, or “game-changing”;
- exposes hashes, ticket IDs, internal codenames, or confidential context;
- hides a breaking change, required action, limitation, or availability constraint;
- creates empty categories or one bullet per commit merely to appear complete.

## Final check

Return notes only when every entry:

- represents a user-visible outcome supported by the source evidence;
- is grouped by meaning rather than commit order;
- explains value or intention without speculation;
- is understandable without engineering context;
- includes material action, scope, or limitation information;
- avoids all red flags above;
- leaves storage and publication decisions to the caller.

Maintainers can exercise these rules with the pass/fail cases in [`checklists/evals.md`](checklists/evals.md).

## Credits

- Keep a Changelog, for human-readable, categorized change communication: https://keepachangelog.com/
- GOV.UK Content Design, for user needs, plain language, and front-loading important information: https://www.gov.uk/guidance/content-design
- Intercom, *Writing a Changelog*, for benefit-led product update communication: https://www.intercom.com/blog/writing-a-changelog/
- Jobs-to-be-Done theory, for framing product changes around user progress and outcomes.
