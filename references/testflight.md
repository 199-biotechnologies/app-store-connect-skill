# TestFlight Management

Manage beta testers, groups, builds, and beta review submissions.

## List Builds

```python
response = requests.get(
    "https://api.appstoreconnect.apple.com/v1/builds",
    headers=headers,
    params={
        "filter[app]": APP_ID,
        "sort": "-uploadedDate",
        "limit": 10,
        "fields[builds]": "version,uploadedDate,processingState,buildAudienceType"
    }
)
for build in response.json()['data']:
    attrs = build['attributes']
    print(f"Build {attrs['version']} - {attrs['processingState']} ({attrs['uploadedDate']})")
BUILD_ID = response.json()['data'][0]['id']  # Latest build
```

## Create a Beta Group

```python
group_data = {
    "data": {
        "type": "betaGroups",
        "attributes": {
            "name": "External Testers",
            "isInternalGroup": False,
            "hasAccessToAllBuilds": False,
            "publicLinkEnabled": True,
            "publicLinkLimit": 100
        },
        "relationships": {
            "app": {"data": {"type": "apps", "id": APP_ID}}
        }
    }
}
response = requests.post(
    "https://api.appstoreconnect.apple.com/v1/betaGroups",
    headers=headers, json=group_data
)
GROUP_ID = response.json()['data']['id']
```

## List Beta Groups

```python
response = requests.get(
    f"https://api.appstoreconnect.apple.com/v1/apps/{APP_ID}/betaGroups",
    headers=headers
)
for group in response.json()['data']:
    print(f"{group['attributes']['name']} (ID: {group['id']})")
```

## Add a Beta Tester

```python
tester_data = {
    "data": {
        "type": "betaTesters",
        "attributes": {
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "jane.doe@example.com"
        },
        "relationships": {
            "betaGroups": {
                "data": [{"type": "betaGroups", "id": GROUP_ID}]
            }
        }
    }
}
requests.post(
    "https://api.appstoreconnect.apple.com/v1/betaTesters",
    headers=headers, json=tester_data
)
```

## Add Existing Testers to a Group

```python
tester_ids = ["tester-id-1", "tester-id-2"]
requests.post(
    f"https://api.appstoreconnect.apple.com/v1/betaGroups/{GROUP_ID}/relationships/betaTesters",
    headers=headers,
    json={"data": [{"type": "betaTesters", "id": tid} for tid in tester_ids]}
)
```

## Remove Testers from a Group

```python
requests.delete(
    f"https://api.appstoreconnect.apple.com/v1/betaGroups/{GROUP_ID}/relationships/betaTesters",
    headers=headers,
    json={"data": [{"type": "betaTesters", "id": tid} for tid in tester_ids]}
)
```

## Assign Build to a Beta Group

```python
requests.post(
    f"https://api.appstoreconnect.apple.com/v1/betaGroups/{GROUP_ID}/relationships/builds",
    headers=headers,
    json={"data": [{"type": "builds", "id": BUILD_ID}]}
)
```

## Submit Build for Beta Review

Required for external testers (not needed for internal testers):

```python
submission_data = {
    "data": {
        "type": "betaAppReviewSubmissions",
        "relationships": {
            "build": {"data": {"type": "builds", "id": BUILD_ID}}
        }
    }
}
requests.post(
    "https://api.appstoreconnect.apple.com/v1/betaAppReviewSubmissions",
    headers=headers, json=submission_data
)
```

## Send TestFlight Invitation

```python
invite_data = {
    "data": {
        "type": "betaTesterInvitations",
        "relationships": {
            "betaTester": {"data": {"type": "betaTesters", "id": "tester-id"}}
        }
    }
}
requests.post(
    "https://api.appstoreconnect.apple.com/v1/betaTesterInvitations",
    headers=headers, json=invite_data
)
```

## Update Beta App Localization (TestFlight Description)

```python
response = requests.get(
    f"https://api.appstoreconnect.apple.com/v1/apps/{APP_ID}/betaAppLocalizations",
    headers=headers
)
BETA_LOC_ID = response.json()['data'][0]['id']

update_data = {
    "data": {
        "type": "betaAppLocalizations",
        "id": BETA_LOC_ID,
        "attributes": {
            "description": "Thanks for testing! This build includes...",
            "feedbackEmail": "support@yourcompany.com"
        }
    }
}
requests.patch(
    f"https://api.appstoreconnect.apple.com/v1/betaAppLocalizations/{BETA_LOC_ID}",
    headers=headers, json=update_data
)
```

## List All Beta Testers

```python
response = requests.get(
    "https://api.appstoreconnect.apple.com/v1/betaTesters",
    headers=headers,
    params={"filter[apps]": APP_ID, "limit": 100}
)
for tester in response.json()['data']:
    attrs = tester['attributes']
    print(f"{attrs.get('firstName', '')} {attrs.get('lastName', '')} - {attrs['email']}")
```
