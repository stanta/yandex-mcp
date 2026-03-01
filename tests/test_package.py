"""Tests for Yandex MCP package structure and tool registration."""

import pytest


EXPECTED_DIRECT_TOOLS = [
    # Campaigns (8)
    "direct_get_campaigns",
    "direct_create_campaign",
    "direct_update_campaign",
    "direct_suspend_campaigns",
    "direct_resume_campaigns",
    "direct_archive_campaigns",
    "direct_unarchive_campaigns",
    "direct_delete_campaigns",
    # Ad Groups (7)
    "direct_get_adgroups",
    "direct_create_adgroup",
    "direct_update_adgroup",
    "direct_suspend_adgroups",
    "direct_resume_adgroups",
    "direct_archive_adgroups",
    "direct_unarchive_adgroups",
    # Ads (12)
    "direct_get_ads",
    "direct_create_text_ad",
    "direct_create_image_ad",
    "direct_create_dynamic_ad",
    "direct_create_shopping_ad",
    "direct_update_ad",
    "direct_moderate_ads",
    "direct_suspend_ads",
    "direct_resume_ads",
    "direct_archive_ads",
    "direct_unarchive_ads",
    "direct_delete_ads",
    # Keywords (6)
    "direct_get_keywords",
    "direct_add_keywords",
    "direct_set_keyword_bids",
    "direct_suspend_keywords",
    "direct_resume_keywords",
    "direct_delete_keywords",
    # Statistics (1)
    "direct_get_statistics",
    # Bid Modifiers (5)
    "direct_get_bid_modifiers",
    "direct_add_bid_modifier",
    "direct_set_bid_modifier",
    "direct_delete_bid_modifiers",
    "direct_toggle_bid_modifiers",
    # Retargeting (4)
    "direct_get_retargeting_lists",
    "direct_add_retargeting_list",
    "direct_update_retargeting_list",
    "direct_delete_retargeting_lists",
    # Audience Targets (5)
    "direct_get_audience_targets",
    "direct_add_audience_target",
    "direct_suspend_audience_targets",
    "direct_resume_audience_targets",
    "direct_delete_audience_targets",
    # Smart Ad Targets (5)
    "direct_get_smart_ad_targets",
    "direct_add_smart_ad_target",
    "direct_suspend_smart_ad_targets",
    "direct_resume_smart_ad_targets",
    "direct_delete_smart_ad_targets",
    # Dynamic Text Ad Targets (6)
    "direct_get_dynamic_text_ad_targets",
    "direct_add_dynamic_text_ad_target",
    "direct_update_dynamic_text_ad_target",
    "direct_suspend_dynamic_text_ad_targets",
    "direct_resume_dynamic_text_ad_targets",
    "direct_delete_dynamic_text_ad_targets",
    # Sitelinks (3)
    "direct_get_sitelinks",
    "direct_add_sitelinks",
    "direct_delete_sitelinks",
    # VCards (3)
    "direct_get_vcards",
    "direct_add_vcard",
    "direct_delete_vcards",
    # Negative Keywords (4)
    "direct_get_negative_keyword_shared_sets",
    "direct_add_negative_keyword_shared_set",
    "direct_update_negative_keyword_shared_set",
    "direct_delete_negative_keyword_shared_sets",
    # Ad Extensions (3)
    "direct_get_adextensions",
    "direct_add_callouts",
    "direct_link_callouts_to_ad",
    # Videos & Creatives (7)
    "direct_upload_video",
    "direct_get_advideos",
    "direct_delete_advideos",
    "direct_create_video_creative",
    "direct_create_cpc_video_creative",
    "direct_create_cpm_video_creative",
    "direct_get_creatives",
    # Feeds (4)
    "direct_get_feeds",
    "direct_add_feed",
    "direct_update_feed",
    "direct_delete_feeds",
    # Images (3)
    "direct_upload_image",
    "direct_get_images",
    "direct_delete_images",
    # Dictionaries & Regions (3)
    "direct_get_dictionaries",
    "direct_get_regions",
    "direct_get_interests",
    # Client & Changes (4)
    "direct_get_client_info",
    "direct_check_campaign_changes",
    "direct_check_all_changes",
    "direct_get_recent_changes_timestamp",
    # Lead Forms (5)
    "direct_get_lead_forms",
    "direct_add_lead_form",
    "direct_update_lead_form",
    "direct_delete_lead_forms",
    "direct_get_lead_form_leads",
    # Agency Clients (2)
    "direct_get_agency_clients",
    "direct_update_agency_client",
    # TurboPages (5)
    "direct_get_turbo_pages",
    "direct_add_turbo_page",
    "direct_update_turbo_page",
    "direct_delete_turbo_pages",
    "direct_get_turbo_page_templates",
]

EXPECTED_METRIKA_TOOLS = [
    # Counters (5)
    "metrika_get_counters",
    "metrika_get_counter",
    "metrika_create_counter",
    "metrika_update_counter",
    "metrika_delete_counter",
    # Goals (4)
    "metrika_get_goals",
    "metrika_create_goal",
    "metrika_update_goal",
    "metrika_delete_goal",
    # Reports (4)
    "metrika_get_report",
    "metrika_get_report_by_time",
    "metrika_get_comparison_report",
    "metrika_get_drilldown_report",
    # Segments (4)
    "metrika_get_segments",
    "metrika_create_segment",
    "metrika_update_segment",
    "metrika_delete_segment",
    # Filters (4)
    "metrika_get_filters",
    "metrika_create_filter",
    "metrika_update_filter",
    "metrika_delete_filter",
    # Grants (4)
    "metrika_get_grants",
    "metrika_add_grant",
    "metrika_update_grant",
    "metrika_delete_grant",
    # Offline Data (5)
    "metrika_upload_offline_conversions",
    "metrika_get_offline_conversions_status",
    "metrika_upload_calls",
    "metrika_upload_expenses",
    "metrika_upload_user_parameters",
    # Labels (6)
    "metrika_get_labels",
    "metrika_create_label",
    "metrika_update_label",
    "metrika_delete_label",
    "metrika_link_counter_to_label",
    "metrika_unlink_counter_from_label",
    # Annotations (4)
    "metrika_get_annotations",
    "metrika_create_annotation",
    "metrika_update_annotation",
    "metrika_delete_annotation",
    # Delegates (3)
    "metrika_get_delegates",
    "metrika_add_delegate",
    "metrika_delete_delegate",
]

EXPECTED_WORDSTAT_TOOLS = [
    "wordstat_top_requests",
    "wordstat_dynamics",
    "wordstat_regions",
    "wordstat_regions_tree",
    "wordstat_user_info",
]


class TestToolRegistration:
    """Test that all tools are properly registered."""

    def test_total_tool_count(self, mcp_instance):
        tools = list(mcp_instance._tool_manager._tools.keys())
        expected = len(EXPECTED_DIRECT_TOOLS) + len(EXPECTED_METRIKA_TOOLS) + len(EXPECTED_WORDSTAT_TOOLS)
        assert len(tools) == expected, (
            f"Expected {expected} tools, got {len(tools)}. "
            f"Missing: {set(EXPECTED_DIRECT_TOOLS + EXPECTED_METRIKA_TOOLS + EXPECTED_WORDSTAT_TOOLS) - set(tools)}. "
            f"Extra: {set(tools) - set(EXPECTED_DIRECT_TOOLS + EXPECTED_METRIKA_TOOLS + EXPECTED_WORDSTAT_TOOLS)}"
        )

    def test_direct_tool_count(self, mcp_instance):
        tools = [t for t in mcp_instance._tool_manager._tools if t.startswith("direct_")]
        assert len(tools) == len(EXPECTED_DIRECT_TOOLS)

    def test_metrika_tool_count(self, mcp_instance):
        tools = [t for t in mcp_instance._tool_manager._tools if t.startswith("metrika_")]
        assert len(tools) == len(EXPECTED_METRIKA_TOOLS)

    def test_wordstat_tool_count(self, mcp_instance):
        tools = [t for t in mcp_instance._tool_manager._tools if t.startswith("wordstat_")]
        assert len(tools) == len(EXPECTED_WORDSTAT_TOOLS)

    @pytest.mark.parametrize("tool_name", EXPECTED_DIRECT_TOOLS)
    def test_direct_tool_exists(self, mcp_instance, tool_name):
        assert tool_name in mcp_instance._tool_manager._tools, f"Missing Direct tool: {tool_name}"

    @pytest.mark.parametrize("tool_name", EXPECTED_METRIKA_TOOLS)
    def test_metrika_tool_exists(self, mcp_instance, tool_name):
        assert tool_name in mcp_instance._tool_manager._tools, f"Missing Metrika tool: {tool_name}"

    @pytest.mark.parametrize("tool_name", EXPECTED_WORDSTAT_TOOLS)
    def test_wordstat_tool_exists(self, mcp_instance, tool_name):
        assert tool_name in mcp_instance._tool_manager._tools, f"Missing Wordstat tool: {tool_name}"


class TestToolNaming:
    """Test naming conventions."""

    def test_all_direct_tools_prefixed(self, mcp_instance):
        direct_tools = [t for t in mcp_instance._tool_manager._tools if t.startswith("direct_")]
        for tool in direct_tools:
            assert tool.startswith("direct_"), f"Direct tool not properly prefixed: {tool}"

    def test_all_metrika_tools_prefixed(self, mcp_instance):
        metrika_tools = [t for t in mcp_instance._tool_manager._tools if t.startswith("metrika_")]
        for tool in metrika_tools:
            assert tool.startswith("metrika_"), f"Metrika tool not properly prefixed: {tool}"

    def test_all_wordstat_tools_prefixed(self, mcp_instance):
        wordstat_tools = [t for t in mcp_instance._tool_manager._tools if t.startswith("wordstat_")]
        for tool in wordstat_tools:
            assert tool.startswith("wordstat_"), f"Wordstat tool not properly prefixed: {tool}"

    def test_no_unknown_prefixes(self, mcp_instance):
        known_prefixes = ("direct_", "metrika_", "wordstat_")
        for tool in mcp_instance._tool_manager._tools:
            assert any(tool.startswith(p) for p in known_prefixes), f"Unknown prefix in tool: {tool}"


class TestImports:
    """Test that all modules import cleanly."""

    def test_import_package(self):
        import yandex_mcp
        assert hasattr(yandex_mcp, "mcp")

    def test_import_client(self):
        from yandex_mcp.client import api_client
        assert api_client is not None

    def test_import_config(self):
        from yandex_mcp.config import YANDEX_DIRECT_API_URL, YANDEX_WORDSTAT_API_URL
        assert "direct" in YANDEX_DIRECT_API_URL
        assert "wordstat" in YANDEX_WORDSTAT_API_URL

    def test_import_models(self):
        from yandex_mcp.models.common import ResponseFormat
        assert ResponseFormat.JSON.value == "json"
        assert ResponseFormat.MARKDOWN.value == "markdown"

    def test_import_wordstat_models(self):
        from yandex_mcp.models.wordstat import (
            WordstatTopRequestsInput,
            WordstatDynamicsInput,
            WordstatRegionsInput,
        )
        assert WordstatTopRequestsInput is not None

    def test_import_formatters(self):
        from yandex_mcp.formatters.wordstat import format_wordstat_top_requests_markdown
        assert callable(format_wordstat_top_requests_markdown)


class TestBiddingStrategies:
    """Test bidding strategy models and enums."""

    def test_bidding_strategy_types_enum(self):
        """Test that all bidding strategy types are defined."""
        from yandex_mcp.models.direct import BiddingStrategyType
        
        # Verify all expected strategies exist
        assert BiddingStrategyType.WB_MAXIMUM_CLICKS.value == "WB_MAXIMUM_CLICKS"
        assert BiddingStrategyType.AVERAGE_CPC.value == "AVERAGE_CPC"
        assert BiddingStrategyType.WB_MAXIMUM_CONVERSION_RATE.value == "WB_MAXIMUM_CONVERSION_RATE"
        assert BiddingStrategyType.AVERAGE_CPA.value == "AVERAGE_CPA"
        assert BiddingStrategyType.AVERAGE_ROI.value == "AVERAGE_ROI"
        assert BiddingStrategyType.PAY_FOR_CONVERSION.value == "PAY_FOR_CONVERSION"
        assert BiddingStrategyType.PAY_FOR_CONVERSION_CRR.value == "PAY_FOR_CONVERSION_CRR"
        assert BiddingStrategyType.SERVING_OFF.value == "SERVING_OFF"

    def test_update_campaign_input_with_average_cpa(self):
        """Test UpdateCampaignInput with AVERAGE_CPA strategy."""
        from yandex_mcp.models.direct import UpdateCampaignInput, BiddingStrategyType
        
        input_data = UpdateCampaignInput(
            campaign_id=12345678,
            bidding_strategy_type=BiddingStrategyType.AVERAGE_CPA,
            average_cpa=500.0,
            goal_id=9876543,
            weekly_spend_limit=10000.0
        )
        assert input_data.campaign_id == 12345678
        assert input_data.bidding_strategy_type == BiddingStrategyType.AVERAGE_CPA
        assert input_data.average_cpa == 500.0
        assert input_data.goal_id == 9876543
        assert input_data.weekly_spend_limit == 10000.0

    def test_update_campaign_input_with_average_roi(self):
        """Test UpdateCampaignInput with AVERAGE_ROI strategy."""
        from yandex_mcp.models.direct import UpdateCampaignInput, BiddingStrategyType
        
        input_data = UpdateCampaignInput(
            campaign_id=12345678,
            bidding_strategy_type=BiddingStrategyType.AVERAGE_ROI,
            roi_coef=1.5,
            reserve_return=0.8,
            goal_id=9876543,
            weekly_spend_limit=5000.0
        )
        assert input_data.bidding_strategy_type == BiddingStrategyType.AVERAGE_ROI
        assert input_data.roi_coef == 1.5
        assert input_data.reserve_return == 0.8
        assert input_data.goal_id == 9876543

    def test_update_campaign_input_with_pay_for_conversion(self):
        """Test UpdateCampaignInput with PAY_FOR_CONVERSION strategy."""
        from yandex_mcp.models.direct import UpdateCampaignInput, BiddingStrategyType
        
        input_data = UpdateCampaignInput(
            campaign_id=12345678,
            bidding_strategy_type=BiddingStrategyType.PAY_FOR_CONVERSION,
            max_conversion_cost=1000.0,
            goal_id=9876543
        )
        assert input_data.bidding_strategy_type == BiddingStrategyType.PAY_FOR_CONVERSION
        assert input_data.max_conversion_cost == 1000.0
        assert input_data.goal_id == 9876543

    def test_update_campaign_input_with_pay_for_conversion_crr(self):
        """Test UpdateCampaignInput with PAY_FOR_CONVERSION_CRR strategy."""
        from yandex_mcp.models.direct import UpdateCampaignInput, BiddingStrategyType
        
        input_data = UpdateCampaignInput(
            campaign_id=12345678,
            bidding_strategy_type=BiddingStrategyType.PAY_FOR_CONVERSION_CRR,
            crr_limit=50.0,
            goal_id=9876543
        )
        assert input_data.bidding_strategy_type == BiddingStrategyType.PAY_FOR_CONVERSION_CRR
        assert input_data.crr_limit == 50.0
        assert input_data.goal_id == 9876543

    def test_create_campaign_input_with_average_cpa(self):
        """Test CreateCampaignInput with AVERAGE_CPA strategy."""
        from yandex_mcp.models.direct import CreateCampaignInput, BiddingStrategyType, CampaignType
        
        input_data = CreateCampaignInput(
            name="Test Campaign",
            start_date="2026-03-01",
            campaign_type=CampaignType.TEXT_CAMPAIGN,
            search_strategy_type=BiddingStrategyType.AVERAGE_CPA,
            average_cpa=500.0,
            goal_id=9876543
        )
        assert input_data.name == "Test Campaign"
        assert input_data.search_strategy_type == BiddingStrategyType.AVERAGE_CPA
        assert input_data.average_cpa == 500.0
        assert input_data.goal_id == 9876543

    def test_create_campaign_input_with_average_roi(self):
        """Test CreateCampaignInput with AVERAGE_ROI strategy."""
        from yandex_mcp.models.direct import CreateCampaignInput, BiddingStrategyType, CampaignType
        
        input_data = CreateCampaignInput(
            name="Test ROI Campaign",
            start_date="2026-03-01",
            campaign_type=CampaignType.TEXT_CAMPAIGN,
            search_strategy_type=BiddingStrategyType.AVERAGE_ROI,
            roi_coef=2.0,
            reserve_return=1.0,
            goal_id=9876543
        )
        assert input_data.search_strategy_type == BiddingStrategyType.AVERAGE_ROI
        assert input_data.roi_coef == 2.0
        assert input_data.reserve_return == 1.0

    def test_create_campaign_input_with_pay_for_conversion(self):
        """Test CreateCampaignInput with PAY_FOR_CONVERSION strategy."""
        from yandex_mcp.models.direct import CreateCampaignInput, BiddingStrategyType, CampaignType
        
        input_data = CreateCampaignInput(
            name="Test PFC Campaign",
            start_date="2026-03-01",
            campaign_type=CampaignType.TEXT_CAMPAIGN,
            search_strategy_type=BiddingStrategyType.PAY_FOR_CONVERSION,
            max_conversion_cost=750.0,
            goal_id=9876543
        )
        assert input_data.search_strategy_type == BiddingStrategyType.PAY_FOR_CONVERSION
        assert input_data.max_conversion_cost == 750.0

    def test_create_campaign_input_with_pay_for_conversion_crr(self):
        """Test CreateCampaignInput with PAY_FOR_CONVERSION_CRR strategy."""
        from yandex_mcp.models.direct import CreateCampaignInput, BiddingStrategyType, CampaignType
        
        input_data = CreateCampaignInput(
            name="Test PFC CRR Campaign",
            start_date="2026-03-01",
            campaign_type=CampaignType.TEXT_CAMPAIGN,
            search_strategy_type=BiddingStrategyType.PAY_FOR_CONVERSION_CRR,
            crr_limit=75.0,
            goal_id=9876543
        )
        assert input_data.search_strategy_type == BiddingStrategyType.PAY_FOR_CONVERSION_CRR
        assert input_data.crr_limit == 75.0


class TestLeadFormsModels:
    """Test LeadForms models and enums."""

    def test_question_type_enum(self):
        """Test that all question types are defined."""
        from yandex_mcp.models.direct_extended import QuestionType
        
        assert QuestionType.NAME.value == "NAME"
        assert QuestionType.PHONE.value == "PHONE"
        assert QuestionType.EMAIL.value == "EMAIL"
        assert QuestionType.ADDRESS.value == "ADDRESS"
        assert QuestionType.COMMENT.value == "COMMENT"
        assert QuestionType.CHECKBOX.value == "CHECKBOX"

    def test_lead_form_question_model(self):
        """Test LeadFormQuestion model."""
        from yandex_mcp.models.direct_extended import LeadFormQuestion, QuestionType
        
        question = LeadFormQuestion(
            type=QuestionType.PHONE,
            required=True,
            label="Your phone number"
        )
        assert question.type == QuestionType.PHONE
        assert question.required is True
        assert question.label == "Your phone number"

    def test_add_lead_form_input_model(self):
        """Test AddLeadFormInput model."""
        from yandex_mcp.models.direct_extended import AddLeadFormInput, LeadFormQuestion, QuestionType
        
        questions = [
            LeadFormQuestion(type=QuestionType.NAME, required=True),
            LeadFormQuestion(type=QuestionType.PHONE, required=True),
            LeadFormQuestion(type=QuestionType.EMAIL, required=False),
        ]
        
        input_data = AddLeadFormInput(
            name="Contact Form",
            campaign_id=12345678,
            url="https://example.com/contact",
            policy_url="https://example.com/privacy",
            short_form=False,
            questions=questions
        )
        assert input_data.name == "Contact Form"
        assert input_data.campaign_id == 12345678
        assert input_data.short_form is False
        assert len(input_data.questions) == 3

    def test_update_lead_form_input_model(self):
        """Test UpdateLeadFormInput model."""
        from yandex_mcp.models.direct_extended import UpdateLeadFormInput
        
        input_data = UpdateLeadFormInput(
            form_id=12345,
            name="Updated Form Name",
            url="https://example.com/new-page"
        )
        assert input_data.form_id == 12345
        assert input_data.name == "Updated Form Name"
        assert input_data.url == "https://example.com/new-page"

    def test_get_lead_forms_input_model(self):
        """Test GetLeadFormsInput model."""
        from yandex_mcp.models.direct_extended import GetLeadFormsInput
        
        input_data = GetLeadFormsInput(
            campaign_ids=[12345678, 87654321],
            form_ids=[111, 222],
            limit=50,
            offset=0
        )
        assert input_data.campaign_ids == [12345678, 87654321]
        assert input_data.form_ids == [111, 222]
        assert input_data.limit == 50

    def test_delete_lead_forms_input_model(self):
        """Test DeleteLeadFormsInput model."""
        from yandex_mcp.models.direct_extended import DeleteLeadFormsInput
        
        input_data = DeleteLeadFormsInput(
            form_ids=[111, 222, 333]
        )
        assert input_data.form_ids == [111, 222, 333]


class TestBidModifiersModels:
    """Test BidModifiers models including Video and Retargeting adjustments."""

    def test_video_adjustment_model(self):
        """Test VideoAdjustment model."""
        from yandex_mcp.models.direct_extended import VideoAdjustment
        
        # Test valid bid modifier
        adjustment = VideoAdjustment(bid_modifier=150)
        assert adjustment.bid_modifier == 150
        
        # Test minimum value (0 = disable)
        adjustment_min = VideoAdjustment(bid_modifier=0)
        assert adjustment_min.bid_modifier == 0
        
        # Test maximum value (1300 = 13x)
        adjustment_max = VideoAdjustment(bid_modifier=1300)
        assert adjustment_max.bid_modifier == 1300

    def test_video_adjustment_validation(self):
        """Test VideoAdjustment validation."""
        from yandex_mcp.models.direct_extended import VideoAdjustment
        from pydantic import ValidationError
        
        # Test invalid - too low
        with pytest.raises(ValidationError):
            VideoAdjustment(bid_modifier=-1)
        
        # Test invalid - too high
        with pytest.raises(ValidationError):
            VideoAdjustment(bid_modifier=1301)

    def test_retargeting_adjustment_model(self):
        """Test RetargetingAdjustment model."""
        from yandex_mcp.models.direct_extended import RetargetingAdjustment
        
        # Test with enabled=True (default)
        adjustment = RetargetingAdjustment(
            retargeting_list_id=12345,
            bid_modifier=120
        )
        assert adjustment.retargeting_list_id == 12345
        assert adjustment.bid_modifier == 120
        assert adjustment.enabled is True
        
        # Test with enabled=False
        adjustment_disabled = RetargetingAdjustment(
            retargeting_list_id=67890,
            bid_modifier=100,
            enabled=False
        )
        assert adjustment_disabled.enabled is False

    def test_retargeting_adjustment_validation(self):
        """Test RetargetingAdjustment validation."""
        from yandex_mcp.models.direct_extended import RetargetingAdjustment
        from pydantic import ValidationError
        
        # Test invalid - too low
        with pytest.raises(ValidationError):
            RetargetingAdjustment(retargeting_list_id=123, bid_modifier=-1)
        
        # Test invalid - too high
        with pytest.raises(ValidationError):
            RetargetingAdjustment(retargeting_list_id=123, bid_modifier=1301)

    def test_add_bid_modifier_with_video_adjustment(self):
        """Test AddBidModifierInput with video adjustment."""
        from yandex_mcp.models.direct_extended import AddBidModifierInput, VideoAdjustment
        
        input_data = AddBidModifierInput(
            campaign_id=12345678,
            video_adjustment=VideoAdjustment(bid_modifier=150)
        )
        assert input_data.campaign_id == 12345678
        assert input_data.video_adjustment is not None
        assert input_data.video_adjustment.bid_modifier == 150

    def test_add_bid_modifier_with_retargeting_adjustments(self):
        """Test AddBidModifierInput with retargeting adjustments."""
        from yandex_mcp.models.direct_extended import AddBidModifierInput, RetargetingAdjustment
        
        input_data = AddBidModifierInput(
            campaign_id=12345678,
            retargeting_adjustments=[
                RetargetingAdjustment(retargeting_list_id=111, bid_modifier=120),
                RetargetingAdjustment(retargeting_list_id=222, bid_modifier=80, enabled=False),
            ]
        )
        assert input_data.campaign_id == 12345678
        assert len(input_data.retargeting_adjustments) == 2
        assert input_data.retargeting_adjustments[0].bid_modifier == 120
        assert input_data.retargeting_adjustments[1].enabled is False

    def test_add_bid_modifier_with_all_adjustment_types(self):
        """Test AddBidModifierInput with all adjustment types."""
        from yandex_mcp.models.direct_extended import (
            AddBidModifierInput, MobileAdjustment, DesktopAdjustment,
            DemographicsAdjustment, RegionalAdjustment, VideoAdjustment,
            RetargetingAdjustment
        )
        
        input_data = AddBidModifierInput(
            campaign_id=12345678,
            mobile_adjustment=MobileAdjustment(bid_modifier=120),
            desktop_adjustment=DesktopAdjustment(bid_modifier=100),
            demographics_adjustments=[
                DemographicsAdjustment(gender="GENDER_MALE", age="AGE_25_34", bid_modifier=110)
            ],
            regional_adjustments=[
                RegionalAdjustment(region_id=213, bid_modifier=130)
            ],
            video_adjustment=VideoAdjustment(bid_modifier=150),
            retargeting_adjustments=[
                RetargetingAdjustment(retargeting_list_id=123, bid_modifier=140)
            ]
        )
        
        assert input_data.campaign_id == 12345678
        assert input_data.mobile_adjustment.bid_modifier == 120
        assert input_data.desktop_adjustment.bid_modifier == 100
        assert len(input_data.demographics_adjustments) == 1
        assert len(input_data.regional_adjustments) == 1
        assert input_data.video_adjustment.bid_modifier == 150
        assert len(input_data.retargeting_adjustments) == 1


class TestAgencyClientsModels:
    """Test AgencyClients models."""

    def test_get_agency_clients_input_model(self):
        """Test GetAgencyClientsInput model."""
        from yandex_mcp.models.direct_extended import GetAgencyClientsInput
        
        input_data = GetAgencyClientsInput(
            logins=["client1", "client2"],
            status=["ALLOWED", "SUSPENDED"],
            limit=50,
            offset=0
        )
        assert input_data.logins == ["client1", "client2"]
        assert input_data.status == ["ALLOWED", "SUSPENDED"]
        assert input_data.limit == 50
        assert input_data.offset == 0

    def test_get_agency_clients_input_defaults(self):
        """Test GetAgencyClientsInput with default values."""
        from yandex_mcp.models.direct_extended import GetAgencyClientsInput
        
        input_data = GetAgencyClientsInput()
        assert input_data.logins is None
        assert input_data.status is None
        assert input_data.limit == 100
        assert input_data.offset == 0

    def test_agency_client_settings_model(self):
        """Test AgencyClientSettings model."""
        from yandex_mcp.models.direct_extended import AgencyClientSettings
        
        settings = AgencyClientSettings(
            send_account_warnings=True,
            send_notification_about_warnings=False
        )
        assert settings.send_account_warnings is True
        assert settings.send_notification_about_warnings is False

    def test_agency_client_notification_model(self):
        """Test AgencyClientNotification model."""
        from yandex_mcp.models.direct_extended import AgencyClientNotification
        
        notification = AgencyClientNotification(
            email="client@example.com",
            email_balance=True,
            email_trade_offers=False,
            email_advertising_on_account=True
        )
        assert notification.email == "client@example.com"
        assert notification.email_balance is True
        assert notification.email_trade_offers is False
        assert notification.email_advertising_on_account is True

    def test_update_agency_client_input_model(self):
        """Test UpdateAgencyClientInput model."""
        from yandex_mcp.models.direct_extended import (
            UpdateAgencyClientInput,
            AgencyClientSettings,
            AgencyClientNotification
        )
        
        input_data = UpdateAgencyClientInput(
            login="client_login",
            settings=AgencyClientSettings(
                send_account_warnings=True
            ),
            notification=AgencyClientNotification(
                email="client@example.com",
                email_balance=True
            )
        )
        assert input_data.login == "client_login"
        assert input_data.settings is not None
        assert input_data.settings.send_account_warnings is True
        assert input_data.notification is not None
        assert input_data.notification.email == "client@example.com"

    def test_update_agency_client_input_login_only(self):
        """Test UpdateAgencyClientInput with only login."""
        from yandex_mcp.models.direct_extended import UpdateAgencyClientInput
        
        input_data = UpdateAgencyClientInput(
            login="client_login"
        )
        assert input_data.login == "client_login"
        assert input_data.settings is None
        assert input_data.notification is None


class TestCreativesModels:
    """Test Creatives input models."""

    def test_create_video_extension_creative_input_model(self):
        """Test CreateVideoExtensionCreativeInput model."""
        from yandex_mcp.tools.direct.creatives import CreateVideoExtensionCreativeInput
        
        input_data = CreateVideoExtensionCreativeInput(
            video_id="abc123"
        )
        assert input_data.video_id == "abc123"

    def test_create_cpc_video_creative_input_model(self):
        """Test CreateCPCVideoCreativeInput model."""
        from yandex_mcp.tools.direct.creatives import CreateCPCVideoCreativeInput
        
        # Test with only required fields
        input_data = CreateCPCVideoCreativeInput(
            video_id="abc123"
        )
        assert input_data.video_id == "abc123"
        assert input_data.title is None
        assert input_data.trailer_version is None
        
        # Test with optional fields
        input_data_full = CreateCPCVideoCreativeInput(
            video_id="def456",
            title="My Video Ad",
            trailer_version="FULL"
        )
        assert input_data_full.video_id == "def456"
        assert input_data_full.title == "My Video Ad"
        assert input_data_full.trailer_version == "FULL"

    def test_create_cpm_video_creative_input_model(self):
        """Test CreateCPMVideoCreativeInput model."""
        from yandex_mcp.tools.direct.creatives import CreateCPMVideoCreativeInput
        
        # Test with only required fields
        input_data = CreateCPMVideoCreativeInput(
            video_id="abc123"
        )
        assert input_data.video_id == "abc123"
        assert input_data.title is None
        assert input_data.trailer_version is None
        
        # Test with optional fields
        input_data_full = CreateCPMVideoCreativeInput(
            video_id="ghi789",
            title="Display Video Ad",
            trailer_version="SHORT"
        )
        assert input_data_full.video_id == "ghi789"
        assert input_data_full.title == "Display Video Ad"
        assert input_data_full.trailer_version == "SHORT"

    def test_get_creatives_input_model(self):
        """Test GetCreativesInput model."""
        from yandex_mcp.tools.direct.creatives import GetCreativesInput
        
        # Test with default values
        input_data = GetCreativesInput()
        assert input_data.creative_ids is None
        assert input_data.types is None
        assert input_data.limit == 100
        
        # Test with filters
        input_data_filtered = GetCreativesInput(
            creative_ids=[123, 456],
            types=["CPC_VIDEO_CREATIVE", "CPM_VIDEO_CREATIVE"],
            limit=50
        )
        assert input_data_filtered.creative_ids == [123, 456]
        assert input_data_filtered.types == ["CPC_VIDEO_CREATIVE", "CPM_VIDEO_CREATIVE"]
        assert input_data_filtered.limit == 50


class TestAdVideosModels:
    """Test AdVideos input models."""

    def test_delete_advideos_input_model(self):
        """Test DeleteAdVideosInput model."""
        from yandex_mcp.tools.direct.advideos import DeleteAdVideosInput
        
        input_data = DeleteAdVideosInput(
            video_ids=["abc123", "def456", "ghi789"]
        )
        assert input_data.video_ids == ["abc123", "def456", "ghi789"]
        assert len(input_data.video_ids) == 3

    def test_delete_advideos_input_single_id(self):
        """Test DeleteAdVideosInput with single video ID."""
        from yandex_mcp.tools.direct.advideos import DeleteAdVideosInput
        
        input_data = DeleteAdVideosInput(
            video_ids=["single_video_id"]
        )
        assert input_data.video_ids == ["single_video_id"]
        assert len(input_data.video_ids) == 1


class TestTurboPagesModels:
    """Test TurboPages models."""

    def test_get_turbo_pages_input_model(self):
        """Test GetTurboPagesInput model."""
        from yandex_mcp.models.direct_extended import GetTurboPagesInput
        
        input_data = GetTurboPagesInput(
            turbo_page_ids=[111, 222],
            limit=50,
            offset=10
        )
        assert input_data.turbo_page_ids == [111, 222]
        assert input_data.limit == 50
        assert input_data.offset == 10

    def test_get_turbo_pages_input_defaults(self):
        """Test GetTurboPagesInput with default values."""
        from yandex_mcp.models.direct_extended import GetTurboPagesInput
        
        input_data = GetTurboPagesInput()
        assert input_data.turbo_page_ids is None
        assert input_data.limit == 100
        assert input_data.offset == 0

    def test_turbo_page_input_model(self):
        """Test TurboPageInput model for creating."""
        from yandex_mcp.models.direct_extended import TurboPageInput
        
        input_data = TurboPageInput(
            name="My Turbo Page",
            url="https://example.com"
        )
        assert input_data.name == "My Turbo Page"
        assert input_data.url == "https://example.com"
        assert input_data.turbo_site_id is None

    def test_turbo_page_input_with_turbo_site_id(self):
        """Test TurboPageInput with turbo_site_id."""
        from yandex_mcp.models.direct_extended import TurboPageInput
        
        input_data = TurboPageInput(
            name="My Turbo Page",
            url="https://example.com",
            turbo_site_id=12345
        )
        assert input_data.turbo_site_id == 12345

    def test_turbo_page_input_for_update(self):
        """Test TurboPageInput model for updating."""
        from yandex_mcp.models.direct_extended import TurboPageInput
        
        input_data = TurboPageInput(
            name="Updated Page",
            url="https://example.org",
            turbo_page_ids=[111]
        )
        assert input_data.name == "Updated Page"
        assert input_data.url == "https://example.org"
        assert input_data.turbo_page_ids == [111]

    def test_delete_turbo_pages_input_model(self):
        """Test DeleteTurboPagesInput model."""
        from yandex_mcp.models.direct_extended import DeleteTurboPagesInput
        
        input_data = DeleteTurboPagesInput(
            turbo_page_ids=[111, 222, 333]
        )
        assert input_data.turbo_page_ids == [111, 222, 333]
