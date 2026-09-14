# Usage examples

These are conversational requests, not shell commands. Ranges and product details are illustrative; use actual selected commits. Natural language and translated field labels work alongside the English subcommands.

## Technical note with a custom structure

```text
/release-notes technical
Commits: v0.5.1..v0.5.2
Público: engenheiros de plataforma
Foco: confiabilidade e diagnóstico
Apresentação: sem ícones
Estrutura: problema, mudanças, evidências, limites
Idioma: português
```

## User-facing notes with icons

```text
/release-notes release v0.5.1..v0.5.2
Em inglês, com ícones e foco no valor para operadores.
Destaque o isolamento entre workspaces.
```

## Plain-text announcement

```text
/release-notes announce v0.5.1..v0.5.2
Para LinkedIn, em inglês, texto simples e até 180 palavras.
Contexto: queremos explicar por que rastrear vários agentes ficou
mais previsível. Termine com um convite para consultar a release.
```

## Default mode and inherited evidence

```text
/release-notes after v2.4.0
Brief, without icons, for product users.
```

Follow-up in the same conversation:

```text
/release-notes technical
Use the same commits. Focus on compatibility for SDK developers.
```

## Dates and supplied history

```text
/release-notes release
Commits: main, January 1 through January 31, 2025, Europe/Brussels.
Use the repository already selected in this conversation.
```

Without repository access, supply the selected commit output with its repository and range. Additional focus text can explain intent, but cannot replace those commits.
