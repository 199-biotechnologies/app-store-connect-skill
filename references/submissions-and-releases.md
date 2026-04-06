# Submissions & Releases

Submit for review, manage phased releases, auto-increment versions, and nominate for featuring.

## Submit for App Review

```python
submission_data = {
    "data": {
        "type": "appStoreVersionSubmissions",
        "relationships": {
            "appStoreVersion": {
                "data": {"type": "appStoreVersions", "id": VERSION_ID}
            }
        }
    }
}
requests.post(
    "https://api.appstoreconnect.apple.com/v1/appStoreVersionSubmissions",
    headers=headers, json=submission_data
)
```

**Prerequisites before submission:**
- All required metadata fields populated (description, keywords, screenshots)
- Build uploaded and processed
- Age rating configured
- Review contact info set
- Content rights declared
- App privacy configured (manual in ASC portal)

## Release an Approved Version

After Apple approves a version, manually release it:

```python
release_data = {
    "data": {
        "type": "appStoreVersionReleaseRequests",
        "relationships": {
            "appStoreVersion": {
                "data": {"type": "appStoreVersions", "id": VERSION_ID}
            }
        }
    }
}
requests.post(
    "https://api.appstoreconnect.apple.com/v1/appStoreVersionReleaseRequests",
    headers=headers, json=release_data
)
```

## Phased Release

Gradual rollout over 7 days: 1% -> 2% -> 5% -> 10% -> 20% -> 50% -> 100%.

### Enable Phased Release

```python
phased_data = {
    "data": {
        "type": "appStoreVersionPhasedReleases",
        "attributes": {"phasedReleaseState": "INACTIVE"},
        "relationships": {
            "appStoreVersion": {
                "data": {"type": "appStoreVersions", "id": VERSION_ID}
            }
        }
    }
}
response = requests.post(
    "https://api.appstoreconnect.apple.com/v1/appStoreVersionPhasedReleases",
    headers=headers, json=phased_data
)
PHASED_RELEASE_ID = response.json()['data']['id']
```

### Check Phased Release Status

```python
response = requests.get(
    f"https://api.appstoreconnect.apple.com/v1/appStoreVersions/{VERSION_ID}/appStoreVersionPhasedRelease",
    headers=headers
)
state = response.json()['data']['attributes']
print(f"State: {state['phasedReleaseState']}, Day: {state.get('currentDayNumber')}")
```

### Pause Phased Release

Use when crash reports spike:

```python
requests.patch(
    f"https://api.appstoreconnect.apple.com/v1/appStoreVersionPhasedReleases/{PHASED_RELEASE_ID}",
    headers=headers,
    json={"data": {"type": "appStoreVersionPhasedReleases", "id": PHASED_RELEASE_ID,
                    "attributes": {"phasedReleaseState": "PAUSED"}}}
)
```

### Resume Phased Release

```python
requests.patch(
    f"https://api.appstoreconnect.apple.com/v1/appStoreVersionPhasedReleases/{PHASED_RELEASE_ID}",
    headers=headers,
    json={"data": {"type": "appStoreVersionPhasedReleases", "id": PHASED_RELEASE_ID,
                    "attributes": {"phasedReleaseState": "ACTIVE"}}}
)
```

### Immediately Release to All Users

```python
requests.patch(
    f"https://api.appstoreconnect.apple.com/v1/appStoreVersionPhasedReleases/{PHASED_RELEASE_ID}",
    headers=headers,
    json={"data": {"type": "appStoreVersionPhasedReleases", "id": PHASED_RELEASE_ID,
                    "attributes": {"phasedReleaseState": "COMPLETE"}}}
)
```

States: `INACTIVE`, `ACTIVE`, `PAUSED`, `COMPLETE`.

## Version Auto-Increment

### Create a New Version

```python
# Get current latest version number
response = requests.get(
    f"https://api.appstoreconnect.apple.com/v1/apps/{APP_ID}/appStoreVersions",
    headers=headers,
    params={"sort": "-createdDate", "limit": 1}
)
current_version = response.json()['data'][0]['attributes']['versionString']

# Compute next version (e.g., "1.2.0" -> "1.3.0")
parts = current_version.split('.')
while len(parts) < 3:
    parts.append('0')  # Ensure 3-part version
parts[1] = str(int(parts[1]) + 1)
parts[2] = '0'
next_version = '.'.join(parts)

# Create new version
version_data = {
    "data": {
        "type": "appStoreVersions",
        "attributes": {
            "versionString": next_version,
            "platform": "IOS"
        },
        "relationships": {
            "app": {"data": {"type": "apps", "id": APP_ID}}
        }
    }
}
response = requests.post(
    "https://api.appstoreconnect.apple.com/v1/appStoreVersions",
    headers=headers, json=version_data
)
NEW_VERSION_ID = response.json()['data']['id']
```

**Note:** This creates the ASC version entry. The actual build version (CFBundleShortVersionString) must match and is set in Xcode/Info.plist.

## Featured App Nomination

Nominate an app for editorial featuring:

```python
nomination_data = {
    "data": {
        "type": "nominations",
        "attributes": {
            "description": "Brief description of why this app deserves featuring...",
            "releaseDate": "2026-05-01"
        },
        "relationships": {
            "app": {"data": {"type": "apps", "id": APP_ID}}
        }
    }
}
requests.post(
    "https://api.appstoreconnect.apple.com/v1/nominations",
    headers=headers, json=nomination_data
)
```

## Launch Readiness Check

Aggregate multiple API calls to verify an app is ready for submission:

```python
def check_launch_readiness(APP_ID, VERSION_ID, headers):
    checks = []

    # Check version exists and has a build
    r = requests.get(f"https://api.appstoreconnect.apple.com/v1/appStoreVersions/{VERSION_ID}",
                     headers=headers, params={"include": "build"})
    version = r.json()
    has_build = version.get('included') and len(version['included']) > 0
    checks.append(("Build attached", has_build))

    # Check localizations have required fields
    r = requests.get(f"https://api.appstoreconnect.apple.com/v1/appStoreVersions/{VERSION_ID}/appStoreVersionLocalizations",
                     headers=headers)
    locs = r.json()['data']
    for loc in locs:
        attrs = loc['attributes']
        has_desc = bool(attrs.get('description'))
        has_keywords = bool(attrs.get('keywords'))
        checks.append((f"Description ({attrs['locale']})", has_desc))
        checks.append((f"Keywords ({attrs['locale']})", has_keywords))

    # Check screenshots exist
    for loc in locs:
        r = requests.get(f"https://api.appstoreconnect.apple.com/v1/appStoreVersionLocalizations/{loc['id']}/appScreenshotSets",
                         headers=headers)
        has_screenshots = len(r.json()['data']) > 0
        checks.append((f"Screenshots ({loc['attributes']['locale']})", has_screenshots))

    # Check review detail
    r = requests.get(f"https://api.appstoreconnect.apple.com/v1/appStoreVersions/{VERSION_ID}/appStoreReviewDetail",
                     headers=headers)
    has_review_detail = r.status_code == 200 and r.json().get('data')
    checks.append(("Review contact info", has_review_detail))

    # Print results
    all_pass = True
    for name, passed in checks:
        status = "PASS" if passed else "FAIL"
        if not passed: all_pass = False
        print(f"  [{status}] {name}")

    return all_pass
```
