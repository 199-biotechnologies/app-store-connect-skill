# In-App Purchases & Subscriptions

Create and manage IAPs, subscription groups, subscriptions, promotional offers, and pricing.

## Create a Non-Consumable In-App Purchase

```python
iap_data = {
    "data": {
        "type": "inAppPurchases",
        "attributes": {
            "name": "Remove Ads",
            "productId": "com.company.app.removeads",
            "inAppPurchaseType": "NON_CONSUMABLE",
            "reviewNote": "Removes all banner and interstitial ads"
        },
        "relationships": {
            "app": {"data": {"type": "apps", "id": APP_ID}}
        }
    }
}
response = requests.post(
    "https://api.appstoreconnect.apple.com/v2/inAppPurchases",
    headers=headers, json=iap_data
)
IAP_ID = response.json()['data']['id']
```

IAP types: `CONSUMABLE`, `NON_CONSUMABLE`, `NON_RENEWING_SUBSCRIPTION`.

## List All In-App Purchases

```python
response = requests.get(
    f"https://api.appstoreconnect.apple.com/v1/apps/{APP_ID}/inAppPurchasesV2",
    headers=headers
)
for iap in response.json()['data']:
    attrs = iap['attributes']
    print(f"{attrs['name']} ({attrs['productId']}) - {attrs['inAppPurchaseType']} - {attrs['state']}")
```

## Create a Subscription Group

```python
group_data = {
    "data": {
        "type": "subscriptionGroups",
        "attributes": {"referenceName": "Premium Plans"},
        "relationships": {
            "app": {"data": {"type": "apps", "id": APP_ID}}
        }
    }
}
response = requests.post(
    "https://api.appstoreconnect.apple.com/v1/subscriptionGroups",
    headers=headers, json=group_data
)
SUB_GROUP_ID = response.json()['data']['id']
```

## Create a Subscription

```python
sub_data = {
    "data": {
        "type": "subscriptions",
        "attributes": {
            "name": "Monthly Premium",
            "productId": "com.company.app.monthly",
            "subscriptionPeriod": "ONE_MONTH",
            "groupLevel": 1,
            "reviewNote": "Auto-renewable monthly subscription",
            "familySharable": True
        },
        "relationships": {
            "group": {"data": {"type": "subscriptionGroups", "id": SUB_GROUP_ID}}
        }
    }
}
response = requests.post(
    "https://api.appstoreconnect.apple.com/v1/subscriptions",
    headers=headers, json=sub_data
)
SUBSCRIPTION_ID = response.json()['data']['id']
```

Subscription periods: `ONE_WEEK`, `ONE_MONTH`, `TWO_MONTHS`, `THREE_MONTHS`, `SIX_MONTHS`, `ONE_YEAR`.

## Set Subscription Pricing

```python
# Get available price points
response = requests.get(
    f"https://api.appstoreconnect.apple.com/v1/subscriptions/{SUBSCRIPTION_ID}/pricePoints",
    headers=headers,
    params={"filter[territory]": "USA"}
)
PRICE_POINT_ID = response.json()['data'][0]['id']
```

## Promotional Offers

Win back lapsed subscribers:

```python
offer_data = {
    "data": {
        "type": "subscriptionPromotionalOffers",
        "attributes": {
            "name": "Winback30",
            "offerCode": "WINBACK30",
            "duration": "ONE_MONTH",
            "offerMode": "FREE_TRIAL",
            "numberOfPeriods": 1
        },
        "relationships": {
            "subscription": {"data": {"type": "subscriptions", "id": SUBSCRIPTION_ID}},
            "prices": {
                "data": [{"type": "subscriptionPromotionalOfferPrices", "id": "PLACEHOLDER_PRICE_ID"}]
            }
        }
    },
    "included": [{
        "type": "subscriptionPromotionalOfferPrices",
        "id": "PLACEHOLDER_PRICE_ID",
        "relationships": {
            "subscriptionPricePoint": {"data": {"type": "subscriptionPricePoints", "id": PRICE_POINT_ID}},
            "territory": {"data": {"type": "territories", "id": "USA"}}
        }
    }]
}
requests.post(
    "https://api.appstoreconnect.apple.com/v1/subscriptionPromotionalOffers",
    headers=headers, json=offer_data
)
```

Offer modes: `PAY_AS_YOU_GO`, `PAY_UP_FRONT`, `FREE_TRIAL`.
Durations: `ONE_DAY`, `THREE_DAYS`, `ONE_WEEK`, `TWO_WEEKS`, `ONE_MONTH`, `TWO_MONTHS`, `THREE_MONTHS`, `SIX_MONTHS`, `ONE_YEAR`.

## App Pricing & Availability

```python
# Set app pricing schedule
price_data = {
    "data": {
        "type": "appPriceSchedules",
        "relationships": {
            "app": {"data": {"type": "apps", "id": APP_ID}},
            "baseTerritory": {"data": {"type": "territories", "id": "USA"}},
            "manualPrices": {"data": [{"type": "appPrices", "id": "PLACEHOLDER_PRICE_ID"}]}
        }
    },
    "included": [{
        "type": "appPrices",
        "id": "PLACEHOLDER_PRICE_ID",
        "attributes": {"startDate": None},
        "relationships": {
            "appPricePoint": {"data": {"type": "appPricePoints", "id": "PRICE_POINT_ID"}}
        }
    }]
}
requests.post(
    "https://api.appstoreconnect.apple.com/v1/appPriceSchedules",
    headers=headers, json=price_data
)
```

## Update Territory Availability

First, get the territory availability IDs:

```python
response = requests.get(
    f"https://api.appstoreconnect.apple.com/v1/apps/{APP_ID}/appAvailability",
    headers=headers,
    params={"include": "availableTerritories"}
)
# Each included territory has an ID for patching
for territory in response.json().get('included', []):
    print(f"{territory['attributes']['currency']} - {territory['id']}")
TERRITORY_ID = "the-territory-id"
```

Then update:

```python
requests.patch(
    f"https://api.appstoreconnect.apple.com/v1/territoryAvailabilities/{TERRITORY_ID}",
    headers=headers,
    json={"data": {"type": "territoryAvailabilities", "id": TERRITORY_ID,
                    "attributes": {"available": True, "preOrderEnabled": False}}}
)
```
