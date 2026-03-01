"""Yandex Direct AgencyClients tools.

This module provides tools for managing agency client accounts.
AgencyClients API is used by advertising agencies to manage their sub-accounts.
"""

import json
from mcp.server.fastmcp import FastMCP

from ...client import api_client
from ...models.common import ResponseFormat
from ...models.direct_extended import (
    GetAgencyClientsInput,
    UpdateAgencyClientInput,
)
from ...utils import handle_api_error


def register(mcp: FastMCP) -> None:
    """Register agency clients tools."""

    # =========================================================================
    # Get Agency Clients
    # =========================================================================

    @mcp.tool(
        name="direct_get_agency_clients",
        annotations={
            "title": "Get Yandex Direct Agency Clients",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False
        }
    )
    async def direct_get_agency_clients(params: GetAgencyClientsInput) -> str:
        """Get list of agency client accounts.

        Returns information about all client accounts managed by the agency.
        Use this to get an overview of all sub-accounts under your agency.
        Requires agency credentials (token with agency rights).
        """
        try:
            request_params = {
                "Page": {
                    "Limit": params.limit,
                    "Offset": params.offset
                },
                "FieldNames": [
                    "ClientId", "Login", "Status", "Type", "Currency",
                    "AccountManagement", "Grants", "ClientInfo", "CreatedAt"
                ]
            }

            if params.logins:
                request_params["Logins"] = params.logins

            if params.status:
                request_params["Status"] = params.status

            result = await api_client.direct_request(
                "agencyclients", "get", request_params
            )
            clients = result.get("result", {}).get("Clients", [])

            if params.response_format == ResponseFormat.JSON:
                return json.dumps({"clients": clients}, indent=2, ensure_ascii=False)

            if not clients:
                return "No agency client accounts found."

            lines = ["# Agency Client Accounts\n"]

            for client in clients:
                lines.append(f"## {client.get('Login', 'Unknown')}")
                lines.append(f"- **Client ID**: {client.get('ClientId', 'N/A')}")
                lines.append(f"- **Login**: {client.get('Login', 'N/A')}")
                lines.append(f"- **Status**: {client.get('Status', 'N/A')}")
                lines.append(f"- **Type**: {client.get('Type', 'N/A')}")
                lines.append(f"- **Currency**: {client.get('Currency', 'N/A')}")
                lines.append(f"- **Created At**: {client.get('CreatedAt', 'N/A')}")

                # Account Management
                account_mgmt = client.get("AccountManagement", {})
                if account_mgmt:
                    lines.append(f"- **Account Manager**: {account_mgmt.get('AgencyUserId', 'N/A')}")

                # Client Info
                client_info = client.get("ClientInfo")
                if client_info:
                    lines.append(f"- **Client Name**: {client_info}")

                # Grants (permissions)
                grants = client.get("Grants", [])
                if grants:
                    lines.append("\n### Permissions")
                    for grant in grants:
                        privilege = grant.get("Privilege", "N/A")
                        value = grant.get("Value", "N/A")
                        lines.append(f"- **{privilege}**: {value}")

                lines.append("")

            return "\n".join(lines)

        except Exception as e:
            return handle_api_error(e)

    # =========================================================================
    # Update Agency Client
    # =========================================================================

    @mcp.tool(
        name="direct_update_agency_client",
        annotations={
            "title": "Update Yandex Direct Agency Client",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False
        }
    )
    async def direct_update_agency_client(params: UpdateAgencyClientInput) -> str:
        """Update agency client account settings.

        Use this to modify notification settings and preferences for a client account.
        Requires agency credentials (token with agency rights).
        """
        try:
            # Build the updates structure
            updates = {}

            # Add settings if provided
            if params.settings:
                settings_dict = {}
                if params.settings.send_account_warnings is not None:
                    settings_dict["SendAccountWarnings"] = (
                        "YES" if params.settings.send_account_warnings else "NO"
                    )
                if params.settings.send_notification_about_warnings is not None:
                    settings_dict["SendNotificationAboutWarnings"] = (
                        "YES" if params.settings.send_notification_about_warnings else "NO"
                    )
                if settings_dict:
                    updates["Settings"] = settings_dict

            # Add notification if provided
            if params.notification:
                notification_dict = {}
                if params.notification.email is not None:
                    notification_dict["Email"] = params.notification.email
                if params.notification.email_balance is not None:
                    notification_dict["EmailBalance"] = (
                        "YES" if params.notification.email_balance else "NO"
                    )
                if params.notification.email_trade_offers is not None:
                    notification_dict["EmailTradeOffers"] = (
                        "YES" if params.notification.email_trade_offers else "NO"
                    )
                if params.notification.email_advertising_on_account is not None:
                    notification_dict["EmailAdvertisingOnAccount"] = (
                        "YES" if params.notification.email_advertising_on_account else "NO"
                    )
                if notification_dict:
                    updates["Notification"] = notification_dict

            if not updates:
                return "No updates provided. Please provide settings or notification to update."

            request_params = {
                "Login": params.login,
                "Updates": updates
            }

            result = await api_client.direct_request(
                "agencyclients", "update", request_params
            )
            data = result.get("result", {})

            if params.response_format == ResponseFormat.JSON:
                return json.dumps(data, indent=2, ensure_ascii=False)

            # Check for errors
            update_results = data.get("UpdateResults", [])
            if not update_results:
                return "No results returned."

            lines = ["# Update Agency Client Result\n"]
            lines.append(f"**Login**: {params.login}")
            lines.append("")

            for res in update_results:
                if res.get("Errors"):
                    lines.append("## Errors")
                    for err in res["Errors"]:
                        lines.append(f"- **{err.get('Code')}**: {err.get('Message')}")
                    lines.append("")
                else:
                    lines.append("## Success")
                    lines.append("Settings updated successfully.")
                    lines.append("")

            return "\n".join(lines)

        except Exception as e:
            return handle_api_error(e)
