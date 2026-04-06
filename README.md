<div align="center">

# App Store Connect Skill for Claude Code

**Manage your entire iOS app lifecycle from the terminal — metadata, screenshots, reviews, TestFlight, subscriptions, and releases.**

<br />

[![Star this repo](https://img.shields.io/github/stars/199-biotechnologies/app-store-connect-skill?style=for-the-badge&logo=github&label=%E2%AD%90%20Star%20this%20repo&color=yellow)](https://github.com/199-biotechnologies/app-store-connect-skill/stargazers)
&nbsp;&nbsp;
[![Follow @longevityboris](https://img.shields.io/badge/Follow_%40longevityboris-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/longevityboris)

<br />

[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
&nbsp;
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)](https://github.com/199-biotechnologies/app-store-connect-skill/pulls)
&nbsp;
[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-8A2BE2?style=for-the-badge)](https://docs.anthropic.com/en/docs/claude-code)

---

A Claude Code skill that turns your terminal into a full App Store Connect dashboard. Update metadata across 30+ locales, upload screenshots, respond to reviews, manage TestFlight testers, create subscriptions, download sales reports, and submit for review — all through natural language.

[Install](#install) | [What You Can Do](#what-you-can-do) | [How It Works](#how-it-works) | [Hard Limitations](#hard-limitations) | [Contributing](#contributing)

</div>

## The Problem

App Store Connect's web UI is slow and repetitive. Updating metadata across multiple locales means clicking through dozens of screens. Managing TestFlight testers is tedious. Downloading sales reports requires navigating a maze of dropdowns. And if you have multiple apps, multiply all of that.

## How This Skill Fixes It

Tell Claude what you need in plain English. The skill gives Claude deep knowledge of every App Store Connect API endpoint, so it writes and executes the right API calls for you.

```
You: "Update the description for my app in English, French, and Japanese"
You: "Add these 5 screenshots to the 6.7-inch iPhone set"
You: "Respond to all 1-star reviews from the last week"
You: "Create a monthly subscription at $4.99 with a free trial"
You: "Submit version 2.1 for review with phased release enabled"
```

No subscription fees. No config files. No memorising API endpoints.

## What You Can Do

| Area | Operations |
|------|-----------|
| **Metadata & Localization** | Descriptions, keywords, subtitles, categories, copyright, promo text, multi-locale translation with AI |
| **Screenshots & Previews** | Upload, reorder, delete screenshots and app preview videos. Simulator automation |
| **Customer Reviews** | Read reviews, filter by rating, respond with AI-drafted replies, delete responses |
| **TestFlight** | Create beta groups, add testers, assign builds, submit for beta review, send invitations |
| **Submissions & Releases** | Submit for App Review, phased release (pause/resume/complete), version auto-increment, nominations |
| **In-App Purchases** | Create consumables, non-consumables, subscription groups, subscriptions, promotional offers |
| **Pricing** | Set prices per territory, manage availability, schedule price changes |
| **Sales & Finance** | Download daily/weekly/monthly sales reports, finance reports as TSV |
| **In-App Events** | Create challenges, competitions, premieres with scheduling and localization |
| **Custom Product Pages** | Create campaign-specific store listings with unique URLs |
| **App Clips** | Configure default and advanced App Clip card experiences |
| **Build & Deploy** | Archive, sign, and upload builds via xcodebuild CLI |

## Install

Three commands:

```bash
# 1. Clone the skill
git clone https://github.com/199-biotechnologies/app-store-connect-skill.git \
  ~/.claude/skills/app-store-connect

# 2. Set up your credentials
cp ~/.claude/skills/app-store-connect/config/credentials.local.md.example \
   ~/.claude/skills/app-store-connect/config/credentials.local.md

# 3. Edit with your API key details
$EDITOR ~/.claude/skills/app-store-connect/config/credentials.local.md
```

Need an API key? Go to [App Store Connect](https://appstoreconnect.apple.com) > Users and Access > Integrations > App Store Connect API. Generate a key, download the `.p8` file (available once only), and note your Key ID and Issuer ID.

## How It Works

The skill uses **progressive disclosure** to stay lightweight:

```
app-store-connect/
├── SKILL.md                     # Core skill — auth, ID resolution, operations index
├── config/
│   └── credentials.local.md     # Your API credentials (gitignored)
└── references/
    ├── metadata-and-localization.md
    ├── screenshots-and-previews.md
    ├── reviews-and-ratings.md
    ├── testflight.md
    ├── submissions-and-releases.md
    ├── iap-and-subscriptions.md
    ├── reports-and-analytics.md
    ├── advanced-features.md
    └── build-and-deploy.md
```

`SKILL.md` loads when Claude detects an App Store task. It contains auth setup, ID resolution patterns, and an index pointing to the 9 reference files. Claude only reads the specific reference file it needs for your request — keeping context lean and responses fast.

## Hard Limitations

These operations are confirmed impossible via the App Store Connect REST API as of April 2026. The skill documents these clearly so Claude won't waste time attempting them.

| Operation | Why | What to Do Instead |
|-----------|-----|-------------------|
| **Create a new app** | No `POST /v1/apps` endpoint exists | Create manually in the ASC portal |
| **Configure App Privacy** | No API endpoints for privacy questionnaire | Manual: ASC > App Privacy wizard |
| **Upload/change app icon** | Icons are embedded in the Xcode binary | Set in Xcode asset catalog, then upload a new build |
| **Delete an app** | No delete endpoint | Remove from sale in ASC portal |
| **Transfer an app** | Multi-step manual process | Initiate in ASC portal |
| **Manage agreements** | Tax, banking, contracts have no API | Handle at appstoreconnect.apple.com/agreements/ |
| **Privacy manifests** | PrivacyInfo.xcprivacy is an Xcode project file | Add to your Xcode project before building |

## Requirements

- **Python 3** with `PyJWT` and `requests` — `pip install PyJWT requests`
- **Xcode** — for build archiving and simulator screenshots
- **App Store Connect API key** — with appropriate permissions

## Contributing

PRs are welcome. If you find a missing API endpoint or an outdated limitation, open an issue or submit a fix.

1. Fork the repo
2. Make your changes
3. Submit a PR with a clear description

## License

MIT

---

<div align="center">

Built by [Boris Djordjevic](https://github.com/longevityboris) at [Paperfoot AI](https://paperfoot.com)

<br />

**If this saves you time:**

[![Star this repo](https://img.shields.io/github/stars/199-biotechnologies/app-store-connect-skill?style=for-the-badge&logo=github&label=%E2%AD%90%20Star%20this%20repo&color=yellow)](https://github.com/199-biotechnologies/app-store-connect-skill/stargazers)
&nbsp;&nbsp;
[![Follow @longevityboris](https://img.shields.io/badge/Follow_%40longevityboris-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/longevityboris)

</div>
