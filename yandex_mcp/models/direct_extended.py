"""Extended Pydantic models for Yandex Direct API - Sitelinks, VCards, BidModifiers, etc."""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .common import ResponseFormat


# =============================================================================
# Sitelinks Models
# =============================================================================

class GetSitelinksInput(BaseModel):
    """Input for getting sitelink sets."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    sitelink_set_ids: Optional[List[int]] = Field(
        default=None,
        description="Filter by specific sitelink set IDs"
    )
    limit: int = Field(
        default=100,
        ge=1,
        le=10000,
        description="Maximum number of sitelink sets to return"
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Offset for pagination"
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' or 'json'"
    )


class SitelinkItem(BaseModel):
    """Single sitelink item."""
    title: str = Field(..., max_length=30, description="Sitelink title (max 30 chars)")
    href: str = Field(..., description="Sitelink URL")
    description: Optional[str] = Field(default=None, max_length=60, description="Description (max 60 chars)")


class AddSitelinksInput(BaseModel):
    """Input for adding a sitelink set."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    sitelinks: List[SitelinkItem] = Field(
        ...,
        min_length=1,
        max_length=8,
        description="List of sitelinks (1-8 items)"
    )


class DeleteSitelinksInput(BaseModel):
    """Input for deleting sitelink sets."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    sitelink_set_ids: List[int] = Field(
        ...,
        min_length=1,
        description="Sitelink set IDs to delete"
    )


# =============================================================================
# VCards Models
# =============================================================================

class GetVCardsInput(BaseModel):
    """Input for getting vCards."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    vcard_ids: Optional[List[int]] = Field(
        default=None,
        description="Filter by specific vCard IDs"
    )
    limit: int = Field(
        default=100,
        ge=1,
        le=10000,
        description="Maximum number of vCards to return"
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Offset for pagination"
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' or 'json'"
    )


class AddVCardInput(BaseModel):
    """Input for adding a vCard."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    campaign_id: int = Field(..., description="Campaign ID for this vCard")
    company: str = Field(..., max_length=255, description="Company name")
    country_code: str = Field(default="+7", description="Phone country code (e.g., +7)")
    city_code: str = Field(..., description="Phone city code (e.g., 423 for Vladivostok)")
    phone_number: str = Field(..., description="Phone number without codes (e.g., 204-50-70)")
    phone_extension: Optional[str] = Field(default=None, description="Phone extension")
    country: str = Field(default="Россия", description="Country name")
    city: str = Field(..., description="City name")
    street: Optional[str] = Field(default=None, description="Street address")
    house: Optional[str] = Field(default=None, description="House number")
    work_time: Optional[str] = Field(default=None, description="Working hours (e.g., '0#3#10#00#18#00')")
    extra_message: Optional[str] = Field(default=None, max_length=200, description="Additional info")


class DeleteVCardsInput(BaseModel):
    """Input for deleting vCards."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    vcard_ids: List[int] = Field(
        ...,
        min_length=1,
        description="vCard IDs to delete"
    )


# =============================================================================
# BidModifiers Models
# =============================================================================

class GetBidModifiersInput(BaseModel):
    """Input for getting bid modifiers."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    campaign_ids: Optional[List[int]] = Field(
        default=None,
        description="Filter by campaign IDs"
    )
    adgroup_ids: Optional[List[int]] = Field(
        default=None,
        description="Filter by ad group IDs"
    )
    bid_modifier_ids: Optional[List[int]] = Field(
        default=None,
        description="Filter by specific bid modifier IDs"
    )
    types: Optional[List[str]] = Field(
        default=None,
        description="Filter by types: MOBILE_ADJUSTMENT, DESKTOP_ADJUSTMENT, DEMOGRAPHICS_ADJUSTMENT, etc."
    )
    limit: int = Field(
        default=100,
        ge=1,
        le=10000,
        description="Maximum number to return"
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' or 'json'"
    )


class MobileAdjustment(BaseModel):
    """Mobile bid adjustment."""
    bid_modifier: int = Field(..., ge=0, le=1300, description="Bid modifier percent (0-1300, 100=no change)")


class DesktopAdjustment(BaseModel):
    """Desktop bid adjustment."""
    bid_modifier: int = Field(..., ge=0, le=1300, description="Bid modifier percent (0-1300)")


class DemographicsAdjustment(BaseModel):
    """Demographics bid adjustment."""
    gender: Optional[str] = Field(default=None, description="GENDER_MALE or GENDER_FEMALE")
    age: Optional[str] = Field(default=None, description="AGE_0_17, AGE_18_24, AGE_25_34, AGE_35_44, AGE_45_54, AGE_55")
    bid_modifier: int = Field(..., ge=0, le=1300, description="Bid modifier percent")


class RegionalAdjustment(BaseModel):
    """Regional bid adjustment."""
    region_id: int = Field(..., description="Region ID")
    bid_modifier: int = Field(..., ge=10, le=1300, description="Bid modifier percent (10-1300)")


class VideoAdjustment(BaseModel):
    """Video bid adjustment for video ad campaigns."""
    bid_modifier: int = Field(..., ge=0, le=1300, description="Bid modifier percent (0-1300, 100=no change)")


class RetargetingAdjustment(BaseModel):
    """Retargeting list bid adjustment."""
    retargeting_list_id: int = Field(..., description="Retargeting list ID")
    bid_modifier: int = Field(..., ge=0, le=1300, description="Bid modifier percent (0-1300)")
    enabled: bool = Field(default=True, description="Whether the adjustment is enabled")


class AddBidModifierInput(BaseModel):
    """Input for adding bid modifiers."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    campaign_id: Optional[int] = Field(default=None, description="Campaign ID (for campaign-level modifier)")
    adgroup_id: Optional[int] = Field(default=None, description="Ad group ID (for group-level modifier)")

    mobile_adjustment: Optional[MobileAdjustment] = Field(default=None, description="Mobile device adjustment")
    desktop_adjustment: Optional[DesktopAdjustment] = Field(default=None, description="Desktop adjustment")
    demographics_adjustments: Optional[List[DemographicsAdjustment]] = Field(default=None, description="Demographics adjustments")
    regional_adjustments: Optional[List[RegionalAdjustment]] = Field(default=None, description="Regional adjustments")
    video_adjustment: Optional[VideoAdjustment] = Field(default=None, description="Video ad campaign adjustment")
    retargeting_adjustments: Optional[List[RetargetingAdjustment]] = Field(default=None, description="Retargeting list adjustments")


class SetBidModifierInput(BaseModel):
    """Input for setting bid modifier value."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    bid_modifier_id: int = Field(..., description="Bid modifier ID")
    bid_modifier: int = Field(..., ge=0, le=1300, description="New bid modifier percent")


class DeleteBidModifiersInput(BaseModel):
    """Input for deleting bid modifiers."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    bid_modifier_ids: List[int] = Field(
        ...,
        min_length=1,
        description="Bid modifier IDs to delete"
    )


class ToggleBidModifiersInput(BaseModel):
    """Input for enabling/disabling bid modifiers."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    bid_modifier_ids: List[int] = Field(..., description="Bid modifier IDs")
    enabled: bool = Field(..., description="Enable (True) or disable (False)")


# =============================================================================
# RetargetingLists Models
# =============================================================================

class GetRetargetingListsInput(BaseModel):
    """Input for getting retargeting lists."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    retargeting_list_ids: Optional[List[int]] = Field(
        default=None,
        description="Filter by specific retargeting list IDs"
    )
    limit: int = Field(
        default=100,
        ge=1,
        le=10000,
        description="Maximum number to return"
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' or 'json'"
    )


class RetargetingRule(BaseModel):
    """Single retargeting rule."""
    goal_id: int = Field(..., description="Metrika goal ID")
    member_of: str = Field(default="POSITIVE", description="POSITIVE or NEGATIVE")
    days: int = Field(default=30, ge=1, le=540, description="Days to look back (1-540)")


class AddRetargetingListInput(BaseModel):
    """Input for adding a retargeting list."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(..., max_length=255, description="Retargeting list name")
    rules: List[List[RetargetingRule]] = Field(
        ...,
        description="Rules groups (OR between groups, AND within group)"
    )
    description: Optional[str] = Field(default=None, description="Description")


class UpdateRetargetingListInput(BaseModel):
    """Input for updating a retargeting list."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    retargeting_list_id: int = Field(..., description="Retargeting list ID")
    name: Optional[str] = Field(default=None, max_length=255, description="New name")
    rules: Optional[List[List[RetargetingRule]]] = Field(default=None, description="New rules")
    description: Optional[str] = Field(default=None, description="New description")


class DeleteRetargetingListsInput(BaseModel):
    """Input for deleting retargeting lists."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    retargeting_list_ids: List[int] = Field(
        ...,
        min_length=1,
        description="Retargeting list IDs to delete"
    )


# =============================================================================
# AudienceTargets Models
# =============================================================================

class GetAudienceTargetsInput(BaseModel):
    """Input for getting audience targets."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    campaign_ids: Optional[List[int]] = Field(default=None, description="Filter by campaign IDs")
    adgroup_ids: Optional[List[int]] = Field(default=None, description="Filter by ad group IDs")
    audience_target_ids: Optional[List[int]] = Field(default=None, description="Filter by IDs")
    limit: int = Field(default=100, ge=1, le=10000)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class AddAudienceTargetInput(BaseModel):
    """Input for adding an audience target."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    adgroup_id: int = Field(..., description="Ad group ID")
    retargeting_list_id: int = Field(..., description="Retargeting list ID")
    interest_id: Optional[int] = Field(default=None, description="Interest category ID")
    context_bid: Optional[float] = Field(default=None, gt=0, description="Bid for context networks")


class ManageAudienceTargetsInput(BaseModel):
    """Input for managing audience targets (suspend/resume/delete)."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    audience_target_ids: List[int] = Field(..., min_length=1, description="Audience target IDs")


# =============================================================================
# NegativeKeywordSharedSets Models
# =============================================================================

class GetNegativeKeywordSharedSetsInput(BaseModel):
    """Input for getting negative keyword shared sets."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    shared_set_ids: Optional[List[int]] = Field(default=None, description="Filter by IDs")
    limit: int = Field(default=100, ge=1, le=10000)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class AddNegativeKeywordSharedSetInput(BaseModel):
    """Input for adding a negative keyword shared set."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(..., max_length=255, description="Set name")
    negative_keywords: List[str] = Field(..., min_length=1, description="Negative keywords")


class UpdateNegativeKeywordSharedSetInput(BaseModel):
    """Input for updating a negative keyword shared set."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    shared_set_id: int = Field(..., description="Shared set ID")
    name: Optional[str] = Field(default=None, max_length=255, description="New name")
    negative_keywords: Optional[List[str]] = Field(default=None, description="New negative keywords")


class DeleteNegativeKeywordSharedSetsInput(BaseModel):
    """Input for deleting negative keyword shared sets."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    shared_set_ids: List[int] = Field(..., min_length=1, description="Set IDs to delete")


# =============================================================================
# Dictionaries Models
# =============================================================================

class GetDictionariesInput(BaseModel):
    """Input for getting dictionaries."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    dictionary_names: List[str] = Field(
        ...,
        min_length=1,
        description="Dictionary names: GeoRegions, Currencies, TimeZones, Constants, AdCategories, OperationSystemVersions, ProductivityAssertions, SupplySidePlatforms, Interests, AudienceCriteriaTypes"
    )
    response_format: ResponseFormat = Field(default=ResponseFormat.JSON)


# =============================================================================
# Changes Models
# =============================================================================

class CheckCampaignChangesInput(BaseModel):
    """Input for checking campaign changes."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    campaign_ids: List[int] = Field(..., min_length=1, description="Campaign IDs to check")
    timestamp: str = Field(..., description="Timestamp from previous check (ISO 8601)")
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class CheckAllChangesInput(BaseModel):
    """Input for checking all changes."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    timestamp: str = Field(..., description="Timestamp from previous check (ISO 8601)")
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


# =============================================================================
# Clients Models
# =============================================================================


class GetClientInfoInput(BaseModel):
    """Input for getting client info."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


# =============================================================================
# AdImages Models
# =============================================================================

class ImageType(str, Enum):
    """Ad image type."""
    REGULAR = "REGULAR"
    WIDE = "WIDE"


class ImageAssociated(str, Enum):
    """Image association status."""
    YES = "YES"
    NO = "NO"


class UploadImageInput(BaseModel):
    """Input for uploading an ad image."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    image_data: str = Field(..., description="Base64-encoded image data")
    name: str = Field(..., max_length=255, description="Image name")
    image_type: ImageType = Field(default=ImageType.REGULAR, description="Image type: REGULAR or WIDE")


class GetImagesInput(BaseModel):
    """Input for getting ad images."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    ad_image_hashes: Optional[List[str]] = Field(default=None, description="Filter by image hashes")
    associated: Optional[ImageAssociated] = Field(default=None, description="Filter by association: YES or NO")
    limit: int = Field(default=100, ge=1, le=10000, description="Maximum images to return")
    offset: int = Field(default=0, ge=0, description="Offset for pagination")
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="Output format")


class DeleteImagesInput(BaseModel):
    """Input for deleting ad images."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    ad_image_hashes: List[str] = Field(..., min_length=1, description="Image hashes to delete")


# =============================================================================
# DynamicTextAdTargets Models
# =============================================================================

class DynamicTextAdTargetCondition(BaseModel):
    """A single filter condition for dynamic text ad targeting."""
    operand: str = Field(..., description="Feed field name (e.g., 'price', 'manufacturer', 'category_id', 'url', 'title')")
    operator: str = Field(..., description="Operator: EQUALS_ANY, CONTAINS_ANY, NOT_CONTAINS_ALL, GREATER_THAN, LESS_THAN, IN_RANGE, EXISTS")
    arguments: List[str] = Field(..., description="Values to match (max 50). For IN_RANGE use 'min-max' format.")


class GetDynamicTextAdTargetsInput(BaseModel):
    """Input for getting dynamic text ad targets."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    campaign_ids: Optional[List[int]] = Field(default=None, description="Filter by campaign IDs")
    adgroup_ids: Optional[List[int]] = Field(default=None, description="Filter by ad group IDs")
    target_ids: Optional[List[int]] = Field(default=None, description="Filter by target IDs")
    limit: int = Field(default=100, ge=1, le=10000)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class AddDynamicTextAdTargetInput(BaseModel):
    """Input for adding a dynamic text ad target."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    adgroup_id: int = Field(..., description="Ad group ID (dynamic text ad group)")
    name: str = Field(..., max_length=255, description="Target name")
    auto_budget: bool = Field(default=True, description="Use campaign budget (YES) or set manual bid (NO)")
    bid: Optional[float] = Field(default=None, gt=0, description="Manual bid (if auto_budget is NO)")
    conditions: Optional[List[DynamicTextAdTargetCondition]] = Field(
        default=None,
        description="Filter conditions. If empty, all feed items are used."
    )


class UpdateDynamicTextAdTargetInput(BaseModel):
    """Input for updating a dynamic text ad target."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    target_id: int = Field(..., description="Dynamic text ad target ID")
    name: Optional[str] = Field(default=None, max_length=255, description="New name")
    auto_budget: Optional[bool] = Field(default=None, description="Use campaign budget (YES) or set manual bid (NO)")
    bid: Optional[float] = Field(default=None, gt=0, description="Manual bid (if auto_budget is NO)")
    conditions: Optional[List[DynamicTextAdTargetCondition]] = Field(default=None, description="New conditions")


class ManageDynamicTextAdTargetsInput(BaseModel):
    """Input for managing dynamic text ad targets (suspend/resume/delete)."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    target_ids: List[int] = Field(..., min_length=1, description="Dynamic text ad target IDs")


class DeleteDynamicTextAdTargetsInput(BaseModel):
    """Input for deleting dynamic text ad targets."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    target_ids: List[int] = Field(..., min_length=1, description="Dynamic text ad target IDs to delete")


# =============================================================================
# LeadForms Models
# =============================================================================

class QuestionType(str, Enum):
    """Lead form question types."""
    NAME = "NAME"
    PHONE = "PHONE"
    EMAIL = "EMAIL"
    ADDRESS = "ADDRESS"
    COMMENT = "COMMENT"
    CHECKBOX = "CHECKBOX"


class LeadFormQuestion(BaseModel):
    """A single question in the lead form."""
    type: QuestionType = Field(..., description="Question type: NAME, PHONE, EMAIL, ADDRESS, COMMENT, CHECKBOX")
    required: bool = Field(default=False, description="Whether this question is required")
    label: Optional[str] = Field(default=None, max_length=255, description="Custom label for the question")


class GetLeadFormsInput(BaseModel):
    """Input for getting lead forms."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    campaign_ids: Optional[List[int]] = Field(default=None, description="Filter by campaign IDs")
    adgroup_ids: Optional[List[int]] = Field(default=None, description="Filter by ad group IDs")
    form_ids: Optional[List[int]] = Field(default=None, description="Filter by form IDs")
    limit: int = Field(default=100, ge=1, le=10000, description="Maximum forms to return")
    offset: int = Field(default=0, ge=0, description="Offset for pagination")
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


class AddLeadFormInput(BaseModel):
    """Input for adding a lead form."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(..., max_length=255, description="Lead form name")
    campaign_id: int = Field(..., description="Campaign ID")
    url: str = Field(..., max_length=1024, description="Landing page URL where form is placed")
    policy_url: str = Field(..., max_length=1024, description="Privacy policy URL")
    short_form: bool = Field(default=False, description="Use short form (only name + phone)")
    questions: Optional[List[LeadFormQuestion]] = Field(
        default=None,
        description="Form questions. If not specified, default questions will be used."
    )


class UpdateLeadFormInput(BaseModel):
    """Input for updating a lead form."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    form_id: int = Field(..., description="Lead form ID to update")
    name: Optional[str] = Field(default=None, max_length=255, description="New form name")
    url: Optional[str] = Field(default=None, max_length=1024, description="New landing page URL")
    policy_url: Optional[str] = Field(default=None, max_length=1024, description="New privacy policy URL")
    short_form: Optional[bool] = Field(default=None, description="Use short form")
    questions: Optional[List[LeadFormQuestion]] = Field(default=None, description="New questions")


class DeleteLeadFormsInput(BaseModel):
    """Input for deleting lead forms."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    form_ids: List[int] = Field(..., min_length=1, description="Lead form IDs to delete")


class GetLeadFormLeadsInput(BaseModel):
    """Input for getting leads from lead forms."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    form_ids: Optional[List[int]] = Field(default=None, description="Filter by form IDs")
    limit: int = Field(default=100, ge=1, le=10000, description="Maximum leads to return")
    offset: int = Field(default=0, ge=0, description="Offset for pagination")
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)


# =============================================================================
# AgencyClients Models
# =============================================================================

class GetAgencyClientsInput(BaseModel):
    """Input for getting agency client accounts."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    logins: Optional[List[str]] = Field(
        default=None,
        description="Filter by client logins (usernames)"
    )
    status: Optional[List[str]] = Field(
        default=None,
        description="Filter by status: ALLOWED, SUSPENDED, BLOCKED, NONE"
    )
    limit: int = Field(
        default=100,
        ge=1,
        le=10000,
        description="Maximum number of clients to return"
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Offset for pagination"
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' or 'json'"
    )


class AgencyClientSettings(BaseModel):
    """Settings for agency client."""
    send_account_warnings: Optional[bool] = Field(
        default=None,
        description="Send account warnings to client"
    )
    send_notification_about_warnings: Optional[bool] = Field(
        default=None,
        description="Send notification about warnings"
    )


class AgencyClientNotification(BaseModel):
    """Notification settings for agency client."""
    email: Optional[str] = Field(
        default=None,
        description="Email for notifications"
    )
    email_balance: Optional[bool] = Field(
        default=None,
        description="Send balance notifications"
    )
    email_trade_offers: Optional[bool] = Field(
        default=None,
        description="Send trade offers notifications"
    )
    email_advertising_on_account: Optional[bool] = Field(
        default=None,
        description="Send advertising on account notifications"
    )


class UpdateAgencyClientInput(BaseModel):
    """Input for updating an agency client."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    login: str = Field(
        ...,
        description="Client login (username) to update"
    )
    settings: Optional[AgencyClientSettings] = Field(
        default=None,
        description="Client settings"
    )
    notification: Optional[AgencyClientNotification] = Field(
        default=None,
        description="Notification settings"
    )
