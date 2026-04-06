# Build & Deploy

All operations require AUTH credentials from `config/credentials.local.md` (Key ID, Issuer ID, key path, Team ID).

Archive, sign, and upload builds to App Store Connect via xcodebuild CLI.

## Archive

```bash
# For .xcodeproj
xcodebuild -project AppName.xcodeproj -scheme AppName \
    -configuration Release \
    -archivePath /tmp/AppName.xcarchive \
    -destination 'generic/platform=iOS' \
    archive

# For .xcworkspace (CocoaPods, etc.)
xcodebuild -workspace AppName.xcworkspace -scheme AppName \
    -configuration Release \
    -archivePath /tmp/AppName.xcarchive \
    -destination 'generic/platform=iOS' \
    archive
```

## Export Options Plist

Create `/tmp/ExportOptions.plist` (adjust teamID per your account):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store-connect</string>
    <key>destination</key>
    <string>upload</string>
    <key>teamID</key>
    <string>TEAM_ID_HERE</string><!-- See config/credentials.local.md -->
    <key>signingStyle</key>
    <string>automatic</string>
    <key>manageAppVersionAndBuildNumber</key>
    <true/>
</dict>
</plist>
```

## Export and Upload

Use API key authentication for non-interactive (CI/CD) uploads. Provide the key path, key ID, and issuer ID from the credentials config:

```bash
xcodebuild -exportArchive \
    -archivePath /tmp/AppName.xcarchive \
    -exportOptionsPlist /tmp/ExportOptions.plist \
    -exportPath /tmp/AppExport \
    -allowProvisioningUpdates \
    -authenticationKeyPath PATH_TO_P8_KEY \   # See config/credentials.local.md
    -authenticationKeyID KEY_ID \             # See config/credentials.local.md
    -authenticationKeyIssuerID ISSUER_ID      # See config/credentials.local.md
```

## One-Line Build + Upload

```bash
xcodebuild -project AppName.xcodeproj -scheme AppName -configuration Release \
    -archivePath /tmp/AppName.xcarchive -destination 'generic/platform=iOS' archive && \
xcodebuild -exportArchive -archivePath /tmp/AppName.xcarchive \
    -exportOptionsPlist /tmp/ExportOptions.plist -exportPath /tmp/AppExport \
    -allowProvisioningUpdates \
    -authenticationKeyPath PATH_TO_P8_KEY \   # See config/credentials.local.md
    -authenticationKeyID KEY_ID \             # See config/credentials.local.md
    -authenticationKeyIssuerID ISSUER_ID      # See config/credentials.local.md
```

## Common Build Errors

| Error | Solution |
|-------|----------|
| `No profiles for 'bundle.id' were found` | Use API key auth flags |
| `The certificate has expired` | Renew in Apple Developer portal |
| `Provisioning profile doesn't include signing certificate` | Use `signingStyle: automatic` |
| `App Store Connect Operation Error` | Check bundle ID matches registered app |
| `exportArchive requires -archivePath` | Ensure archive step completed successfully |
