# Yandex Direct API v5 - Comprehensive Research Report

## Executive Summary

This research provides a comprehensive analysis of the Yandex Direct API v5, documenting all available services, methods, parameters, and data structures. The API is Yandex's official interface for programmatically managing advertising campaigns across the Yandex.Direct platform.

---

## 1. API Endpoints & Configuration

### Base URLs
| Environment | URL |
|------------|-----|
| Production (v5) | `https://api.direct.yandex.com/json/v5` |
| Production (v501) | `https://api.direct.yandex.com/json/v501` |
| Sandbox | `https://api-sandbox.direct.yandex.com/json/v5` |

**Source:** `yandex_mcp/config.py`, [Yandex Direct API Official](https://yandex.com/dev/direct)

The v501 endpoint is required for **Unified Performance Campaigns (ЕПК)** and certain features like Shopping ads.

---

## 2. Authentication

### OAuth 2.0 Authentication
The API uses Bearer token authentication:

```http
Authorization: Bearer <access_token>
```

### Environment Variables
| Variable | Description |
|----------|-------------|
| `YANDEX_DIRECT_TOKEN` | Access token for Direct API |
| `YANDEX_METRIKA_TOKEN` | Access token for Metrika API |
| `YANDEX_TOKEN` | Unified token for both services |
| `YANDEX_CLIENT_LOGIN` | Agency client login (for managing sub-accounts) |
| `YANDEX_USE_SANDBOX` | Set to "true" to use sandbox environment |

**Source:** `yandex_mcp/client.py`

### Headers
- `Authorization`: Bearer token (required)
- `Client-Login`: Agency client login (required for agencies)
- `Accept-Language`: Language for error messages (ru/en)
- `Content-Type`: application/json

---

## 3. Available Services & Methods

The Yandex Direct API v5 provides **18 distinct services** for managing different aspects of advertising campaigns:

### 3.1 Campaigns Service
**Endpoint:** `https://api.direct.yandex.com/json/v5/campaigns`

| Method | Description |
|--------|-------------|
| `get` | Retrieve campaigns with filtering |
| `add` | Create new campaigns |
| `update` | Modify campaign settings |
| `delete` | Remove campaigns |
| `suspend` | Pause campaigns |
| `resume` | Activate paused campaigns |
| `archive` | Archive campaigns |
| `unarchive` | Restore archived campaigns |

**Campaign Types:**
- `TEXT_CAMPAIGN` - Standard text ads
- `DYNAMIC_TEXT_CAMPAIGN` - Dynamic text ads from feeds
- `MOBILE_APP_CAMPAIGN` - Mobile app promotion
- `CPM_BANNER_CAMPAIGN` - Display/banner campaigns
- `SMART_CAMPAIGN` - Smart banners (automated)
- `UNIFIED_CAMPAIGN` - Unified Performance Campaign (ЕПК)

**Bidding Strategies:**
- `WB_MAXIMUM_CLICKS` - Maximize clicks
- `WB_MAXIMUM_CONVERSION_RATE` - Maximize conversions
- `AVERAGE_CPC` - Average CPC
- `AVERAGE_CPA` - Average CPA
- `AVERAGE_ROI` - ROI-based bidding
- `PAY_FOR_CONVERSION` - Pay per conversion

**Source:** `yandex_mcp/tools/direct/campaigns.py`, [Yandex Campaigns API](https://tech.yandex.com/direct/doc/ref-v5/campaigns/campaigns-docpage/)

---

### 3.2 AdGroups Service
**Endpoint:** `https://api.direct.yandex.com/json/v5/adgroups`

| Method | Description |
|--------|-------------|
| `get` | Retrieve ad groups |
| `add` | Create new ad groups |
| `update` | Modify ad groups |
| `delete` | Remove ad groups |

**Parameters:**
- `campaign_id` (required) - Parent campaign
- `name` - Ad group name (max 255 chars)
- `region_ids` - Geographic targeting (list of region IDs)
- `negative_keywords` - Group-level negative keywords
- `feed_id` - Feed ID for dynamic/smart ad groups

**Group Types:**
- Standard AdGroup
- DynamicTextAdGroup (for DYNAMIC_TEXT_CAMPAIGN)
- SmartAdGroup (for SMART_CAMPAIGN)
- UnifiedAdGroup (for UNIFIED_CAMPAIGN) - requires v501

**Source:** `yandex_mcp/tools/direct/adgroups.py`

---

### 3.3 Ads Service
**Endpoint:** `https://api.direct.yandex.com/json/v5/ads`

| Method | Description |
|--------|-------------|
| `get` | Retrieve ads |
| `add` | Create new ads |
| `update` | Modify ads |
| `delete` | Remove ads |
| `moderate` | Submit for moderation |
| `suspend` | Pause ads |
| `resume` | Activate ads |
| `archive` | Archive ads |
| `unarchive` | Restore ads |

**Ad Types:**
- `TextAd` - Standard text ads
- `TextImageAd` - Image/banner ads
- `DynamicTextAd` - Dynamic text ads
- `ShoppingAd` - Product ads (requires v501)
- `CPM_BANNER_AD` - Display banner ads

**Parameters:**
- `adgroup_id` - Parent ad group
- `title` - Ad title (max 56 chars, 30 for title2)
- `text` - Ad body text (max 81 chars)
- `href` - Landing page URL
- `mobile` - Mobile-specific ad (YES/NO)
- `ad_image_hash` - Image hash for image ads

**Source:** `yandex_mcp/tools/direct/ads.py`

---

### 3.4 Keywords Service
**Endpoint:** `https://api.direct.yandex.com/json/v5/keywords`

| Method | Description |
|--------|-------------|
| `get` | Retrieve keywords |
| `add` | Create new keywords |
| `update` | Modify keywords |
| `delete` | Remove keywords |
| `suspend` | Pause keywords |
| `resume` | Activate keywords |

**Parameters:**
- `adgroup_id` - Parent ad group
- `keyword` - Keyword text (max 4096 chars)
- `bid` - Search bid (in micros)
- `context_bid` - Network bid (in micros)

**Source:** `yandex_mcp/tools/direct/keywords.py`

---

### 3.5 KeywordBids Service
**Endpoint:** `https://api.direct.yandex.com/json/v5/keywordbids`

| Method | Description |
|--------|-------------|
| `get` | Retrieve current bids |
| `set` | Update keyword bids |

**Parameters:**
- `keyword_id` - Keyword identifier
- `search_bid` - Bid for search results
- `network_bid` - Bid for display network

**Source:** `yandex_mcp/tools/direct/keywords.py`

---

### 3.6 BidModifiers Service
**Endpoint:** `https://api.direct.yandex.com/json/v5/bidmodifiers`

| Method | Description |
|--------|-------------|
| `get` | Retrieve bid modifiers |
| `add` | Create bid modifiers |
| `set` | Update modifier values |
| `delete` | Remove modifiers |
| `toggle` | Enable/disable modifiers |

**Modifier Types:**
- `MobileAdjustment` - Mobile device (0-1300%)
- `DesktopAdjustment` - Desktop (0-1300%)
- `DemographicsAdjustment` - Age/gender targeting
- `RegionalAdjustment` - Geographic adjustments

**Note:** The `Levels` parameter is REQUIRED for get requests (CAMPAIGN or AD_GROUP).

**Source:** `yandex_mcp/tools/direct/bidmodifiers.py`

---

### 3.7 Sitelinks Service
**Endpoint:** `https://api.direct.yandex.com/json/v5/sitelinks`

| Method | Description |
|--------|-------------|
| `get` | Retrieve sitelink sets |
| `add` | Create sitelink sets |
| `delete` | Remove sitelink sets |

**Parameters:**
- `title` - Sitelink title (max 30 chars)
- `href` - Sitelink URL
- `description` - Optional description (max 60 chars)

**Limits:** Max 8 sitelinks per set, max 66 chars total for titles 1-4 and 5-8.

**Source:** `yandex_mcp/tools/direct/sitelinks.py`

---

### 3.8 VCards Service
**Endpoint:** `https://api.direct.yandex.com/json/v5/vcards`

| Method | Description |
|--------|-------------|
| `get` | Retrieve vCards |
| `add` | Create vCards |
| `delete` | Remove vCards |

**Parameters:**
- `campaign_id` - Campaign ID
- `company` - Company name
- `phone` - Phone number object (country_code, city_code, phone_number)
- `country`, `city`, `street`, `house` - Address
- `work_time` - Working hours format: `0#3#10#00#18#00`
- `extra_message` - Additional info (max 200 chars)

**Source:** `yandex_mcp/tools/direct/vcards.py`

---

### 3.9 AdExtensions Service
**Endpoint:** `https://api.direct.yandex.com/json/v5/adextensions`

| Method | Description |
|--------|-------------|
| `get` | Retrieve extensions |
| `add` | Create callout extensions |
| `delete` | Remove extensions |

**Extension Types:**
- `CALLOUT` - Text callouts

**Parameters:**
- `callout_text` - Callout text (max 25 chars each)
- Max 50 callouts per account
- Max 25 callouts per ad

**Source:** `yandex_mcp/tools/direct/adextensions.py`

---

### 3.10 Images Service (AdImages)
**Endpoint:** `https://api.direct.yandex.com/json/v5/adimages`

| Method | Description |
|--------|-------------|
| `get` | Retrieve images |
| `add` | Upload new images |
| `delete` | Remove images |

**Parameters:**
- `image_data` - Base64-encoded image
- `name` - Image name
- `type` - Image type (REGULAR or WIDE)

**Requirements:**
- Formats: JPEG, GIF, PNG
- REGULAR: Min 450x450px
- WIDE: Min 1080x607px

**Source:** `yandex_mcp/tools/direct/images.py`

---

### 3.11 Videos Service (AdVideos)
**Endpoint:** `https://api.direct.yandex.com/json/v5/advideos`

| Method | Description |
|--------|-------------|
| `get` | Retrieve videos |
| `add` | Upload new videos |

**Parameters:**
- `video_data` - Base64-encoded video
- `name` - Video name

**Requirements:**
- Formats: MP4, WebM, MOV, QT, FLV, AVI
- Max size: 100 MB
- Duration: 5-60 seconds
- Statuses: NEW → CONVERTING → READY → ERROR

**Source:** `yandex_mcp/tools/direct/advideos.py`

---

### 3.12 Creatives Service
**Endpoint:** `https://api.direct.yandex.com/json/v5/creatives`

| Method | Description |
|--------|-------------|
| `get` | Retrieve creatives |
| `add` | Create video creatives |

**Creative Types:**
- `VIDEO_EXTENSION_CREATIVE` - Video extension
- `CPC_VIDEO_CREATIVE` - Video for CPC campaigns
- `CPM_VIDEO_CREATIVE` - Video for CPM campaigns

**Source:** `yandex_mcp/tools/direct/creatives.py`

---

### 3.13 Feeds Service
**Endpoint:** `https://api.direct.yandex.com/json/v5/feeds`

| Method | Description |
|--------|-------------|
| `get` | Retrieve feeds |
| `add` | Create feeds |
| `update` | Modify feeds |
| `delete` | Remove feeds |

**Business Types:**
- `RETAIL` - E-commerce/retail
- `HOTELS` - Hotel booking
- `REALTY` - Real estate
- `AUTOMOBILES` - Auto listings
- `FLIGHTS` - Flight search
- `OTHER` - Other products

**Parameters:**
- `name` - Feed name
- `business_type` - Business category
- `url` - Feed URL (YML/CSV)
- `login`, `password` - HTTP Basic Auth credentials

**Limits:** Max 50 feeds per advertiser.

**Source:** `yandex_mcp/tools/direct/feeds.py`

---

### 3.14 RetargetingLists Service
**Endpoint:** `https://api.direct.yandex.com/json/v5/retargetinglists`

| Method | Description |
|--------|-------------|
| `get` | Retrieve retargeting lists |
| `add` | Create retargeting lists |
| `update` | Modify lists |
| `delete` | Remove lists |

**Parameters:**
- `name` - List name
- `rules` - Array of rule groups (OR between groups, AND within)
- `goal_id` - Metrika goal ID
- `member_of` - POSITIVE or NEGATIVE
- `days` - Lookback period (1-540 days)

**Source:** `yandex_mcp/tools/direct/retargeting.py`

---

### 3.15 AudienceTargets Service
**Endpoint:** `https://api.direct.yandex.com/json/v5/audiencetargets`

| Method | Description |
|--------|-------------|
| `get` | Retrieve audience targets |
| `add` | Create audience targets |
| `suspend` | Pause targets |
| `resume` | Activate targets |
| `delete` | Remove targets |

**Parameters:**
- `adgroup_id` - Ad group ID
- `retargeting_list_id` - Retargeting list ID
- `interest_id` - Interest category ID
- `context_bid` - Bid for context networks

**Source:** `yandex_mcp/tools/direct/retargeting.py`

---

### 3.16 SmartAdTargets Service
**Endpoint:** `https://api.direct.yandex.com/json/v5/smartadtargets`

| Method | Description |
|--------|-------------|
| `get` | Retrieve smart ad targets |
| `add` | Create smart ad targets |
| `suspend` | Pause targets |
| `resume` | Activate targets |
| `delete` | Remove targets |

**Parameters:**
- `adgroup_id` - Smart ad group ID
- `name` - Filter name
- `available_items_only` - Show only available items
- `conditions` - Filter conditions

**Condition Operators:**
- `EQUALS_ANY`, `CONTAINS_ANY`, `NOT_CONTAINS_ALL`
- `GREATER_THAN`, `LESS_THAN`
- `IN_RANGE`, `EXISTS`

**Source:** `yandex_mcp/tools/direct/smartadtargets.py`

---

### 3.17 NegativeKeywordSharedSets Service
**Endpoint:** `https://api.direct.yandex.com/json/v5/negativekeywordsharedsets`

| Method | Description |
|--------|-------------|
| `get` | Retrieve shared sets |
| `add` | Create shared sets |
| `update` | Modify sets |
| `delete` | Remove sets |

**Limits:**
- Max 20 shared sets per account
- Max 5000 keywords per set

**Source:** `yandex_mcp/tools/direct/negative_keywords_shared.py`

---

### 3.18 Dictionaries Service
**Endpoint:** `https://api.direct.yandex.com/json/v5/dictionaries`

| Method | Description |
|--------|-------------|
| `get` | Retrieve dictionary data |

**Available Dictionaries:**
- `GeoRegions` - Geographic regions for targeting
- `Currencies` - Currency information
- `TimeZones` - Time zones
- `Constants` - API constants and limits
- `AdCategories` - Ad categories
- `OperationSystemVersions` - OS versions for mobile
- `SupplySidePlatforms` - SSP platforms for RTB
- `Interests` - Interest categories
- `AudienceCriteriaTypes` - Audience criteria types

**Source:** `yandex_mcp/tools/direct/dictionaries.py`

---

### 3.19 Clients Service
**Endpoint:** `https://api.direct.yandex.com/json/v5/clients`

| Method | Description |
|--------|-------------|
| `get` | Retrieve client account info |

**Returns:**
- Account settings, currency, country
- Grants (permissions)
- Restrictions (campaigns per account, etc.)
- Representative logins

**Source:** `yandex_mcp/tools/direct/clients.py`

---

### 3.20 Changes Service
**Endpoint:** `https://api.direct.yandex.com/json/v5/changes`

| Method | Description |
|--------|-------------|
| `checkCampaigns` | Check campaign changes |
| `check` | Check all entity changes |

**Use Case:** Incremental synchronization - fetch only entities that changed since a timestamp.

**Source:** `yandex_mcp/tools/direct/clients.py`

---

### 3.21 Reports Service
**Endpoint:** `https://api.direct.yandex.com/json/v5/reports`

| Method | Description |
|--------|-------------|
| `get` (POST) | Generate and retrieve reports |

**Report Types:**
- `ACCOUNT_PERFORMANCE_REPORT` - Account-level stats
- `CAMPAIGN_PERFORMANCE_REPORT` - Campaign stats
- `AD_PERFORMANCE_REPORT` - Ad-level stats
- `ADGROUP_PERFORMANCE_REPORT` - Ad group stats
- `CRITERIA_PERFORMANCE_REPORT` - Keyword stats
- `SEARCH_QUERY_PERFORMANCE_REPORT` - Search query data

**Common Fields:**
- `Impressions`, `Clicks`, `Cost`
- `Ctr`, `AvgCpc`, `ConversionRate`
- `CampaignName`, `CampaignId`, `Date`

**Note:** Reports are generated asynchronously; may require polling with retry codes 201/202.

**Source:** `yandex_mcp/tools/direct/stats.py`

---

## 4. API Limits & Restrictions

### Request Limits
| Operation | Limit |
|-----------|-------|
| Campaigns per add/update request | Max 10 |
| Ad groups per request | Varies |
| Keywords per request | Max 200 |
| Ads per request | Varies |
| Pagination limit | Max 10,000 per request |

### Account Restrictions
Retrieved via `Clients.get`:
- `CAMPAIGNS_TOTAL_PER_CLIENT` - Total campaigns allowed
- `CAMPAIGNS_UNARCHIVED_PER_CLIENT` - Active campaigns limit
- `ADGROUPS_TOTAL_PER_CAMPAIGN` - Groups per campaign limit

### Rate Limiting
- Standard timeout: 30 seconds
- Report generation timeout: 120 seconds
- Video upload timeout: 300 seconds (5 minutes)

**Source:** `yandex_mcp/config.py`, [Yandex Direct API](https://yandex.com/dev/direct)

---

## 5. Data Structures & Models

### Common Enums
```python
CampaignState: ON, OFF, SUSPENDED, ENDED, CONVERTED, ARCHIVED
CampaignStatus: ACCEPTED, DRAFT, MODERATION, REJECTED
CampaignType: TEXT_CAMPAIGN, DYNAMIC_TEXT_CAMPAIGN, MOBILE_APP_CAMPAIGN, 
              CPM_BANNER_CAMPAIGN, SMART_CAMPAIGN, UNIFIED_CAMPAIGN
AdState: ON, OFF, OFF_BY_MONITORING, SUSPENDED, ARCHIVED
AdStatus: ACCEPTED, DRAFT, MODERATION, PREACCEPTED, REJECTED
DailyBudgetMode: STANDARD, DISTRIBUTED
```

### Bidding Strategy Types
```python
Search: HIGHEST_POSITION, WB_MAXIMUM_CLICKS, WB_MAXIMUM_CONVERSION_RATE,
        AVERAGE_CPC, AVERAGE_CPA, AVERAGE_ROI, WEEKLY_CLICK_PACKAGE,
        PAY_FOR_CONVERSION, PAY_FOR_CONVERSION_CRR, SERVING_OFF

Network: SERVING_OFF WB_MAXIMUM_CL, NETWORK_DEFAULT,ICKS, AVERAGE_CPC,
         WB_MAXIMUM_CONVERSION_RATE, AVERAGE_CPC_PER_CAMPAIGN,
         AVERAGE_CPC_PER_FILTER, AVERAGE_CPA_PER_CAMPAIGN,
         AVERAGE_CPA_PER_FILTER
```

**Source:** `yandex_mcp/models/direct.py`

---

## 6. Special Features

### Unified Performance Campaign (ЕПК)
- Requires v501 API endpoint
- Supports Shopping ads
- Uses UnifiedAdGroup structure
- Attribution model: LYDC (last click + day)

### Change Tracking
- Use `Changes.check` for incremental sync
- Store server timestamp between requests
- Returns modified entity IDs for campaigns, ad groups, ads, keywords

### Sandbox Environment
- Test API calls without affecting production
- Set `YANDEX_USE_SANDBOX=true`
- URL: `https://api-sandbox.direct.yandex.com/json/v5`

---

## 7. Confidence Assessment

| Category | Confidence |
|----------|------------|
| Core services (Campaigns, Ads, AdGroups, Keywords) | **High** - Verified against official docs and implementation |
| Extended services (BidModifiers, Retargeting) | **High** - Verified against implementation |
| Dictionaries and Clients | **High** - Verified |
| Reports API | **High** - Verified |
| API limits and restrictions | **Medium** - Based on implementation and docs |

---

## 8. Gaps & Future Research

### Not Covered in Current Implementation:
- **AgencyClients** service (for agencies managing multiple clients)
- **LeadForms** service (lead generation forms)
- **TurboPages** service (Yandex Turbo page management)
- **DynamicTextAdTargets** service (dynamic targeting)
- **VideoAds** service (video ad management)

### Areas Requiring Further Investigation:
- Error code definitions and handling strategies
- Webhook/notifications for campaign status changes
- Programmatic advertising use cases

---

## 9. References

1. [Yandex Direct API Official Documentation](https://yandex.com/dev/direct)
2. [Yandex Direct API Reference](https://tech.yandex.com/direct/doc/ref-v5/)
3. [API Start Guide](https://yandex.com/dev/direct/doc/start/get)
4. [Campaign Management](https://yandex.com/dev/direct/doc/dg/objects/campaign.html)
5. Implementation source code: `yandex_mcp/`

---

*Report generated based on analysis of official Yandex Direct API v5 documentation and examination of the yandex-mcp project implementation.*
