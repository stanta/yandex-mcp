# Yandex Direct API v5/v501 Gap Analysis

**Document Version:** 1.0  
**Date:** 2026-02-28  
**Analysis Target:** Yandex Direct MCP Implementation

---

## 1. Executive Summary

This document provides a comprehensive gap analysis between the Yandex Direct API v5/v501 specification and the current MCP implementation. The analysis identifies missing services, incomplete implementations, and areas requiring enhancement to achieve full API coverage.

### Current Coverage Overview

| Category | Count |
|----------|-------|
| Implemented Service Surfaces | 19 |
| Missing Services | 5 |
| Services with Partial Implementation | 9 |

### Key Findings

The project implements 19 Yandex Direct API service surfaces covering campaign management, ad operations, targeting, reporting, and change tracking. However, several critical gaps remain:

- **5 services entirely missing** from the implementation
- **9 existing services have incomplete method or feature coverage**
- **Model definitions lack some API v5 fields**
- **API version handling requires refinement for certain features**

### Accuracy Corrections Applied in This Revision

- Service classification was corrected in the implementation table: [AdGroups](yandex_mcp/tools/direct/adgroups.py:17) and [Feeds](yandex_mcp/tools/direct/feeds.py:53) are now marked partial.
- Standalone `SmartCampaigns` service row was removed and relabeled as a campaign subtype implemented under [Campaigns](yandex_mcp/tools/direct/campaigns.py:345).
- Broad line references were replaced with method-level references for auditability.
- Priority normalization now treats [AVERAGE_CPA](yandex_mcp/models/direct.py:72), [AVERAGE_ROI](yandex_mcp/models/direct.py:73), and [PAY_FOR_CONVERSION](yandex_mcp/models/direct.py:75) consistently.
- Coverage now includes dedicated parity treatment for `Changes`, `Reports`, and `KeywordBids` surfaces.

---

## 2. Implemented Services and Service Surfaces

The following table lists currently implemented API service surfaces with status and key methods:

| # | Service | File Path | Status | Key Methods Implemented |
|---|---------|-----------|--------|------------------------|
| 1 | Campaigns | `yandex_mcp/tools/direct/campaigns.py` | ⚠️ Partial | get, create, update, suspend, resume, archive, unarchive, delete |
| 2 | AdGroups | `yandex_mcp/tools/direct/adgroups.py` | ⚠️ Partial | get, create, update |
| 3 | Ads | `yandex_mcp/tools/direct/ads.py` | ✅ Complete | get, create, update, moderate, suspend, resume, archive, unarchive, delete |
| 4 | Keywords | `yandex_mcp/tools/direct/keywords.py` | ✅ Complete | get, add, set bids, suspend, resume, archive, unarchive, delete |
| 5 | BidModifiers | `yandex_mcp/tools/direct/bidmodifiers.py` | ⚠️ Partial | get, add, set, delete, toggle |
| 6 | Sitelinks | `yandex_mcp/tools/direct/sitelinks.py` | ✅ Complete | get, add, delete |
| 7 | VCards | `yandex_mcp/tools/direct/vcards.py` | ✅ Complete | get, add, delete |
| 8 | AdExtensions | `yandex_mcp/tools/direct/adextensions.py` | ⚠️ Partial | get, add callouts, link to ad |
| 9 | Images | `yandex_mcp/tools/direct/images.py` | ⚠️ Partial | upload, get, delete |
| 10 | AdVideos | `yandex_mcp/tools/direct/advideos.py` | ⚠️ Partial | upload, get status |
| 11 | Creatives | `yandex_mcp/tools/direct/creatives.py` | ⚠️ Partial | create video creative, get |
| 12 | Feeds | `yandex_mcp/tools/direct/feeds.py` | ⚠️ Partial | get, add, update, delete |
| 13 | Retargeting | `yandex_mcp/tools/direct/retargeting.py` | ✅ Complete | get lists, add, update, delete; get targets, add, suspend, resume, delete |
| 14 | SmartAdTargets | `yandex_mcp/tools/direct/smartadtargets.py` | ✅ Complete | get, add, suspend, resume, delete |
| 15 | NegativeKeywordsShared | `yandex_mcp/tools/direct/negative_keywords_shared.py` | ✅ Complete | get, add, update, delete |
| 16 | Dictionaries | `yandex_mcp/tools/direct/dictionaries.py` | ✅ Complete | get, get regions, get interests |
| 17 | Clients | `yandex_mcp/tools/direct/clients.py` | ✅ Complete | get client info |
| 18 | Changes | `yandex_mcp/tools/direct/clients.py` | ✅ Complete | checkCampaigns, check |
| 19 | Reports | `yandex_mcp/tools/direct/stats.py` | ✅ Complete | report generation with async polling |

`SmartCampaign` is a campaign subtype implemented in [direct_create_campaign()](yandex_mcp/tools/direct/campaigns.py:237), not a standalone API service.

### Service Registration

All services are registered in [register_direct_tools()](yandex_mcp/tools/direct/__init__.py:6).

---

## 3. Missing Services

Five Yandex Direct API services are not yet implemented in the MCP:

### 3.1 AgencyClients Service

| Attribute | Value |
|-----------|-------|
| **Priority** | Medium |
| **File to Create** | `yandex_mcp/tools/direct/agency_clients.py` |
| **Required Methods** | get, update |
| **Use Cases** | Managing client accounts for advertising agencies; retrieving sub-account list; updating client settings |

**API Reference:** `https://api.direct.yandex.com/json/v5/agencyclients`

```python
# Required functionality
- Get agency client accounts list
- Update client account settings
- Handle agency-specific authentication (Client-Login header)
```

---

### 3.2 LeadForms Service

| Attribute | Value |
|-----------|-------|
| **Priority** | High |
| **File to Create** | `yandex_mcp/tools/direct/lead_forms.py` |
| **Required Methods** | get, add, update, delete, get_leads |
| **Use Cases** | Lead generation form management; retrieving form submissions |

**API Reference:** `https://api.direct.yandex.com/json/v5/leadforms`

```python
# Required functionality
- Get lead forms (filter by campaign/ad group)
- Create lead form with questions and policy agreement
- Update existing lead form
- Delete lead form
- Get leads/submissions from forms
```

---

### 3.3 TurboPages Service

| Attribute | Value |
|-----------|-------|
| **Priority** | Low |
| **File to Create** | `yandex_mcp/tools/direct/turbopages.py` |
| **Required Methods** | get, add, update, delete |
| **Use Cases** | Yandex Turbo page management; creating fast-loading mobile pages |

**API Reference:** `https://api.direct.yandex.com/json/v5/turbopages`

```python
# Required functionality
- Get turbo page configurations
- Create turbo page with layout settings
- Update turbo page content and settings
- Delete turbo page
```

---

### 3.4 DynamicTextAdTargets Service

| Attribute | Value |
|-----------|-------|
| **Priority** | High |
| **File to Create** | `yandex_mcp/tools/direct/dynamic_text_ad_targets.py` |
| **Required Methods** | get, add, update, suspend, resume, delete |
| **Use Cases** | Dynamic text ad targeting; autotargeting categories management; product feed filters |

**API Reference:** `https://api.direct.yandex.com/json/v5/dynamictextadtargets`

```python
# Required functionality
- Get dynamic ad targets (filter by campaign/ad group)
- Create dynamic target with feed conditions
- Update target settings and conditions
- Suspend/resume targeting
- Delete dynamic target
```

---

### 3.5 VideoAds Service

| Attribute | Value |
|-----------|-------|
| **Priority** | Medium |
| **File to Create** | `yandex_mcp/tools/direct/video_ads.py` |
| **Required Methods** | get, add, update, delete |
| **Use Cases** | Video ad management (distinct from video extensions); video campaign ad management |

**API Reference:** `https://api.direct.yandex.com/json/v5/videoads`

```python
# Required functionality
- Get video ads (filter by campaign)
- Create video ad with creative
- Update video ad settings
- Delete video ad
```

---

## 4. Gaps in Existing Implementations

### 4.1 Campaigns Service

**File:** `yandex_mcp/tools/direct/campaigns.py`

| Missing Method/Feature | Priority | Line Reference | Notes |
|------------------------|----------|----------------|-------|
| MOBILE_APP_CAMPAIGN creation | Low | `direct_create_campaign()` [237](yandex_mcp/tools/direct/campaigns.py:237), type branches [295](yandex_mcp/tools/direct/campaigns.py:295)-[413](yandex_mcp/tools/direct/campaigns.py:413) | `MOBILE_APP_CAMPAIGN` enum exists but no creation branch |
| AVERAGE_CPA strategy wiring | High | Strategy update block [165](yandex_mcp/tools/direct/campaigns.py:165)-[203](yandex_mcp/tools/direct/campaigns.py:203), create strategy block [261](yandex_mcp/tools/direct/campaigns.py:261)-[293](yandex_mcp/tools/direct/campaigns.py:293) | Enum exists, missing full handling in create/update |
| AVERAGE_ROI strategy wiring | High | Strategy update block [165](yandex_mcp/tools/direct/campaigns.py:165)-[203](yandex_mcp/tools/direct/campaigns.py:203), create strategy block [261](yandex_mcp/tools/direct/campaigns.py:261)-[293](yandex_mcp/tools/direct/campaigns.py:293) | Missing in create/update strategy mapping |
| PAY_FOR_CONVERSION, PAY_FOR_CONVERSION_CRR | High | Strategy update block [165](yandex_mcp/tools/direct/campaigns.py:165)-[203](yandex_mcp/tools/direct/campaigns.py:203), create strategy block [261](yandex_mcp/tools/direct/campaigns.py:261)-[293](yandex_mcp/tools/direct/campaigns.py:293) | Missing conversion strategy handling |
| Attribution model update controls | Medium | [direct_update_campaign()](yandex_mcp/tools/direct/campaigns.py:96) | No explicit attribution update input mapping |
| WalletId field in get | Medium | `FieldNames` in [direct_get_campaigns()](yandex_mcp/tools/direct/campaigns.py:53) | Not requested in campaign retrieval |

**Gap Details:**
- [CampaignType.MOBILE_APP_CAMPAIGN](yandex_mcp/models/direct.py:38) exists but is not handled in [direct_create_campaign()](yandex_mcp/tools/direct/campaigns.py:237).
- Strategy handling covers `WB_MAXIMUM_CLICKS`, `AVERAGE_CPC`, `WB_MAXIMUM_CONVERSION_RATE` but undercovers `AVERAGE_CPA`, `AVERAGE_ROI`, `PAY_FOR_CONVERSION`, `PAY_FOR_CONVERSION_CRR`.

---

### 4.2 AdGroups Service

**File:** `yandex_mcp/tools/direct/adgroups.py`

| Missing Method | Priority | Line Reference | Notes |
|----------------|----------|----------------|-------|
| suspend | Medium | tool registrations [20](yandex_mcp/tools/direct/adgroups.py:20), [63](yandex_mcp/tools/direct/adgroups.py:63), [136](yandex_mcp/tools/direct/adgroups.py:136) | No manage-tool registration for adgroups |
| resume | Medium | tool registrations [20](yandex_mcp/tools/direct/adgroups.py:20), [63](yandex_mcp/tools/direct/adgroups.py:63), [136](yandex_mcp/tools/direct/adgroups.py:136) | No manage-tool registration for adgroups |
| archive | Medium | tool registrations [20](yandex_mcp/tools/direct/adgroups.py:20), [63](yandex_mcp/tools/direct/adgroups.py:63), [136](yandex_mcp/tools/direct/adgroups.py:136) | No manage-tool registration for adgroups |
| unarchive | Medium | tool registrations [20](yandex_mcp/tools/direct/adgroups.py:20), [63](yandex_mcp/tools/direct/adgroups.py:63), [136](yandex_mcp/tools/direct/adgroups.py:136) | No manage-tool registration for adgroups |

**Recommendation:** Use helper pattern from [register_manage_tool()](yandex_mcp/tools/direct/_helpers.py:124) following [campaign registration loop](yandex_mcp/tools/direct/campaigns.py:76).

---

### 4.3 Keywords Service

**File:** `yandex_mcp/tools/direct/keywords.py`

| Missing Method | Priority | Line Reference | Notes |
|----------------|----------|----------------|-------|
| archive | Low | manage loop [156](yandex_mcp/tools/direct/keywords.py:156)-[164](yandex_mcp/tools/direct/keywords.py:164) | Only suspend/resume/delete registered |
| unarchive | Low | manage loop [156](yandex_mcp/tools/direct/keywords.py:156)-[164](yandex_mcp/tools/direct/keywords.py:164) | Only suspend/resume/delete registered |
| QualityScore field | Low | `FieldNames` in [direct_get_keywords()](yandex_mcp/tools/direct/keywords.py:49) | Not requested in get |
| MarketScore field | Low | `FieldNames` in [direct_get_keywords()](yandex_mcp/tools/direct/keywords.py:49) | Not requested in get |

---

### 4.4 BidModifiers Service

**File:** `yandex_mcp/tools/direct/bidmodifiers.py`

| Missing Type | Priority | Model Reference | Notes |
|--------------|----------|-----------------|-------|
| VideoAdjustments | Medium | request fields [63](yandex_mcp/tools/direct/bidmodifiers.py:63)-[71](yandex_mcp/tools/direct/bidmodifiers.py:71), add mapping [135](yandex_mcp/tools/direct/bidmodifiers.py:135)-[159](yandex_mcp/tools/direct/bidmodifiers.py:159) | Video adjustments not wired |
| RetargetingAdjustments | High | request fields [63](yandex_mcp/tools/direct/bidmodifiers.py:63)-[71](yandex_mcp/tools/direct/bidmodifiers.py:71), add mapping [135](yandex_mcp/tools/direct/bidmodifiers.py:135)-[159](yandex_mcp/tools/direct/bidmodifiers.py:159) | Retargeting adjustments not wired |

**Current Implementation:**
```python
# Already implemented
MobileAdjustmentFieldNames
DesktopAdjustmentAdjustmentFieldNames
DemographicsAdjustmentFieldNames
RegionalAdjustmentFieldNames

# Missing
VideoAdjustmentFieldNames  # Not implemented
RetargetingAdjustmentFieldNames  # Not implemented
```

---

### 4.5 AdExtensions Service

**File:** `yandex_mcp/tools/direct/adextensions.py`

| Missing Feature | Priority | Line Reference | Notes |
|-----------------|----------|-----------------|-------|
| Update callouts | Medium | tool registrations [42](yandex_mcp/tools/direct/adextensions.py:42), [91](yandex_mcp/tools/direct/adextensions.py:91), [133](yandex_mcp/tools/direct/adextensions.py:133) | No update tool implemented |
| Delete callouts | Medium | tool registrations [42](yandex_mcp/tools/direct/adextensions.py:42), [91](yandex_mcp/tools/direct/adextensions.py:91), [133](yandex_mcp/tools/direct/adextensions.py:133) | No delete tool implemented |
| Other extension types | Low | type filter [18](yandex_mcp/tools/direct/adextensions.py:18) | Only CALLOUT flow exposed |

---

### 4.6 Images Service

**File:** `yandex_mcp/tools/direct/images.py`

| Missing Method | Priority | Line Reference | Notes |
|----------------|----------|----------------|-------|
| Update image metadata | Low | tool set in [register()](yandex_mcp/tools/direct/images.py:33) | No update tool registered |
| Filter by campaign/adgroup | Medium | `SelectionCriteria` in [direct_get_images()](yandex_mcp/tools/direct/images.py:93) | No campaign or adgroup filter fields |

---

### 4.7 AdVideos Service

**File:** `yandex_mcp/tools/direct/advideos.py`

| Missing Method | Priority | Line Reference | Notes |
|----------------|----------|----------------|-------|
| Delete video | Medium | tool registrations [40](yandex_mcp/tools/direct/advideos.py:40), [99](yandex_mcp/tools/direct/advideos.py:99) | No delete tool registered |
| Filter by campaign | Medium | `GetAdVideosInput` [29](yandex_mcp/tools/direct/advideos.py:29), request criteria [116](yandex_mcp/tools/direct/advideos.py:116)-[124](yandex_mcp/tools/direct/advideos.py:124) | Only `video_ids` filtering available |

---

### 4.8 Creatives Service

**File:** `yandex_mcp/tools/direct/creatives.py`

| Missing Creative Type | Priority | Line Reference | Notes |
|----------------------|----------|----------------|-------|
| CPC_VIDEO_CREATIVE | Medium | creation payload [51](yandex_mcp/tools/direct/creatives.py:51)-[56](yandex_mcp/tools/direct/creatives.py:56) | Only VIDEO_EXTENSION_CREATIVE creation implemented |
| CPM_VIDEO_CREATIVE | Medium | creation payload [51](yandex_mcp/tools/direct/creatives.py:51)-[56](yandex_mcp/tools/direct/creatives.py:56) | Not implemented |
| BANNER_CREATIVE | Low | creation payload [51](yandex_mcp/tools/direct/creatives.py:51)-[56](yandex_mcp/tools/direct/creatives.py:56) | Not implemented |

---

### 4.9 Feeds Service

**File:** `yandex_mcp/tools/direct/feeds.py`

| Missing Method | Priority | Line Reference | Notes |
|----------------|----------|----------------|-------|
| Create from FILE source type | Medium | `SourceType` hardcoded in [direct_add_feed()](yandex_mcp/tools/direct/feeds.py:85) | Only URL source currently exposed |
| Explicit refresh operation | Medium | available methods in [register()](yandex_mcp/tools/direct/feeds.py:53) | Status can be read via get, but no dedicated refresh trigger/poll helper |

---

## 5. API Version Issues

### 5.1 v5 vs v501 Differences

| Feature | v5 | v501 | Required For |
|---------|----|------|--------------|
| Standard Campaigns | ✅ | ✅ | All basic campaigns |
| UnifiedCampaign | ❌ | ✅ | ЕПК (Unified Performance Campaign) |
| ShoppingAd | ❌ | ✅ | Product ads in UnifiedCampaign |
| UnifiedAdGroup | ❌ | ✅ | Ad groups in UnifiedCampaign |
| LeadForms | ❌ | ✅ | Lead generation forms |

### 5.2 Features Requiring v501 Endpoint

**Current Implementation Assessment:**

| Feature | File | Line | Status |
|---------|------|------|--------|
| UNIFIED_CAMPAIGN creation | campaigns.py | 417-418 | ✅ Correct |
| UnifiedAdGroup creation | adgroups.py | 119-120 | ✅ Correct |
| ShoppingAd creation | ads.py | use_v501=True | ✅ Correct |
| Ad moderate | ads.py | use_v501=True | ✅ Correct |
| Link callouts | adextensions.py | use_v501=True | ✅ Correct |

### 5.3 v501 Usage in Client

**File:** `yandex_mcp/client.py`

```python
# Correct implementation pattern
async def direct_request(self, service: str, method: str, params: dict, 
                        use_v501: bool = False, timeout: float = 30.0):
    # Endpoint selection
    base_url = "https://api.direct.yandex.com/json/v501" if use_v501 else \
               "https://api.direct.yandex.com/json/v5"
```

Reference points: [
_get_direct_url()](yandex_mcp/client.py:40), [
direct_request()](yandex_mcp/client.py:46).

### 5.4 Operational Implications: Auth, Headers, Sandbox, Limits

- Auth tokens are sourced from env vars in [__init__()](yandex_mcp/client.py:20): `YANDEX_DIRECT_TOKEN`, `YANDEX_TOKEN`, optional `YANDEX_CLIENT_LOGIN`.
- Direct headers are assembled in [direct_request()](yandex_mcp/client.py:63) and include `Authorization`, `Accept-Language`, `Content-Type`, and conditional `Client-Login`.
- Sandbox routing is controlled by [use_sandbox](yandex_mcp/client.py:26) and [_get_direct_url()](yandex_mcp/client.py:40).
- Default timeout behavior is set in [direct_request()](yandex_mcp/client.py:77), with service-specific override used by [direct_upload_video()](yandex_mcp/tools/direct/advideos.py:77).

### 5.5 Reports Async Behavior and Retry Semantics

Reports polling is implemented in [direct_get_statistics()](yandex_mcp/tools/direct/stats.py:28):
- request loop: [93](yandex_mcp/tools/direct/stats.py:93)-[105](yandex_mcp/tools/direct/stats.py:105)
- handles `201` and `202` as in-progress states
- waits on `retryIn` header: [100](yandex_mcp/tools/direct/stats.py:100)-[103](yandex_mcp/tools/direct/stats.py:103)
- exits with fallback message after max attempts: [104](yandex_mcp/tools/direct/stats.py:104)

---

## 6. Missing Model Fields

### 6.1 Campaign Model Gaps

**File:** `yandex_mcp/models/direct.py`

| Field | Type | Status | Notes |
|-------|------|--------|-------|
| WalletId | int | ❌ Missing | Wallet for campaign funding |
| Statistics | dict | ⚠️ Partial | Needs more fields (Cost, Clicks, Impressions) |
| Notification | dict | ❌ Missing | Notification settings (email, SMS) |
| TimeZone | str | ❌ Missing | Campaign timezone |

**Current get_campaigns request (campaigns.py, lines 51-62):**
```python
"FieldNames": [
    "Id", "Name", "Type", "State", "Status", "StatusPayment",
    "StartDate", "EndDate", "DailyBudget", "Statistics",
    "NegativeKeywords"
]
# Missing: WalletId, Notification, TimeZone
```

---

### 6.2 BiddingStrategyType Enum Gaps

**File:** `yandex_mcp/models/direct.py` (lines 67-78)

| Strategy | Enum Status | Implementation Status |
|----------|-------------|---------------------|
| HIGHEST_POSITION | ✅ | Not implemented |
| WB_MAXIMUM_CLICKS | ✅ | ✅ Implemented |
| WB_MAXIMUM_CONVERSION_RATE | ✅ | ✅ Implemented |
| AVERAGE_CPC | ✅ | ✅ Implemented |
| AVERAGE_CPA | ✅ | ⚠️ Model exists, not in create |
| AVERAGE_ROI | ✅ | ❌ Not implemented |
| WEEKLY_CLICK_PACKAGE | ✅ | Not implemented |
| PAY_FOR_CONVERSION | ✅ | ❌ Not implemented |
| PAY_FOR_CONVERSION_CRR | ✅ | ❌ Not implemented |
| SERVING_OFF | ✅ | ✅ Implemented |

---

### 6.3 NetworkStrategyType Enum

**File:** `yandex_mcp/models/direct.py` (lines 219-230)

| Strategy | Status |
|----------|--------|
| SERVING_OFF | ✅ |
| NETWORK_DEFAULT | ✅ |
| WB_MAXIMUM_CLICKS | ✅ |
| AVERAGE_CPC | ✅ |
| WB_MAXIMUM_CONVERSION_RATE | ✅ |
| AVERAGE_CPC_PER_CAMPAIGN | ✅ |
| AVERAGE_CPC_PER_FILTER | ✅ |
| AVERAGE_CPA_PER_CAMPAIGN | ✅ |
| AVERAGE_CPA_PER_FILTER | ✅ |

---

## 7. Recommendations Summary

### High Priority

| # | Recommendation | Impact | Effort |
|---|----------------|--------|--------|
| 1 | Implement **LeadForms** service | High business value - lead generation | Medium |
| 2 | Implement **DynamicTextAdTargets** service | Required for dynamic campaign management | Medium |
| 3 | Complete **Campaign** bidding strategies `AVERAGE_CPA`, `AVERAGE_ROI`, `PAY_FOR_CONVERSION`, `PAY_FOR_CONVERSION_CRR` | Required for conversion/performance campaigns | Medium |
| 4 | Add **AdGroup** state management (suspend/resume/archive/unarchive) | Full CRUD parity | Low |

### Medium Priority

| # | Recommendation | Impact | Effort |
|---|----------------|--------|--------|
| 1 | Complete **BidModifiers** (VideoAdjustments, RetargetingAdjustments) | Enhanced targeting options | Medium |
| 2 | Implement **AgencyClients** service | Agency workflow support | Medium |
| 3 | Complete **Creatives** types (CPC_VIDEO_CREATIVE, CPM_VIDEO_CREATIVE) | Video ad support | Medium |
| 4 | Add missing **Campaign** fields (WalletId, Notification) | Complete data retrieval | Low |
| 5 | Implement **AdVideos** delete method | Resource management | Low |

### Low Priority

| # | Recommendation | Impact | Effort |
|---|----------------|--------|--------|
| 1 | Implement **TurboPages** service | Niche use case | Medium |
| 2 | Implement **VideoAds** service | Video campaign support | Medium |
| 3 | Complete **AdExtensions** (update/delete callouts) | Full CRUD parity | Low |
| 4 | Add **Images** update method | Resource management | Low |
| 5 | Implement **Keywords** archive/unarchive | Full state management | Low |

---

## 8. Implementation Roadmap

### Phase 1: Foundation & High Priority

**Timeline:** 2-3 weeks

| Week | Task | Deliverable |
|------|------|-------------|
| 1 | Add AdGroup state management methods | `adgroups.py` - suspend, resume, archive, unarchive |
| 1-2 | Complete Campaign conversion strategy set (`AVERAGE_CPA`, `AVERAGE_ROI`, `PAY_FOR_CONVERSION`, `PAY_FOR_CONVERSION_CRR`) | `campaigns.py` - normalized bidding strategy handling |
| 2 | Implement DynamicTextAdTargets service | `dynamic_text_ad_targets.py` - full CRUD |
| 2-3 | Implement LeadForms service | `lead_forms.py` - full CRUD + leads retrieval |

### Phase 2: Enhancement & Medium Priority

**Timeline:** 3-4 weeks

| Week | Task | Deliverable |
|------|------|-------------|
| 1 | Complete BidModifiers types | `bidmodifiers.py` + models - video, retargeting |
| 2 | Implement AgencyClients service | `agency_clients.py` - client management |
| 2-3 | Complete Creatives types | `creatives.py` - CPC/CPM video |
| 3-4 | Add Campaign model fields | `direct.py` - WalletId, Notification |

### Phase 3: Completion & Low Priority

**Timeline:** Ongoing

| Month | Task | Deliverable |
|-------|------|-------------|
| 1 | Implement TurboPages service | `turbopages.py` |
| 1 | Implement VideoAds service | `video_ads.py` |
| 2 | Complete AdExtensions CRUD | `adextensions.py` - update, delete |
| Ongoing | Bug fixes and optimization | Per issue tracker |

---

## Appendix A: File Reference Index

| File | Purpose | Lines |
|------|---------|-------|
| `yandex_mcp/tools/direct/__init__.py` | Service registration | 1-49 |
| `yandex_mcp/tools/direct/_helpers.py` | Reusable tool helpers | 1-200 |
| `yandex_mcp/models/direct.py` | Core models | 1-744 |
| `yandex_mcp/models/direct_extended.py` | Extended models | 1-449 |
| `yandex_mcp/client.py` | API client | 1-150 |

---

## Appendix B: Service-Method Parity Matrix

This matrix aligns with enumerated API surfaces from [docs/yandex-direct-api-v5-research.md](docs/yandex-direct-api-v5-research.md:1) and documents parity status.

| API Service | API Methods | Implemented Surface | Parity | Evidence |
|-------------|-------------|---------------------|--------|----------|
| Campaigns | get add update delete suspend resume archive unarchive | direct tools | ⚠️ Partial | [campaign tools](yandex_mcp/tools/direct/campaigns.py:20), gaps in strategy wiring [165](yandex_mcp/tools/direct/campaigns.py:165) |
| AdGroups | get add update delete suspend resume archive unarchive | get add update | ⚠️ Partial | [adgroup tools](yandex_mcp/tools/direct/adgroups.py:20) |
| Ads | get add update delete moderate suspend resume archive unarchive | full set including moderate | ✅ High | [ads tools](yandex_mcp/tools/direct/ads.py:25) |
| Keywords | get add update delete suspend resume | get add delete suspend resume | ⚠️ Partial | [keywords tools](yandex_mcp/tools/direct/keywords.py:22) |
| KeywordBids | get set | set only | ⚠️ Partial | [direct_set_keyword_bids()](yandex_mcp/tools/direct/keywords.py:127) |
| BidModifiers | get add set delete toggle | get add set delete toggle | ⚠️ Partial | [bidmodifier tools](yandex_mcp/tools/direct/bidmodifiers.py:21), missing adjustment types [63](yandex_mcp/tools/direct/bidmodifiers.py:63) |
| Sitelinks | get add delete | implemented | ✅ High | [sitelinks tools](yandex_mcp/tools/direct/sitelinks.py:19) |
| VCards | get add delete | implemented | ✅ High | [vcards tools](yandex_mcp/tools/direct/vcards.py:19) |
| AdExtensions | get add delete | get add only plus ad-link helper | ⚠️ Partial | [adextensions tools](yandex_mcp/tools/direct/adextensions.py:42) |
| AdImages | get add delete | implemented | ⚠️ Partial | [images tools](yandex_mcp/tools/direct/images.py:33), metadata update not exposed |
| AdVideos | get add delete | get add only | ⚠️ Partial | [advideos tools](yandex_mcp/tools/direct/advideos.py:40) |
| Creatives | get add | limited to video extension creation | ⚠️ Partial | [creatives tools](yandex_mcp/tools/direct/creatives.py:34) |
| Feeds | get add update delete | implemented with URL source only | ⚠️ Partial | [feeds tools](yandex_mcp/tools/direct/feeds.py:56) |
| RetargetingLists | get add update delete | implemented | ✅ High | [retargeting lists](yandex_mcp/tools/direct/retargeting.py:20) |
| AudienceTargets | get add suspend resume delete | implemented | ✅ High | [audience targets](yandex_mcp/tools/direct/retargeting.py:217) |
| SmartAdTargets | get add suspend resume delete | implemented | ✅ High | [smart targets](yandex_mcp/tools/direct/smartadtargets.py:19) |
| NegativeKeywordSharedSets | get add update delete | implemented | ✅ High | [shared negatives](yandex_mcp/tools/direct/negative_keywords_shared.py:20) |
| Dictionaries | get | implemented | ✅ High | [dictionaries](yandex_mcp/tools/direct/dictionaries.py:15) |
| Clients | get | implemented | ✅ High | [direct_get_client_info()](yandex_mcp/tools/direct/clients.py:33) |
| Changes | checkCampaigns check | implemented | ✅ High | [checkCampaigns](yandex_mcp/tools/direct/clients.py:125), [check](yandex_mcp/tools/direct/clients.py:184) |
| Reports | get | implemented with async retry | ✅ High | [direct_get_statistics()](yandex_mcp/tools/direct/stats.py:28) |
| AgencyClients | get update | missing | ❌ Missing | planned file `agency_clients.py` |
| LeadForms | get add update delete get_leads | missing | ❌ Missing | planned file `lead_forms.py` |
| TurboPages | get add update delete | missing | ❌ Missing | planned file `turbopages.py` |
| DynamicTextAdTargets | get add update suspend resume delete | missing | ❌ Missing | planned file `dynamic_text_ad_targets.py` |
| VideoAds | get add update delete | missing | ❌ Missing | planned file `video_ads.py` |

---

*Document generated: 2026-02-28*  
*Analysis based on: Yandex Direct API v5/v501 specification and yandex-mcp codebase*
