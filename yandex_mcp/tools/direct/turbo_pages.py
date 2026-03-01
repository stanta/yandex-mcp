"""Yandex Direct TurboPages tools.

TurboPages are simplified fast-loading mobile landing pages for advertising.
"""

import json
from mcp.server.fastmcp import FastMCP

from ...client import api_client
from ...models.common import ResponseFormat
from ...models.direct_extended import (
    GetTurboPagesInput,
    TurboPageInput,
    DeleteTurboPagesInput,
)
from ...utils import handle_api_error


def register(mcp: FastMCP) -> None:
    """Register TurboPages tools."""

    @mcp.tool(
        name="direct_get_turbo_pages",
        annotations={
            "title": "Get Turbo Pages from Yandex Direct",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False
        }
    )
    async def direct_get_turbo_pages(params: GetTurboPagesInput) -> str:
        """Get list of Turbo pages.

        Retrieves Turbo pages with their settings, URLs, and status.
        Turbo pages are fast-loading mobile landing pages used in Yandex advertising.
        """
        try:
            selection_criteria = {}

            if params.turbo_page_ids:
                selection_criteria["Ids"] = params.turbo_page_ids

            request_params = {
                "SelectionCriteria": selection_criteria,
                "FieldNames": [
                    "Id", "Name", "Domain", "TurboSiteId", "Status",
                    "IsEenabled", "CreatedAt", "ModifiedAt"
                ],
                "Page": {
                    "Limit": params.limit,
                    "Offset": params.offset
                }
            }

            result = await api_client.direct_request("turbo-pages", "get", request_params)

            if "error" in result:
                err = result["error"]
                return f"API Error: {err.get('error_code')}: {err.get('error_string')} | {err.get('error_detail', '')}"

            turbo_pages = result.get("result", {}).get("TurboPages", [])

            if not turbo_pages:
                return "No Turbo pages found."

            if params.response_format == ResponseFormat.JSON:
                return json.dumps({"turbo_pages": turbo_pages, "total": len(turbo_pages)}, indent=2, ensure_ascii=False)

            lines = ["# Turbo Pages\n"]
            for tp in turbo_pages:
                lines.append(f"## {tp.get('Name', 'N/A')} (ID: {tp.get('Id')})")
                lines.append(f"- **Domain**: {tp.get('Domain', 'N/A')}")
                lines.append(f"- **Turbo Site ID**: {tp.get('TurboSiteId', 'N/A')}")
                lines.append(f"- **Status**: {tp.get('Status', 'N/A')}")
                enabled = tp.get("IsEnabled")
                if enabled is not None:
                    lines.append(f"- **Enabled**: {'Yes' if enabled else 'No'}")
                created = tp.get("CreatedAt")
                if created:
                    lines.append(f"- **Created**: {created}")
                modified = tp.get("ModifiedAt")
                if modified:
                    lines.append(f"- **Modified**: {modified}")
                lines.append("")

            return "\n".join(lines)

        except Exception as e:
            return handle_api_error(e)

    @mcp.tool(
        name="direct_add_turbo_page",
        annotations={
            "title": "Add Turbo Page to Yandex Direct",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False
        }
    )
    async def direct_add_turbo_page(params: TurboPageInput) -> str:
        """Create a new Turbo page.

        Creates a fast-loading mobile landing page based on an existing website.
        The Turbo page will be generated from the source URL.
        """
        try:
            turbo_page = {
                "Name": params.name,
                "Domain": params.url
            }

            if params.turbo_site_id:
                turbo_page["TurboSiteId"] = params.turbo_site_id

            request_params = {"TurboPages": [turbo_page]}

            result = await api_client.direct_request("turbo-pages", "add", request_params)

            if "error" in result:
                err = result["error"]
                return f"API Error: {err.get('error_code')}: {err.get('error_string')} | {err.get('error_detail', '')}"

            add_results = result.get("result", {}).get("AddResults", [])

            if add_results and add_results[0].get("Id"):
                turbo_page_id = add_results[0]["Id"]
                return f"Turbo page added successfully!\n\n**ID**: {turbo_page_id}\n**Name**: {params.name}\n**Source URL**: {params.url}\n\nThe Turbo page will be generated. Check status with direct_get_turbo_pages."

            errors = []
            for r in add_results:
                if r.get("Errors"):
                    errors.extend([f"{e.get('Code')}: {e.get('Message')} | {e.get('Details', '')}" for e in r["Errors"]])

            return f"Failed to add Turbo page:\n" + "\n".join(f"- {e}" for e in errors)

        except Exception as e:
            return handle_api_error(e)

    @mcp.tool(
        name="direct_update_turbo_page",
        annotations={
            "title": "Update Turbo Page in Yandex Direct",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False
        }
    )
    async def direct_update_turbo_page(params: TurboPageInput) -> str:
        """Update an existing Turbo page.

        Allows updating the name and URL of a Turbo page.
        """
        try:
            if not params.turbo_page_ids or len(params.turbo_page_ids) == 0:
                return "Error: turbo_page_ids is required for update."

            turbo_page_update = {
                "Id": params.turbo_page_ids[0],
                "Name": params.name,
                "Domain": params.url
            }

            if params.turbo_site_id:
                turbo_page_update["TurboSiteId"] = params.turbo_site_id

            request_params = {"TurboPages": [turbo_page_update]}

            result = await api_client.direct_request("turbo-pages", "update", request_params)

            if "error" in result:
                err = result["error"]
                return f"API Error: {err.get('error_code')}: {err.get('error_string')} | {err.get('error_detail', '')}"

            update_results = result.get("result", {}).get("UpdateResults", [])

            errors = []
            for r in update_results:
                if r.get("Errors"):
                    errors.extend([f"{e.get('Code')}: {e.get('Message')} | {e.get('Details', '')}" for e in r["Errors"]])

            if errors:
                return f"Update failed:\n" + "\n".join(f"- {e}" for e in errors)

            return f"Turbo page updated successfully."

        except Exception as e:
            return handle_api_error(e)

    @mcp.tool(
        name="direct_delete_turbo_pages",
        annotations={
            "title": "Delete Turbo Pages from Yandex Direct",
            "readOnlyHint": False,
            "destructiveHint": True,
            "idempotentHint": False,
            "openWorldHint": False
        }
    )
    async def direct_delete_turbo_pages(params: DeleteTurboPagesInput) -> str:
        """Delete Turbo pages permanently.

        WARNING: This action is irreversible. The Turbo pages will be removed
        and cannot be recovered.
        """
        try:
            request_params = {
                "SelectionCriteria": {"Ids": params.turbo_page_ids}
            }

            result = await api_client.direct_request("turbo-pages", "delete", request_params)

            if "error" in result:
                err = result["error"]
                return f"API Error: {err.get('error_code')}: {err.get('error_string')} | {err.get('error_detail', '')}"

            delete_results = result.get("result", {}).get("DeleteResults", [])

            success = [r["Id"] for r in delete_results if r.get("Id") and not r.get("Errors")]
            errors = []
            for r in delete_results:
                if r.get("Errors"):
                    errors.extend([f"ID {r.get('Id', '?')}: {e.get('Message')}" for e in r["Errors"]])

            response = f"Successfully deleted {len(success)} Turbo page(s)."
            if errors:
                response += f"\n\nErrors:\n" + "\n".join(f"- {e}" for e in errors)

            return response

        except Exception as e:
            return handle_api_error(e)

    @mcp.tool(
        name="direct_get_turbo_page_templates",
        annotations={
            "title": "Get Turbo Page Templates from Yandex Direct",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False
        }
    )
    async def direct_get_turbo_page_templates() -> str:
        """Get available Turbo page templates.

        Returns a list of available templates that can be used when creating Turbo pages.
        Each template has different layouts and customization options.
        """
        try:
            request_params = {}

            result = await api_client.direct_request("turbo-pages", "get_templates", request_params)

            if "error" in result:
                err = result["error"]
                return f"API Error: {err.get('error_code')}: {err.get('error_string')} | {err.get('error_detail', '')}"

            templates = result.get("result", {}).get("Templates", [])

            if not templates:
                return "No Turbo page templates available."

            lines = ["# Turbo Page Templates\n"]
            for template in templates:
                template_id = template.get("TemplateId", "N/A")
                name = template.get("Name", "Unnamed Template")
                lines.append(f"## {name} (ID: {template_id})")

                category = template.get("Category")
                if category:
                    lines.append(f"- **Category**: {category}")

                description = template.get("Description")
                if description:
                    lines.append(f"- **Description**: {description}")

                preview_url = template.get("PreviewUrl")
                if preview_url:
                    lines.append(f"- **Preview**: {preview_url}")

                lines.append("")

            return "\n".join(lines)

        except Exception as e:
            return handle_api_error(e)
