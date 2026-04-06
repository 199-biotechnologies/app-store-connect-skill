# Screenshots & App Previews

## Screenshot Upload Workflow

### Step 1: Create Screenshot Set

Display types:
- `APP_IPHONE_67` — iPhone 6.7" (Pro Max) — 1320x2868 or 1290x2796
- `APP_IPHONE_65` — iPhone 6.5"
- `APP_IPHONE_61` — iPhone 6.1"
- `APP_IPHONE_55` — iPhone 5.5"
- `APP_IPAD_PRO_129` — iPad Pro 12.9" — 2048x2732
- `APP_APPLE_VISION_PRO` — Apple Vision Pro

```python
create_set_data = {
    "data": {
        "type": "appScreenshotSets",
        "attributes": {"screenshotDisplayType": "APP_IPHONE_67"},
        "relationships": {
            "appStoreVersionLocalization": {
                "data": {"type": "appStoreVersionLocalizations", "id": LOCALIZATION_ID}
            }
        }
    }
}
response = requests.post(
    "https://api.appstoreconnect.apple.com/v1/appScreenshotSets",
    headers=headers, json=create_set_data
)
SCREENSHOT_SET_ID = response.json()['data']['id']
```

### Step 2: Reserve, Upload, and Commit Each Screenshot

```python
import os, hashlib  # Additional imports required for screenshot upload

filepath = "/path/to/screenshot.png"
file_size = os.path.getsize(filepath)
with open(filepath, 'rb') as f:
    file_data = f.read()
    checksum = hashlib.md5(file_data).hexdigest()

# Reserve slot
reserve_data = {
    "data": {
        "type": "appScreenshots",
        "attributes": {"fileName": os.path.basename(filepath), "fileSize": file_size},
        "relationships": {
            "appScreenshotSet": {
                "data": {"type": "appScreenshotSets", "id": SCREENSHOT_SET_ID}
            }
        }
    }
}
response = requests.post(
    "https://api.appstoreconnect.apple.com/v1/appScreenshots",
    headers=headers, json=reserve_data
)
screenshot_data = response.json()['data']
screenshot_id = screenshot_data['id']
upload_ops = screenshot_data['attributes']['uploadOperations']

# Upload binary chunks
for op in upload_ops:
    op_headers = {h['name']: h['value'] for h in op.get('requestHeaders', [])}
    offset = op.get('offset', 0)
    length = op.get('length', file_size)
    requests.put(op['url'], headers=op_headers, data=file_data[offset:offset + length])

# Commit
commit_data = {
    "data": {
        "type": "appScreenshots", "id": screenshot_id,
        "attributes": {"uploaded": True, "sourceFileChecksum": checksum}
    }
}
requests.patch(
    f"https://api.appstoreconnect.apple.com/v1/appScreenshots/{screenshot_id}",
    headers=headers, json=commit_data
)
```

### Delete a Screenshot

```python
requests.delete(
    f"https://api.appstoreconnect.apple.com/v1/appScreenshots/{screenshot_id}",
    headers=headers
)
```

### Reorder Screenshots

```python
reorder_data = {
    "data": [
        {"type": "appScreenshots", "id": "screenshot-id-3"},
        {"type": "appScreenshots", "id": "screenshot-id-1"},
        {"type": "appScreenshots", "id": "screenshot-id-2"},
    ]
}
requests.patch(
    f"https://api.appstoreconnect.apple.com/v1/appScreenshotSets/{SCREENSHOT_SET_ID}/relationships/appScreenshots",
    headers=headers, json=reorder_data
)
```

## App Preview (Video) Upload

Same pattern as screenshots but with `appPreviewSets` and `appPreviews`:

```python
# Create preview set
preview_set_data = {
    "data": {
        "type": "appPreviewSets",
        "attributes": {"previewType": "APP_IPHONE_67"},
        "relationships": {
            "appStoreVersionLocalization": {
                "data": {"type": "appStoreVersionLocalizations", "id": LOCALIZATION_ID}
            }
        }
    }
}
response = requests.post(
    "https://api.appstoreconnect.apple.com/v1/appPreviewSets",
    headers=headers, json=preview_set_data
)
PREVIEW_SET_ID = response.json()['data']['id']

# Reserve, upload, commit (same flow as screenshots)
# Use type "appPreviews" and endpoint /v1/appPreviews
```

## Simulator Screenshots

```bash
# Boot simulator
xcrun simctl boot "iPhone 16 Pro Max"
open -a Simulator

# Build and install app
xcodebuild -project App.xcodeproj -scheme App \
    -destination 'platform=iOS Simulator,name=iPhone 16 Pro Max' \
    -derivedDataPath build build
xcrun simctl install booted "build/Build/Products/Debug-iphonesimulator/App Name.app"

# Launch app
xcrun simctl launch booted com.company.bundleid

# Take screenshot
xcrun simctl io booted screenshot ~/Pictures/screenshot.png
```

## Required Screenshot Sizes

| Device | Display Type | Resolution |
|--------|-------------|------------|
| iPhone 16 Pro Max | APP_IPHONE_67 | 1320 x 2868 |
| iPhone 15 Pro Max | APP_IPHONE_67 | 1290 x 2796 |
| iPhone 15 Plus | APP_IPHONE_67 | 1290 x 2796 |
| iPad Pro 12.9" | APP_IPAD_PRO_129 | 2048 x 2732 |

Minimum 2 screenshots per device type, maximum 10. App previews: 15-30 seconds, up to 3 per locale per device.
