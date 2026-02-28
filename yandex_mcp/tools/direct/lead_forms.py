"""Yandex Direct lead forms tools.

Lead forms are used for lead generation campaigns.
Requires v501 API endpoint.
"""

import json
from mcp.server.fastmcp import FastMCP
from typing import Optional, List

from ...client import api_client
from ...models.common import ResponseFormat
from ...models.direct_extended import (
    GetLeadFormsInput,
    AddLeadFormInput,
    UpdateLeadFormInput,
    DeleteLeadFormsInput,
    GetLeadFormLeadsInput,
)
from ...utils import handle_api_error


def register(mcp: FastMCP) -> None:
    """Register lead form tools."""

    @mcp.tool(
        name="direct_get_lead_forms",
        annotations={
            "title": "Get Lead Forms from Yandex Direct",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False
        }
    )
    async def direct_get_lead_forms(params: GetLeadFormsInput) -> str:
        """Get lead forms with optional filtering by campaign, ad group, or form IDs.

        Returns form details including name, URL, questions, and status.
        Requires v501 API endpoint.
        """
        try:
            selection_criteria = {}

            if params.campaign_ids:
                selection_criteria["CampaignIds"] = params.campaign_ids
            if params.adgroup_ids:
                selection_criteria["AdGroupIds"] = params.adgroup_ids
            if params.form_ids:
                selection_criteria["Ids"] = params.form_ids

            request_params = {
                "SelectionCriteria": selection_criteria,
                "FieldNames": [
                    "Id", "Name", "CampaignId", "AdGroupId", "Url",
                    "PolicyUrl", "ShortForm", "Status", "Statistics"
                ],
                "QuestionsFieldNames": ["Type", "Required", "Label"],
                "Page": {
                    "Limit": params.limit,
                    "Offset": params.offset
                }
            }

            result = await api_client.direct_request(
                "leadforms", "get", request_params, use_v501=True
            )

            if "error" in result:
                err = result["error"]
                return f"API Error: {err.get('error_code')}: {err.get('error_string')} | {err.get('error_detail', '')}"

            forms = result.get("result", {}).get("LeadForms", [])

            if params.response_format == ResponseFormat.JSON:
                return json.dumps({"forms": forms, "total": len(forms)}, indent=2, ensure_ascii=False)

            if not forms:
                return "No lead forms found."

            lines = ["# Lead Forms\n"]
            for f in forms:
                lines.append(f"## {f.get('Name', 'N/A')} (ID: {f.get('Id')})")
                lines.append(f"- **Campaign ID**: {f.get('CampaignId', 'N/A')}")
                lines.append(f"- **Ad Group ID**: {f.get('AdGroupId', 'N/A')}")
                lines.append(f"- **Status**: {f.get('Status', 'N/A')}")
                lines.append(f"- **Short Form**: {'Yes' if f.get('ShortForm') else 'No'}")
                lines.append(f"- **URL**: {f.get('Url', 'N/A')}")
                lines.append(f"- **Policy URL**: {f.get('PolicyUrl', 'N/A')}")

                # Questions
                questions = f.get("Questions", [])
                if questions:
                    lines.append("- **Questions:**")
                    for q in questions:
                        req = " (required)" if q.get("Required") else ""
                        label = f" - {q.get('Label')}" if q.get("Label") else ""
                        lines.append(f"  - {q.get('Type')}{req}{label}")

                # Statistics
                stats = f.get("Statistics", {})
                if stats:
                    lines.append(f"- **Leads**: {stats.get('LeadsCount', 0)}")
                    lines.append(f"- **Views**: {stats.get('ViewsCount', 0)}")

                lines.append("")

            return "\n".join(lines)

        except Exception as e:
            return handle_api_error(e)

    @mcp.tool(
        name="direct_add_lead_form",
        annotations={
            "title": "Add Lead Form to Yandex Direct",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False
        }
    )
    async def direct_add_lead_form(params: AddLeadFormInput) -> str:
        """Create a new lead form for lead generation campaigns.

        Supports custom questions: NAME, PHONE, EMAIL, ADDRESS, COMMENT, CHECKBOX.
        Requires v501 API endpoint.
        """
        try:
            lead_form = {
                "Name": params.name,
                "CampaignId": params.campaign_id,
                "Url": params.url,
                "PolicyUrl": params.policy_url,
                "ShortForm": "YES" if params.short_form else "NO"
            }

            if params.questions:
                lead_form["Questions"] = [
                    {
                        "Type": q.type.value,
                        "Required": "YES" if q.required else "NO",
                        "Label": q.label
                    }
                    for q in params.questions
                ]

            request_params = {"LeadForms": [lead_form]}

            result = await api_client.direct_request(
                "leadforms", "add", request_params, use_v501=True
            )

            if "error" in result:
                err = result["error"]
                return f"API Error: {err.get('error_code')}: {err.get('error_string')} | {err.get('error_detail', '')}"

            add_results = result.get("result", {}).get("AddResults", [])

            if add_results and add_results[0].get("Id"):
                form_id = add_results[0]["Id"]
                return (
                    f"Lead form created successfully!\n"
                    f"Form ID: {form_id}\n"
                    f"Name: {params.name}\n"
                    f"Campaign ID: {params.campaign_id}\n"
                    f"URL: {params.url}\n"
                    f"Short Form: {'Yes' if params.short_form else 'No'}\n\n"
                    f"Add this form to your ad group to start collecting leads."
                )

            errors = []
            for r in add_results:
                if r.get("Errors"):
                    errors.extend([
                        f"{e.get('Code')}: {e.get('Message')} | {e.get('Details', '')}"
                        for e in r["Errors"]
                    ])

            return f"Failed to create lead form:\n" + "\n".join(f"- {e}" for e in errors)

        except Exception as e:
            return handle_api_error(e)

    @mcp.tool(
        name="direct_update_lead_form",
        annotations={
            "title": "Update Lead Form in Yandex Direct",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False
        }
    )
    async def direct_update_lead_form(params: UpdateLeadFormInput) -> str:
        """Update an existing lead form (name, URL, questions, policy).

        Requires v501 API endpoint.
        """
        try:
            lead_form_update = {"Id": params.form_id}

            if params.name:
                lead_form_update["Name"] = params.name
            if params.url:
                lead_form_update["Url"] = params.url
            if params.policy_url:
                lead_form_update["PolicyUrl"] = params.policy_url
            if params.short_form is not None:
                lead_form_update["ShortForm"] = "YES" if params.short_form else "NO"
            if params.questions:
                lead_form_update["Questions"] = [
                    {
                        "Type": q.type.value,
                        "Required": "YES" if q.required else "NO",
                        "Label": q.label
                    }
                    for q in params.questions
                ]

            if len(lead_form_update) <= 1:
                return "No fields specified for update."

            request_params = {"LeadForms": [lead_form_update]}

            result = await api_client.direct_request(
                "leadforms", "update", request_params, use_v501=True
            )

            if "error" in result:
                err = result["error"]
                return f"API Error: {err.get('error_code')}: {err.get('error_string')} | {err.get('error_detail', '')}"

            update_results = result.get("result", {}).get("UpdateResults", [])

            errors = []
            for r in update_results:
                if r.get("Errors"):
                    errors.extend([
                        f"{e.get('Code')}: {e.get('Message')} | {e.get('Details', '')}"
                        for e in r["Errors"]
                    ])

            if errors:
                return f"Update completed with issues:\n" + "\n".join(f"- {e}" for e in errors)

            return f"Lead form {params.form_id} updated successfully."

        except Exception as e:
            return handle_api_error(e)

    @mcp.tool(
        name="direct_delete_lead_forms",
        annotations={
            "title": "Delete Lead Forms from Yandex Direct",
            "readOnlyHint": False,
            "destructiveHint": True,
            "idempotentHint": False,
            "openWorldHint": False
        }
    )
    async def direct_delete_lead_forms(params: DeleteLeadFormsInput) -> str:
        """Delete lead forms permanently. WARNING: Irreversible.

        Requires v501 API endpoint.
        """
        try:
            request_params = {
                "SelectionCriteria": {"Ids": params.form_ids}
            }

            result = await api_client.direct_request(
                "leadforms", "delete", request_params, use_v501=True
            )

            if "error" in result:
                err = result["error"]
                return f"API Error: {err.get('error_code')}: {err.get('error_string')} | {err.get('error_detail', '')}"

            delete_results = result.get("result", {}).get("DeleteResults", [])

            success = [r["Id"] for r in delete_results if r.get("Id") and not r.get("Errors")]
            errors = []
            for r in delete_results:
                if r.get("Errors"):
                    errors.extend([
                        f"ID {r.get('Id', '?')}: {e.get('Message')}"
                        for e in r["Errors"]
                    ])

            response = f"Successfully deleted {len(success)} lead form(s)."
            if errors:
                response += f"\n\nErrors:\n" + "\n".join(f"- {e}" for e in errors)

            return response

        except Exception as e:
            return handle_api_error(e)

    @mcp.tool(
        name="direct_get_lead_form_leads",
        annotations={
            "title": "Get Leads from Lead Forms in Yandex Direct",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False
        }
    )
    async def direct_get_lead_form_leads(params: GetLeadFormLeadsInput) -> str:
        """Get submissions/leads from lead forms.

        Returns lead data including contact information submitted by users.
        Requires v501 API endpoint.
        """
        try:
            selection_criteria = {}

            if params.form_ids:
                selection_criteria["LeadFormIds"] = params.form_ids

            request_params = {
                "SelectionCriteria": selection_criteria,
                "FieldNames": [
                    "Id", "LeadFormId", "CreationDate", "Status",
                    "Name", "Phone", "Email", "Address", "Comment", "Checkbox"
                ],
                "Page": {
                    "Limit": params.limit,
                    "Offset": params.offset
                }
            }

            result = await api_client.direct_request(
                "leadforms", "getleads", request_params, use_v501=True
            )

            if "error" in result:
                err = result["error"]
                return f"API Error: {err.get('error_code')}: {err.get('error_string')} | {err.get('error_detail', '')}"

            leads = result.get("result", {}).get("Leads", [])

            if params.response_format == ResponseFormat.JSON:
                return json.dumps({"leads": leads, "total": len(leads)}, indent=2, ensure_ascii=False)

            if not leads:
                return "No leads found."

            lines = ["# Lead Form Leads\n"]
            for lead in leads:
                lines.append(f"## Lead ID: {lead.get('Id')}")
                lines.append(f"- **Form ID**: {lead.get('LeadFormId', 'N/A')}")
                lines.append(f"- **Status**: {lead.get('Status', 'N/A')}")
                lines.append(f"- **Created**: {lead.get('CreationDate', 'N/A')}")

                # Contact fields
                if lead.get("Name"):
                    lines.append(f"- **Name**: {lead['Name']}")
                if lead.get("Phone"):
                    lines.append(f"- **Phone**: {lead['Phone']}")
                if lead.get("Email"):
                    lines.append(f"- **Email**: {lead['Email']}")
                if lead.get("Address"):
                    lines.append(f"- **Address**: {lead['Address']}")
                if lead.get("Comment"):
                    lines.append(f"- **Comment**: {lead['Comment']}")
                if lead.get("Checkbox"):
                    lines.append(f"- **Checkbox**: {lead['Checkbox']}")

                lines.append("")

            return "\n".join(lines)

        except Exception as e:
            return handle_api_error(e)
