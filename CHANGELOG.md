# Changelog

All notable changes to this repository are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/), versions follow [SemVer](https://semver.org/).

## [0.2.0] - 2026-10-17
### Added
- CI that validates every skill's frontmatter and blocks hardcoded brand names or local connector IDs.
- Issue templates, PR template, `CONTRIBUTING.md`, `SECURITY.md`, example `config.json`.

### Changed
- `ga4-roas-corridor-analysis`: brand-neutral — agency name and responsible person now come from `config.json`; Google Drive connector referenced by tool name instead of a local ID.

## [0.1.0] - 2026-05-20
### Added
- `ga4-roas-corridor-analysis` skill: 6-month ROAS corridor and budget forecast from GA4.
