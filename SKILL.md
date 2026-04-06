---
name: app-store-connect
description: >
  This skill should be used when the user asks to "upload to App Store", "manage App Store Connect",
  "update app metadata", "upload screenshots", "set app description", "set keywords", "manage TestFlight",
  "add beta testers", "check app reviews", "respond to reviews", "submit for review", "set app pricing",
  "create in-app purchase", "manage subscriptions", "check sales reports", "download finance report",
  "download analytics", "set phased release", "pause phased release", "resume phased release",
  "create app event", "manage app clips", "deploy iOS app", "archive and upload build",
  "translate app metadata", "check app status", "manage app store listing", "nominate for featuring",
  "create custom product page", "set age rating", "manage release notes", "set app category",
  "upload app preview", "check build status", "list builds", "set privacy policy URL",
  "set content rights", "set review contact info", "create new app version", "increment version",
  "manage territory availability", "set app availability", "create promotional offer",
  "launch readiness check", "is my app ready to submit", "set copyright", "set support URL",
  "set marketing URL", "send TestFlight invitation", "delete screenshot", "reorder screenshots",
  "check app review status", or any App Store Connect operation.
  Covers the full Apple App Store Connect REST API (v1/v2) plus xcodebuild CI/CD pipeline.
---

# App Store Connect — Full Management Skill

Complete App Store Connect management via REST API and xcodebuild CLI.

## Credentials

Load credentials from `config/credentials.local.md` (gitignored). That file contains:
- Key ID, Issuer ID, Private Key path, Team ID
- Default contact info (company, email, phone, copyright)

## Authentication (Required for All API Calls)

```python
import jwt, time, requests

# Load these values from config/credentials.local.md
KEY_ID = "YOUR_KEY_ID"           # See config/credentials.local.md
ISSUER_ID = "YOUR_ISSUER_ID"    # See config/credentials.local.md
KEY_PATH = "/path/to/AuthKey.p8" # See config/credentials.local.md

with open(KEY_PATH, 'r') as f:
    private_key = f.read()

payload = {"iss": ISSUER_ID, "iat": int(time.time()), "exp": int(time.time()) + 1200, "aud": "appstoreconnect-v1"}
token = jwt.encode(payload, private_key, algorithm="ES256", headers={"kid": KEY_ID})
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
```

## Core ID Resolution (Always Do First)

Most operations require these IDs. Resolve them before any update:

```python
# 1. Get APP_ID
response = requests.get("https://api.appstoreconnect.apple.com/v1/apps", headers=headers)
for app in response.json()['data']:
    print(f"{app['attributes']['name']} - {app['attributes']['bundleId']} (ID: {app['id']})")
APP_ID = "the-app-id"

# 2. Get VERSION_ID
response = requests.get(f"https://api.appstoreconnect.apple.com/v1/apps/{APP_ID}/appStoreVersions", headers=headers)
VERSION_ID = response.json()['data'][0]['id']

# 3. Get LOCALIZATION_ID (for version-level metadata)
response = requests.get(f"https://api.appstoreconnect.apple.com/v1/appStoreVersions/{VERSION_ID}/appStoreVersionLocalizations", headers=headers)
LOCALIZATION_ID = response.json()['data'][0]['id']

# 4. Get APP_INFO_ID and APP_INFO_LOC_ID (for app-level metadata)
response = requests.get(f"https://api.appstoreconnect.apple.com/v1/apps/{APP_ID}/appInfos", headers=headers)
APP_INFO_ID = response.json()['data'][0]['id']
response = requests.get(f"https://api.appstoreconnect.apple.com/v1/appInfos/{APP_INFO_ID}/appInfoLocalizations", headers=headers)
APP_INFO_LOC_ID = response.json()['data'][0]['id']
```

## Operations Index

| Area | Operations | Reference File |
|------|-----------|----------------|
| **Metadata & Localization** | Description, keywords, subtitle, copyright, category, promo text, multi-locale, AI translation | `references/metadata-and-localization.md` |
| **Screenshots & Previews** | Upload screenshots, app previews, simulator automation, screenshot sizes | `references/screenshots-and-previews.md` |
| **Customer Reviews** | List reviews, respond, delete responses, AI-assisted responses | `references/reviews-and-ratings.md` |
| **TestFlight** | Beta groups, testers, builds, beta review submission, invitations | `references/testflight.md` |
| **Submissions & Releases** | Submit for review, phased release, version increment, nominations | `references/submissions-and-releases.md` |
| **IAP & Subscriptions** | In-app purchases, subscription groups, promo offers, pricing | `references/iap-and-subscriptions.md` |
| **Reports & Analytics** | Sales reports, finance reports, download TSV data | `references/reports-and-analytics.md` |
| **Advanced Features** | In-app events, custom product pages, app clips | `references/advanced-features.md` |
| **Build & Deploy** | Xcode archive, upload, ExportOptions, one-line deploy | `references/build-and-deploy.md` |

## API Permissions

- GET apps, versions, localizations, reviews, builds, reports
- UPDATE metadata, screenshots, categories, reviews, TestFlight, releases
- CREATE versions, localizations, screenshots, IAPs, subscriptions, events

## Hard Limitations (Cannot Be Done via API)

These operations are **confirmed impossible** via the App Store Connect REST API as of April 2026.
Do NOT attempt these programmatically — they will fail or have no endpoint.

| Operation | Why Not | What to Do Instead |
|-----------|---------|-------------------|
| **Create a new app** | No `POST /v1/apps` endpoint exists. API keys get `403 FORBIDDEN`. Fastlane `produce` also cannot do this with API keys. | Create manually at https://appstoreconnect.apple.com -> Apps -> + -> New App |
| **Configure App Privacy** | No API endpoints exist for the privacy questionnaire (data collection types, tracking declarations). Apple provides only a web-based wizard. | Configure manually: ASC -> Apps -> [App] -> App Privacy -> Get Started |
| **Upload or change app icon** | Icons are embedded in the Xcode asset catalog and bundled into the binary. There is no separate icon upload endpoint. Changing an icon requires a new build. | Set icon in Xcode: Assets.xcassets -> AppIcon, then archive and upload a new build |
| **Retrieve app icon image** | Limited: `iconAssetToken` on build resources may return icon URLs, but there is no dedicated icon download endpoint. Results vary. | Best approach: extract from the Xcode project asset catalog, or use the App Store marketing artwork URL |
| **Delete an app** | Apps cannot be deleted via API. They can be removed from sale or fully removed (if never published). | Remove manually: ASC -> Apps -> [App] -> Remove App (see [Apple docs](https://developer.apple.com/help/app-store-connect/create-an-app-record/remove-an-app/)) |
| **Transfer an app** | App transfers are a multi-step manual process between two developer accounts. No API support. | Initiate manually: ASC -> Apps -> [App] -> Transfer App |
| **Manage agreements/contracts** | Paid/free app agreements, tax forms, and banking details have no API. | Manage at https://appstoreconnect.apple.com/agreements/ |
| **Configure Privacy Manifests** | PrivacyInfo.xcprivacy files are part of the Xcode project, not ASC metadata. | Add PrivacyInfo.xcprivacy to Xcode project before building |

**Note on age rating:** Despite being listed as "manual" in some guides, age ratings CAN be configured via API using `PATCH /v1/ageRatingDeclarations/{id}`. This skill covers it in `references/metadata-and-localization.md`.

## Common Errors

| Error | Solution |
|-------|----------|
| `whatsNew cannot be edited` | Remove whatsNew for new apps (only available for updates) |
| `403 FORBIDDEN on CREATE apps` | This is a hard API limitation, not a permissions issue. Create app manually in ASC portal |
| `Invalid bundle ID` | Ensure bundle ID is registered in Developer portal first |
| `JWT expired` | Tokens last 20 minutes max; regenerate before each session |
| `ENTITY_ERROR.RELATIONSHIP` | Check that relationship IDs exist and are correct type |
| `Pending Agreements` | Accept latest agreements at https://appstoreconnect.apple.com/agreements/ |

## Full Workflow Checklist

### New App Release
- [ ] **MANUAL** Create app in App Store Connect (no API — see Hard Limitations)
- [ ] **MANUAL** Configure App Privacy questionnaire (no API — see Hard Limitations)
- [ ] **MANUAL** Set app icon in Xcode asset catalog (icon is bundled in build, no API)
- [ ] Resolve IDs: APP_ID, VERSION_ID, LOCALIZATION_ID, APP_INFO_ID
- [ ] Update description, keywords, promotionalText, supportUrl
- [ ] Set subtitle (max 30 chars), copyright, category
- [ ] Set age rating declaration (API supported)
- [ ] Set content rights declaration
- [ ] Upload screenshots for each device size
- [ ] Set review contact info
- [ ] Archive and upload build via xcodebuild
- [ ] Set marketing/support/privacy URLs
- [ ] Submit for App Review
- [ ] Optionally enable phased release

### App Update
- [ ] Create new version (or auto-increment)
- [ ] Update whatsNew (release notes) for all locales
- [ ] Update screenshots if UI changed
- [ ] Upload new build
- [ ] Submit for review
- [ ] Monitor phased release

### Ongoing Management
- [ ] Monitor and respond to customer reviews
- [ ] Manage TestFlight beta testers and builds
- [ ] Download sales and finance reports
- [ ] Create in-app events for promotions
- [ ] Update pricing and availability as needed

## App Privacy (Manual)

App Privacy must be configured manually in App Store Connect:
1. App Store Connect -> Apps -> [App] -> App Privacy
2. For apps with no data collection: select "Data Not Collected"
3. Privacy Policy URL: `https://yourcompany.com/privacy`

## Creating a New App (Manual)

1. Go to https://appstoreconnect.apple.com
2. Apps -> + -> New App
3. Platform: iOS, Primary Language: English (U.S.)
4. Bundle ID: select from registered IDs (NOT widget extensions)
5. SKU: unique identifier (e.g., appname001)
