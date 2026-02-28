"""Yandex Direct dynamic text ad targets (autotargeting) tools."""

import json
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

from ...client import api_client
from ...utils import handle_api_error
from ._helpers import register_manage_tool


class GetDynamicTextAdTargetsInput(BaseModel):
    """Input for getting dynamic text ad targets."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    campaign_ids: Optional[List[int]] = Field(default=None, description="Filter by campaign IDs")
    adgroup_ids: Optional[List[int]] = Field(default=None, description="Filter by ad group IDs")
    target_ids: Optional[List[int]] = Field(default=None, description="Filter by target IDs")
    limit: int = Field(default=100, ge=1, le=10000)


class DynamicTextAdTargetCondition(BaseModel):
    """A single filter condition for dynamic text ad targeting."""
    operand: str = Field(..., description="Feed field name (e.g., 'price', 'manufacturer', 'category_id', 'url', 'title')")
    operator: str = Field(..., description="Operator: EQUALS_ANY, CONTAINS_ANY, NOT_CONTAINS_ALL, GREATER_THAN, LESS_THAN, IN_RANGE, EXISTS")
    arguments: List[str] = Field(..., description="Values to match (max 50). For IN_RANGE use 'min-max' format.")


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
    """Input for managing dynamic text ad targets."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    target_ids: List[int] = Field(..., min_length=1, description="Dynamic text ad target IDs")


def register(mcp: FastMCP) -> None:
    """Register dynamic text ad target tools."""

    @mcp.tool(
        name="direct_add_dynamic_text_ad_target",
        annotations={
            "title": "Add Dynamic Text Ad Target",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False
        }
    )
    async def direct_add_dynamic_text_ad_target(params: AddDynamicTextAdTargetInput) -> str:
        """Add an autotargeting filter to a dynamic text ad group.

        Defines which product offers from the feed are used to generate dynamic text ads.
        Without conditions, ALL feed items are used.
        With conditions, only matching items are shown.
        """
        try:
            target = {
                "AdGroupId": params.adgroup_id,
                "Name": params.name,
                "AutoBudget": "YES" if params.auto_budget else "NO"
            }

            if not params.auto_budget and params.bid:
                target["Bid"] = params.bid

            if params.conditions:
                target["Conditions"] = [
                    {
                        "Operand": c.operand,
                        "Operator": c.operator,
                        "Arguments": c.arguments
                    }
                    for c in params.conditions
                ]

            request_params = {"DynamicTextAdTargets": [target]}

            result = await api_client.direct_request("dynamictextadtargets", "add", request_params)

            if "error" in result:
                err = result["error"]
                return f"API Error: {err.get('error_code')}: {err.get('error_string')} | {err.get('error_detail', '')}"

            add_results = result.get("result", {}).get("AddResults", [])

            if add_results and add_results[0].get("Id"):
                target_id = add_results[0]["Id"]
                return f"Dynamic text ad target created successfully!\nTarget ID: {target_id}\nName: {params.name}\nGroup: {params.adgroup_id}"

            errors = []
            for r in add_results:
                if r.get("Errors"):
                    errors.extend([f"{e.get('Code')}: {e.get('Message')} | {e.get('Details', '')}" for e in r["Errors"]])

            return f"Failed to create dynamic text ad target:\n" + "\n".join(f"- {e}" for e in errors)

        except Exception as e:
            return handle_api_error(e)

    @mcp.tool(
        name="direct_get_dynamic_text_ad_targets",
        annotations={
            "title": "Get Dynamic Text Ad Targets",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False
        }
    )
    async def direct_get_dynamic_text_ad_targets(params: GetDynamicTextAdTargetsInput) -> str:
        """Get dynamic text ad targets (autotargeting) and their conditions."""
        try:
            selection_criteria = {}
            if params.campaign_ids:
                selection_criteria["CampaignIds"] = params.campaign_ids
            if params.adgroup_ids:
                selection_criteria["AdGroupIds"] = params.adgroup_ids
            if params.target_ids:
                selection_criteria["Ids"] = params.target_ids

            request_params = {
                "SelectionCriteria": selection_criteria,
                "FieldNames": [
                    "Id", "AdGroupId", "CampaignId", "Name",
                    "State", "Status", "AutoBudget", "Bid", "AverageCpc"
                ],
                "Page": {"Limit": params.limit}
            }

            result = await api_client.direct_request("dynamictextadtargets", "get", request_params)

            if "error" in result:
                err = result["error"]
                return f"API Error: {err.get('error_code')}: {err.get('error_string')} | {err.get('error_detail', '')}"

            targets = result.get("result", {}).get("DynamicTextAdTargets", [])

            if not targets:
                return "No dynamic text ad targets found."

            lines = ["# Dynamic Text Ad Targets (Autotargeting)\n"]
            for t in targets:
                lines.append(f"## {t.get('Name', 'N/A')} (ID: {t.get('Id')})")
                lines.append(f"- **AdGroup**: {t.get('AdGroupId')}")
                lines.append(f"- **Campaign**: {t.get('CampaignId')}")
                lines.append(f"- **State**: {t.get('State')}")
                lines.append(f"- **Status**: {t.get('Status')}")
                lines.append(f"- **Auto Budget**: {t.get('AutoBudget')}")
                if t.get("Bid"):
                    lines.append(f"- **Bid**: {t.get('Bid')}")
                if t.get("AverageCpc"):
                    lines.append(f"- **Avg CPC**: {t.get('AverageCpc')}")
                conditions = t.get("Conditions", [])
                if conditions:
                    lines.append("- **Conditions**:")
                    for c in conditions:
                        lines.append(f"  - {c.get('Operand')} {c.get('Operator')} {c.get('Arguments')}")
                lines.append("")

            return "\n".join(lines)

        except Exception as e:
            return handle_api_error(e)

    @mcp.tool(
        name="direct_update_dynamic_text_ad_target",
        annotations={
            "title": "Update Dynamic Text Ad Target",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False
        }
    )
    async def direct_update_dynamic_text_ad_target(params: UpdateDynamicTextAdTargetInput) -> str:
        """Update a dynamic text ad target's settings and conditions."""
        try:
            target = {
                "Id": params.target_id
            }

            if params.name is not None:
                target["Name"] = params.name
            if params.auto_budget is not None:
                target["AutoBudget"] = "YES" if params.auto_budget else "NO"
            if params.bid is not None:
                target["Bid"] = params.bid
            if params.conditions is not None:
                target["Conditions"] = [
                    {
                        "Operand": c.operand,
                        "Operator": c.operator,
                        "Arguments": c.arguments
                    }
                    for c in params.conditions
                ]

            request_params = {"DynamicTextAdTargets": [target]}

            result = await api_client.direct_request("dynamictextadtargets", "update", request_params)

            if "error" in result:
                err = result["error"]
                return f"API Error: {err.get('error_code')}: {err.get('error_string')} | {err.get('error_detail', '')}"

            update_results = result.get("result", {}).get("UpdateResults", [])

            if update_results and update_results[0].get("Id"):
                return f"Dynamic text ad target updated successfully!\nTarget ID: {params.target_id}"

            errors = []
            for r in update_results:
                if r.get("Errors"):
                    errors.extend([f"{e.get('Code')}: {e.get('Message')} | {e.get('Details', '')}" for e in r["Errors"]])

            return f"Failed to update dynamic text ad target:\n" + "\n".join(f"- {e}" for e in errors)

        except Exception as e:
            return handle_api_error(e)

    for action in ("suspend", "resume", "delete"):
        register_manage_tool(
            mcp,
            service="dynamictextadtargets",
            action=action,
            entity="dynamic text ad target",
            input_model=ManageDynamicTextAdTargetsInput,
            ids_field="target_ids",
            tool_name=f"direct_{action}_dynamic_text_ad_targets",
            tool_title=f"{action.capitalize()} Dynamic Text Ad Targets",
        )
