# App Store Connect Skill for Claude Code

A comprehensive Claude Code skill for managing the Apple App Store Connect REST API (v1/v2), xcodebuild CI/CD pipeline, and iOS app lifecycle.

## What This Skill Does

When loaded into Claude Code, this skill gives Claude full knowledge of the App Store Connect API, enabling it to:

- **Metadata & Localization** -- Update descriptions, keywords, subtitles, categories, and translate to 30+ locales
- **Screenshots & Previews** -- Upload, reorder, and delete screenshots and app preview videos
- **Customer Reviews** -- Read reviews, respond with AI-assisted drafting, manage developer responses
- **TestFlight** -- Create beta groups, add testers, assign builds, submit for beta review
- **Submissions & Releases** -- Submit for App Review, manage phased releases, auto-increment versions
- **In-App Purchases & Subscriptions** -- Create IAPs, subscription groups, promotional offers, pricing
- **Sales & Finance Reports** -- Download daily/weekly/monthly sales and finance TSV reports
- **Advanced Features** -- In-app events, custom product pages, app clips
- **Build & Deploy** -- Archive, sign, and upload builds via xcodebuild CLI

## Hard Limitations (Cannot Be Done via API)

These are confirmed impossible as of April 2026:

| Operation | Alternative |
|-----------|------------|
| Create a new app | Manual: App Store Connect portal |
| Configure App Privacy | Manual: ASC privacy wizard |
| Upload/change app icon | Set in Xcode asset catalog, bundled in build |
| Delete an app | Manual: remove from sale in ASC |
| Transfer an app | Manual: multi-step process in ASC |
| Manage agreements/contracts | Manual: appstoreconnect.apple.com/agreements/ |

## Installation

1. Copy the `SKILL.md` and `references/` directory to your Claude Code skills folder:

```bash
cp -r SKILL.md references/ ~/.claude/skills/app-store-connect/
```

2. Set up your credentials:

```bash
mkdir -p ~/.claude/skills/app-store-connect/config
cp config/credentials.local.md.example ~/.claude/skills/app-store-connect/config/credentials.local.md
```

3. Edit `config/credentials.local.md` with your App Store Connect API key details.

## Getting an API Key

1. Go to [App Store Connect](https://appstoreconnect.apple.com) > Users and Access > Integrations > App Store Connect API
2. Generate a new key with appropriate permissions
3. Download the `.p8` private key file (only available once)
4. Note your Key ID and Issuer ID

## File Structure

```
app-store-connect/
├── SKILL.md                              # Core skill (loaded when triggered)
├── config/
│   ├── credentials.local.md.example      # Template for your credentials
│   └── credentials.local.md              # Your credentials (gitignored)
└── references/
    ├── metadata-and-localization.md       # Descriptions, keywords, subtitles, categories
    ├── screenshots-and-previews.md        # Screenshot/preview upload workflow
    ├── reviews-and-ratings.md             # Customer review management
    ├── testflight.md                      # Beta testing management
    ├── submissions-and-releases.md        # App Review, phased release, versioning
    ├── iap-and-subscriptions.md           # In-app purchases, subscriptions, pricing
    ├── reports-and-analytics.md           # Sales and finance reports
    ├── advanced-features.md               # Events, custom pages, app clips
    └── build-and-deploy.md                # xcodebuild archive and upload
```

## Requirements

- Python 3 with `PyJWT` and `requests` (`pip install PyJWT requests`)
- Xcode (for build archiving and simulator screenshots)
- An App Store Connect API key with appropriate permissions

## License

MIT
