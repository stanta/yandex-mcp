"""Yandex Direct VideoAds tools.

VideoAds is a service for managing video ad campaigns including video ad videos,
video ad groups, and video ads. This is distinct from video extensions (advideos).
"""

import json
from mcp.server.fastmcp import FastMCP

from ...client import api_client
from ...models.common import ResponseFormat
from ...models.direct_extended import (
    GetVideoAdVideosInput,
    AddVideoAdVideosInput,
    GetVideoAdGroupsInput,
    AddVideoAdGroupsInput,
    UpdateVideoAdGroupsInput,
    GetVideoAdsInput,
    AddVideoAdsInput,
)
from ...utils import handle_api_error


def register(mcp: FastMCP) -> None:
    """Register VideoAds tools."""

    # =========================================================================
    # VideoAdVideos - Video files for video ads
    # =========================================================================

    @mcp.tool(
        name="direct_get_video_ad_videos",
        annotations={
            "title": "Get Video Ad Videos from Yandex Direct",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False
        }
    )
    async def direct_get_video_ad_videos(params: GetVideoAdVideosInput) -> str:
        """Get list of video ad videos.

        Retrieves video ad videos with their metadata and status.
        Video ad videos are the video files used in video ad campaigns.
        """
        try:
            selection_criteria = {}

            if params.video_ad_video_ids:
                selection_criteria["Ids"] = params.video_ad_video_ids

            if params.campaign_ids:
                selection_criteria["CampaignIds"] = params.campaign_ids

            request_params = {
                "SelectionCriteria": selection_criteria,
                "FieldNames": [
                    "Id", "Name", "VideoVastUrl", "Status", "Duration",
                    "Width", "Height", "FileSize", "CreatedDate"
                ],
                "Page": {
                    "Limit": params.limit,
                    "Offset": params.offset
                }
            }

            result = await api_client.direct_request("videos", "get", request_params)

            if "error" in result:
                err = result["error"]
                return f"API Error: {err.get('error_code')}: {err.get('error_string')} | {err.get('error_detail', '')}"

            videos = result.get("result", {}).get("VideoAdVideos", [])

            if not videos:
                return "No video ad videos found."

            if params.response_format == ResponseFormat.JSON:
                return json.dumps({"video_ad_videos": videos, "total": len(videos)}, indent=2, ensure_ascii=False)

            lines = ["# Video Ad Videos\n"]
            for v in videos:
                lines.append(f"## {v.get('Name', 'N/A')} (ID: {v.get('Id')})")
                lines.append(f"- **Status**: {v.get('Status', 'N/A')}")
                
                duration = v.get("Duration")
                if duration:
                    lines.append(f"- **Duration**: {duration}s")
                
                width = v.get("Width")
                height = v.get("Height")
                if width and height:
                    lines.append(f"- **Resolution**: {width}x{height}")
                
                file_size = v.get("FileSize")
                if file_size:
                    lines.append(f"- **File Size**: {file_size / 1024 / 1024:.1f} MB")
                
                video_url = v.get("VideoVastUrl")
                if video_url:
                    lines.append(f"- **VAST URL**: {video_url[:80]}...")
                
                created = v.get("CreatedDate")
                if created:
                    lines.append(f"- **Created**: {created}")
                
                lines.append("")

            return "\n".join(lines)

        except Exception as e:
            return handle_api_error(e)

    @mcp.tool(
        name="direct_add_video_ad_videos",
        annotations={
            "title": "Add Video Ad Videos to Yandex Direct",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False
        }
    )
    async def direct_add_video_ad_videos(params: AddVideoAdVideosInput) -> str:
        """Add video ad videos.

        Creates new video ad videos from video URLs.
        The videos will be processed and can be used in video ad campaigns.
        """
        try:
            videos = []
            for video in params.videos:
                video_obj = {
                    "Name": video.name,
                    "VideoUrl": video.video_url
                }
                videos.append(video_obj)

            request_params = {"VideoAdVideos": videos}

            result = await api_client.direct_request("videos", "add", request_params)

            if "error" in result:
                err = result["error"]
                return f"API Error: {err.get('error_code')}: {err.get('error_string')} | {err.get('error_detail', '')}"

            add_results = result.get("result", {}).get("AddResults", [])

            if add_results:
                success_ids = []
                errors_list = []
                
                for r in add_results:
                    if r.get("Id"):
                        success_ids.append(str(r["Id"]))
                    if r.get("Errors"):
                        for e in r["Errors"]:
                            errors_list.append(f"{e.get('Code')}: {e.get('Message')}")

                if success_ids:
                    response = f"Successfully added {len(success_ids)} video ad video(s).\n\n"
                    response += "Video IDs: " + ", ".join(success_ids)
                    response += "\n\nVideos will be processed. Check status with direct_get_video_ad_videos."
                    
                    if errors_list:
                        response += "\n\nWarnings/Errors:\n" + "\n".join(f"- {e}" for e in errors_list)
                    
                    return response
                else:
                    return "Failed to add video ad videos:\n" + "\n".join(f"- {e}" for e in errors_list)

            return "No results returned from API."

        except Exception as e:
            return handle_api_error(e)

    # =========================================================================
    # VideoAdGroups - Ad groups for video ads
    # =========================================================================

    @mcp.tool(
        name="direct_get_video_ad_groups",
        annotations={
            "title": "Get Video Ad Groups from Yandex Direct",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False
        }
    )
    async def direct_get_video_ad_groups(params: GetVideoAdGroupsInput) -> str:
        """Get list of video ad groups.

        Retrieves video ad groups with their settings and status.
        Video ad groups contain video ads and define targeting.
        """
        try:
            selection_criteria = {}

            if params.video_ad_group_ids:
                selection_criteria["Ids"] = params.video_ad_group_ids

            if params.campaign_ids:
                selection_criteria["CampaignIds"] = params.campaign_ids

            request_params = {
                "SelectionCriteria": selection_criteria,
                "FieldNames": [
                    "Id", "Name", "CampaignId", "RegionIds", "Status",
                    "ServingStatus", "Type"
                ],
                "Page": {
                    "Limit": params.limit,
                    "Offset": params.offset
                }
            }

            result = await api_client.direct_request("videos", "get", request_params)

            if "error" in result:
                err = result["error"]
                return f"API Error: {err.get('error_code')}: {err.get('error_string')} | {err.get('error_detail', '')}"

            # The API uses VideoAdGroups for the response
            groups = result.get("result", {}).get("VideoAdGroups", [])

            if not groups:
                return "No video ad groups found."

            if params.response_format == ResponseFormat.JSON:
                return json.dumps({"video_ad_groups": groups, "total": len(groups)}, indent=2, ensure_ascii=False)

            lines = ["# Video Ad Groups\n"]
            for g in groups:
                lines.append(f"## {g.get('Name', 'N/A')} (ID: {g.get('Id')})")
                lines.append(f"- **Campaign ID**: {g.get('CampaignId', 'N/A')}")
                lines.append(f"- **Status**: {g.get('Status', 'N/A')}")
                lines.append(f"- **Serving Status**: {g.get('ServingStatus', 'N/A')}")
                lines.append(f"- **Type**: {g.get('Type', 'N/A')}")
                
                region_ids = g.get("RegionIds", [])
                if region_ids:
                    lines.append(f"- **Region IDs**: {', '.join(str(r) for r in region_ids[:5])}")
                    if len(region_ids) > 5:
                        lines.append(f"  ... and {len(region_ids) - 5} more")
                
                lines.append("")

            return "\n".join(lines)

        except Exception as e:
            return handle_api_error(e)

    @mcp.tool(
        name="direct_add_video_ad_groups",
        annotations={
            "title": "Add Video Ad Groups to Yandex Direct",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False
        }
    )
    async def direct_add_video_ad_groups(params: AddVideoAdGroupsInput) -> str:
        """Add video ad groups.

        Creates new video ad groups in a video ad campaign.
        """
        try:
            ad_groups = []
            for ag in params.ad_groups:
                group_obj = {
                    "CampaignId": ag.campaign_id,
                    "Name": ag.name
                }
                
                if ag.region_ids:
                    group_obj["RegionIds"] = ag.region_ids
                
                ad_groups.append(group_obj)

            request_params = {"VideoAdGroups": ad_groups}

            result = await api_client.direct_request("videos", "add", request_params)

            if "error" in result:
                err = result["error"]
                return f"API Error: {err.get('error_code')}: {err.get('error_string')} | {err.get('error_detail', '')}"

            add_results = result.get("result", {}).get("AddResults", [])

            if add_results:
                success_ids = []
                errors_list = []
                
                for r in add_results:
                    if r.get("Id"):
                        success_ids.append(str(r["Id"]))
                    if r.get("Errors"):
                        for e in r["Errors"]:
                            errors_list.append(f"{e.get('Code')}: {e.get('Message')}")

                if success_ids:
                    response = f"Successfully added {len(success_ids)} video ad group(s).\n\n"
                    response += "Video Ad Group IDs: " + ", ".join(success_ids)
                    
                    if errors_list:
                        response += "\n\nWarnings/Errors:\n" + "\n".join(f"- {e}" for e in errors_list)
                    
                    return response
                else:
                    return "Failed to add video ad groups:\n" + "\n".join(f"- {e}" for e in errors_list)

            return "No results returned from API."

        except Exception as e:
            return handle_api_error(e)

    @mcp.tool(
        name="direct_update_video_ad_groups",
        annotations={
            "title": "Update Video Ad Groups in Yandex Direct",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False
        }
    )
    async def direct_update_video_ad_groups(params: UpdateVideoAdGroupsInput) -> str:
        """Update video ad groups.

        Updates settings for existing video ad groups.
        """
        try:
            ad_groups = []
            for ag in params.ad_groups:
                group_obj = {
                    "Id": ag.video_ad_group_id
                }
                
                if ag.name is not None:
                    group_obj["Name"] = ag.name
                
                if ag.region_ids is not None:
                    group_obj["RegionIds"] = ag.region_ids
                
                ad_groups.append(group_obj)

            request_params = {"VideoAdGroups": ad_groups}

            result = await api_client.direct_request("videos", "update", request_params)

            if "error" in result:
                err = result["error"]
                return f"API Error: {err.get('error_code')}: {err.get('error_string')} | {err.get('error_detail', '')}"

            update_results = result.get("result", {}).get("UpdateResults", [])

            if update_results:
                success_count = 0
                errors_list = []
                
                for r in update_results:
                    if r.get("Id") and not r.get("Errors"):
                        success_count += 1
                    if r.get("Errors"):
                        for e in r["Errors"]:
                            errors_list.append(f"ID {r.get('Id', '?')}: {e.get('Message')}")

                response = f"Successfully updated {success_count} video ad group(s)."
                
                if errors_list:
                    response += "\n\nErrors:\n" + "\n".join(f"- {e}" for e in errors_list)
                
                return response

            return "No results returned from API."

        except Exception as e:
            return handle_api_error(e)

    # =========================================================================
    # VideoAds - The actual video advertisements
    # =========================================================================

    @mcp.tool(
        name="direct_get_video_ads",
        annotations={
            "title": "Get Video Ads from Yandex Direct",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False
        }
    )
    async def direct_get_video_ads(params: GetVideoAdsInput) -> str:
        """Get list of video ads.

        Retrieves video ads with their settings and status.
        Video ads are the actual advertisements shown in video ad campaigns.
        """
        try:
            selection_criteria = {}

            if params.video_ad_ids:
                selection_criteria["Ids"] = params.video_ad_ids

            if params.campaign_ids:
                selection_criteria["CampaignIds"] = params.campaign_ids

            if params.ad_group_ids:
                selection_criteria["AdGroupIds"] = params.ad_group_ids

            request_params = {
                "SelectionCriteria": selection_criteria,
                "FieldNames": [
                    "Id", "AdGroupId", "VideoAdGroupId", "VideoAdVideoId",
                    "Status", "ModerationStatus", "Title", "LinkUrl", "DisplayUrl"
                ],
                "Page": {
                    "Limit": params.limit,
                    "Offset": params.offset
                }
            }

            result = await api_client.direct_request("videos", "get", request_params)

            if "error" in result:
                err = result["error"]
                return f"API Error: {err.get('error_code')}: {err.get('error_string')} | {err.get('error_detail', '')}"

            ads = result.get("result", {}).get("VideoAds", [])

            if not ads:
                return "No video ads found."

            if params.response_format == ResponseFormat.JSON:
                return json.dumps({"video_ads": ads, "total": len(ads)}, indent=2, ensure_ascii=False)

            lines = ["# Video Ads\n"]
            for ad in ads:
                lines.append(f"## Ad ID: {ad.get('Id')}")
                
                title = ad.get("Title")
                if title:
                    lines.append(f"- **Title**: {title}")
                
                lines.append(f"- **Video Ad Group ID**: {ad.get('VideoAdGroupId', 'N/A')}")
                lines.append(f"- **Video Ad Video ID**: {ad.get('VideoAdVideoId', 'N/A')}")
                lines.append(f"- **Status**: {ad.get('Status', 'N/A')}")
                lines.append(f"- **Moderation**: {ad.get('ModerationStatus', 'N/A')}")
                
                link_url = ad.get("LinkUrl")
                if link_url:
                    lines.append(f"- **Link URL**: {link_url[:80]}...")
                
                display_url = ad.get("DisplayUrl")
                if display_url:
                    lines.append(f"- **Display URL**: {display_url}")
                
                lines.append("")

            return "\n".join(lines)

        except Exception as e:
            return handle_api_error(e)

    @mcp.tool(
        name="direct_add_video_ads",
        annotations={
            "title": "Add Video Ads to Yandex Direct",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False
        }
    )
    async def direct_add_video_ads(params: AddVideoAdsInput) -> str:
        """Add video ads.

        Creates new video ads in video ad groups.
        """
        try:
            ads = []
            for ad in params.ads:
                ad_obj = {
                    "VideoAdGroupId": ad.video_ad_group_id,
                    "VideoAdVideoId": ad.video_ad_video_id,
                    "Title": ad.title,
                    "LinkUrl": ad.link_url
                }
                
                if ad.display_url:
                    ad_obj["DisplayUrl"] = ad.display_url
                
                if ad.vcard_id:
                    ad_obj["VCardId"] = ad.vcard_id
                
                if ad.href_param:
                    ad_obj["HrefParam"] = ad.href_param
                
                ads.append(ad_obj)

            request_params = {"VideoAds": ads}

            result = await api_client.direct_request("videos", "add", request_params)

            if "error" in result:
                err = result["error"]
                return f"API Error: {err.get('error_code')}: {err.get('error_string')} | {err.get('error_detail', '')}"

            add_results = result.get("result", {}).get("AddResults", [])

            if add_results:
                success_ids = []
                errors_list = []
                
                for r in add_results:
                    if r.get("Id"):
                        success_ids.append(str(r["Id"]))
                    if r.get("Errors"):
                        for e in r["Errors"]:
                            errors_list.append(f"{e.get('Code')}: {e.get('Message')}")

                if success_ids:
                    response = f"Successfully added {len(success_ids)} video ad(s).\n\n"
                    response += "Video Ad IDs: " + ", ".join(success_ids)
                    response += "\n\nAds will be submitted for moderation."
                    
                    if errors_list:
                        response += "\n\nWarnings/Errors:\n" + "\n".join(f"- {e}" for e in errors_list)
                    
                    return response
                else:
                    return "Failed to add video ads:\n" + "\n".join(f"- {e}" for e in errors_list)

            return "No results returned from API."

        except Exception as e:
            return handle_api_error(e)
