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
    # Videos & Creatives (4)
    "direct_upload_video",
    "direct_get_advideos",
    "direct_create_video_creative",
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
