# Metadata & Localization

All operations require AUTH headers and resolved IDs from SKILL.md.

## Update Description, Keywords & Promo Text

```python
update_data = {
    "data": {
        "type": "appStoreVersionLocalizations",
        "id": LOCALIZATION_ID,
        "attributes": {
            "description": "Your app description...",
            "keywords": "keyword1,keyword2,keyword3",  # Max 100 chars total
            "promotionalText": "Short promo text (170 chars max)",
            "supportUrl": "https://yourcompany.com/{slug}/support",
            "marketingUrl": "https://yourcompany.com/{slug}",
            "whatsNew": "Bug fixes and improvements"  # Only for updates, not new apps
        }
    }
}
requests.patch(
    f"https://api.appstoreconnect.apple.com/v1/appStoreVersionLocalizations/{LOCALIZATION_ID}",
    headers=headers, json=update_data
)
```

**Note:** `whatsNew` cannot be set for new apps (only for version updates).

## Set Subtitle (Max 30 Characters)

Subtitle is at the appInfoLocalizations level, not version level:

```python
update_data = {
    "data": {
        "type": "appInfoLocalizations",
        "id": APP_INFO_LOC_ID,
        "attributes": {
            "subtitle": "Your subtitle here"
        }
    }
}
requests.patch(
    f"https://api.appstoreconnect.apple.com/v1/appInfoLocalizations/{APP_INFO_LOC_ID}",
    headers=headers, json=update_data
)
```

## Set Copyright

```python
update_data = {
    "data": {
        "type": "appStoreVersions",
        "id": VERSION_ID,
        "attributes": {"copyright": "2026 Your Company"}
    }
}
requests.patch(
    f"https://api.appstoreconnect.apple.com/v1/appStoreVersions/{VERSION_ID}",
    headers=headers, json=update_data
)
```

## Set Category

```python
update_data = {
    "data": {
        "type": "appInfos",
        "id": APP_INFO_ID,
        "relationships": {
            "primaryCategory": {
                "data": {"type": "appCategories", "id": "HEALTH_AND_FITNESS"}
            }
        }
    }
}
requests.patch(
    f"https://api.appstoreconnect.apple.com/v1/appInfos/{APP_INFO_ID}",
    headers=headers, json=update_data
)
```

Common category IDs: `HEALTH_AND_FITNESS`, `MEDICAL`, `LIFESTYLE`, `PRODUCTIVITY`, `UTILITIES`, `EDUCATION`, `BUSINESS`, `FINANCE`, `SOCIAL_NETWORKING`, `ENTERTAINMENT`, `GAMES`, `SPORTS`, `TRAVEL`, `FOOD_AND_DRINK`, `WEATHER`, `MUSIC`, `PHOTO_AND_VIDEO`, `NAVIGATION`, `REFERENCE`, `NEWS`, `BOOKS`.

## Set Privacy Policy URL

```python
update_data = {
    "data": {
        "type": "appInfoLocalizations",
        "id": APP_INFO_LOC_ID,
        "attributes": {
            "privacyPolicyUrl": "https://yourcompany.com/privacy"
        }
    }
}
requests.patch(
    f"https://api.appstoreconnect.apple.com/v1/appInfoLocalizations/{APP_INFO_LOC_ID}",
    headers=headers, json=update_data
)
```

## Content Rights Declaration

```python
update_data = {
    "data": {
        "type": "apps",
        "id": APP_ID,
        "attributes": {
            "contentRightsDeclaration": "DOES_NOT_USE_THIRD_PARTY_CONTENT"
        }
    }
}
requests.patch(
    f"https://api.appstoreconnect.apple.com/v1/apps/{APP_ID}",
    headers=headers, json=update_data
)
```

Values: `DOES_NOT_USE_THIRD_PARTY_CONTENT`, `USES_THIRD_PARTY_CONTENT`.

## Age Rating

```python
response = requests.get(
    f"https://api.appstoreconnect.apple.com/v1/appInfos/{APP_INFO_ID}/ageRatingDeclaration",
    headers=headers
)
AGE_RATING_ID = response.json()['data']['id']

# All NONE for 4+ rating
update_data = {
    "data": {
        "type": "ageRatingDeclarations",
        "id": AGE_RATING_ID,
        "attributes": {
            "alcoholTobaccoOrDrugUseOrReferences": "NONE",
            "contests": "NONE",
            "gamblingSimulated": "NONE",
            "horrorOrFearThemes": "NONE",
            "matureOrSuggestiveThemes": "NONE",
            "medicalOrTreatmentInformation": "NONE",
            "profanityOrCrudeHumor": "NONE",
            "sexualContentGraphicAndNudity": "NONE",
            "sexualContentOrNudity": "NONE",
            "violenceCartoonOrFantasy": "NONE",
            "violenceRealistic": "NONE",
            "violenceRealisticProlongedGraphicOrSadistic": "NONE",
            "gambling": False,
            "unrestrictedWebAccess": False,
            "ageRatingOverride": "NONE"
        }
    }
}
requests.patch(
    f"https://api.appstoreconnect.apple.com/v1/ageRatingDeclarations/{AGE_RATING_ID}",
    headers=headers, json=update_data
)
```

For health apps with medical info, set `medicalOrTreatmentInformation` to `INFREQUENT_OR_MILD` or `FREQUENT_OR_INTENSE`.

## Review Contact Info

```python
create_data = {
    "data": {
        "type": "appStoreReviewDetails",
        "attributes": {
            "contactFirstName": "Your Company",
            "contactLastName": "Support",
            "contactPhone": "+44 20 8191 3199",
            "contactEmail": "support@yourcompany.com",
            "demoAccountRequired": False
        },
        "relationships": {
            "appStoreVersion": {
                "data": {"type": "appStoreVersions", "id": VERSION_ID}
            }
        }
    }
}
requests.post(
    "https://api.appstoreconnect.apple.com/v1/appStoreReviewDetails",
    headers=headers, json=create_data
)
```

## Multi-Locale Translation Workflow

To translate metadata to multiple locales:

### Step 1: List existing localizations

```python
response = requests.get(
    f"https://api.appstoreconnect.apple.com/v1/appStoreVersions/{VERSION_ID}/appStoreVersionLocalizations",
    headers=headers
)
existing_locales = {loc['attributes']['locale']: loc['id'] for loc in response.json()['data']}
```

### Step 2: Create missing localizations

```python
TARGET_LOCALES = ["fr-FR", "de-DE", "es-ES", "ja", "zh-Hans", "pt-BR", "it", "ko", "ar-SA", "nl-NL"]

for locale in TARGET_LOCALES:
    if locale not in existing_locales:
        create_data = {
            "data": {
                "type": "appStoreVersionLocalizations",
                "attributes": {"locale": locale},
                "relationships": {
                    "appStoreVersion": {
                        "data": {"type": "appStoreVersions", "id": VERSION_ID}
                    }
                }
            }
        }
        response = requests.post(
            "https://api.appstoreconnect.apple.com/v1/appStoreVersionLocalizations",
            headers=headers, json=create_data
        )
        existing_locales[locale] = response.json()['data']['id']
```

### Step 3: Translate with Claude and update each locale

For each locale, use Claude to translate the English description, keywords, and promo text, then PATCH each localization with the translated content. Also create appInfoLocalizations for subtitle translation:

```python
# Create app-info localization for subtitle in each locale
response = requests.get(
    f"https://api.appstoreconnect.apple.com/v1/appInfos/{APP_INFO_ID}/appInfoLocalizations",
    headers=headers
)
existing_info_locales = {loc['attributes']['locale']: loc['id'] for loc in response.json()['data']}

for locale in TARGET_LOCALES:
    if locale not in existing_info_locales:
        create_data = {
            "data": {
                "type": "appInfoLocalizations",
                "attributes": {"locale": locale},
                "relationships": {
                    "appInfo": {"data": {"type": "appInfos", "id": APP_INFO_ID}}
                }
            }
        }
        response = requests.post(
            "https://api.appstoreconnect.apple.com/v1/appInfoLocalizations",
            headers=headers, json=create_data
        )
```

### AI-Assisted Keyword Generation

Use Claude to generate optimized keywords:
1. Provide the app description, category, and current keywords
2. Ask Claude to generate keyword variations optimized for App Store search
3. Ensure total keyword string stays within 100 characters
4. Focus on high-volume, low-competition terms relevant to the app
5. PATCH the keywords field on each localization
