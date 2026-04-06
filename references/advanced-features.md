# Advanced Features

In-app events, custom product pages, and app clips.

## In-App Events

Promote time-sensitive content on the App Store (challenges, competitions, premieres).

### Create an Event

```python
event_data = {
    "data": {
        "type": "appEvents",
        "attributes": {
            "referenceName": "Summer Challenge 2026",
            "badge": "CHALLENGE",
            "deepLink": "myapp://events/summer2026",
            "purchaseRequirement": "NO_COST_ASSOCIATED",
            "purpose": "APPROPRIATE_FOR_ALL_USERS",
            "primaryLocale": "en-US",
            "priority": "NORMAL",
            "territorySchedules": [{
                "territories": ["USA", "GBR", "CAN"],
                "publishStart": "2026-06-01T00:00:00Z",
                "eventStart": "2026-06-01T08:00:00Z",
                "eventEnd": "2026-08-31T23:59:00Z"
            }]
        },
        "relationships": {
            "app": {"data": {"type": "apps", "id": APP_ID}}
        }
    }
}
response = requests.post(
    "https://api.appstoreconnect.apple.com/v1/appEvents",
    headers=headers, json=event_data
)
EVENT_ID = response.json()['data']['id']
```

Badge values: `LIVE_EVENT`, `PREMIERE`, `CHALLENGE`, `COMPETITION`, `NEW_SEASON`, `MAJOR_UPDATE`, `SPECIAL_EVENT`.

### Add Event Localization

```python
loc_data = {
    "data": {
        "type": "appEventLocalizations",
        "attributes": {
            "locale": "en-US",
            "name": "Summer Fitness Challenge",
            "shortDescription": "30 days of daily workouts",
            "longDescription": "Join thousands of users in our annual summer challenge..."
        },
        "relationships": {
            "appEvent": {"data": {"type": "appEvents", "id": EVENT_ID}}
        }
    }
}
requests.post(
    "https://api.appstoreconnect.apple.com/v1/appEventLocalizations",
    headers=headers, json=loc_data
)
```

Limits: 10 published events at a time, 15 approved events total.

### List Events

```python
response = requests.get(
    f"https://api.appstoreconnect.apple.com/v1/apps/{APP_ID}/appEvents",
    headers=headers
)
```

## Custom Product Pages

Create different store listings for different ad campaigns. Each gets a unique App Store URL.

### Create a Custom Product Page

```python
cpp_data = {
    "data": {
        "type": "appCustomProductPages",
        "attributes": {"name": "Holiday Campaign 2026"},
        "relationships": {
            "app": {"data": {"type": "apps", "id": APP_ID}}
        }
    }
}
response = requests.post(
    "https://api.appstoreconnect.apple.com/v1/appCustomProductPages",
    headers=headers, json=cpp_data
)
CPP_ID = response.json()['data']['id']
```

### Create a Version for the Custom Page

```python
version_data = {
    "data": {
        "type": "appCustomProductPageVersions",
        "relationships": {
            "appCustomProductPage": {
                "data": {"type": "appCustomProductPages", "id": CPP_ID}
            }
        }
    }
}
response = requests.post(
    "https://api.appstoreconnect.apple.com/v1/appCustomProductPageVersions",
    headers=headers, json=version_data
)
CPP_VERSION_ID = response.json()['data']['id']
```

### Add Localization to Custom Page

```python
loc_data = {
    "data": {
        "type": "appCustomProductPageLocalizations",
        "attributes": {
            "locale": "en-US",
            "promotionalText": "Special holiday offer!"
        },
        "relationships": {
            "appCustomProductPageVersion": {
                "data": {"type": "appCustomProductPageVersions", "id": CPP_VERSION_ID}
            }
        }
    }
}
requests.post(
    "https://api.appstoreconnect.apple.com/v1/appCustomProductPageLocalizations",
    headers=headers, json=loc_data
)
```

### List Custom Pages

```python
response = requests.get(
    f"https://api.appstoreconnect.apple.com/v1/apps/{APP_ID}/appCustomProductPages",
    headers=headers
)
```

Maximum 35 custom product pages per app.

## App Clips

Configure App Clip card experiences for NFC/QR code invocations.

### Create Default Experience

```python
# Get app clip ID
response = requests.get(
    f"https://api.appstoreconnect.apple.com/v1/apps/{APP_ID}/appClips",
    headers=headers
)
APP_CLIP_ID = response.json()['data'][0]['id']

experience_data = {
    "data": {
        "type": "appClipDefaultExperiences",
        "attributes": {"action": "OPEN"},
        "relationships": {
            "appClip": {"data": {"type": "appClips", "id": APP_CLIP_ID}},
            "releaseWithAppStoreVersion": {
                "data": {"type": "appStoreVersions", "id": VERSION_ID}
            }
        }
    }
}
response = requests.post(
    "https://api.appstoreconnect.apple.com/v1/appClipDefaultExperiences",
    headers=headers, json=experience_data
)
EXPERIENCE_ID = response.json()['data']['id']
```

Actions: `OPEN`, `VIEW`, `PLAY`.

### Add Localization to App Clip Card

```python
loc_data = {
    "data": {
        "type": "appClipDefaultExperienceLocalizations",
        "attributes": {
            "locale": "en-US",
            "subtitle": "Track your health instantly"
        },
        "relationships": {
            "appClipDefaultExperience": {
                "data": {"type": "appClipDefaultExperiences", "id": EXPERIENCE_ID}
            }
        }
    }
}
requests.post(
    "https://api.appstoreconnect.apple.com/v1/appClipDefaultExperienceLocalizations",
    headers=headers, json=loc_data
)
```
