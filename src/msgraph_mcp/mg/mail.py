from markdownify import markdownify as md

from ..models import MailInfo
from .client import GRAPH_CLIENT

async def search_mails(search_value: str, top: int = 5) -> list[MailInfo]:
    """
    Search for emails in the user's mailbox based on a search term.
    
    This function queries Microsoft Graph API to search through the user's email messages
    and returns structured information about matching emails. The email body content is
    converted from HTML to Markdown format for easier consumption.
    
    Args:
        search_value (str): The search term to look for in emails. This will be wrapped
                           in quotes for exact phrase matching.
        top (int, optional): Maximum number of emails to return. Defaults to 5.
    
    Returns:
        list[MailInfo]: A list of MailInfo objects containing email details including:
                       - from_address: Sender's email address
                       - subject: Email subject line
                       - send_date_time: When the email was sent
                       - body: Email body content converted to Markdown
                       - id: Unique email identifier
    
    Example:
        >>> mails = await search_mails("project update", 10)
        >>> print(f"Found {len(mails)} emails")
        >>> print(mails[0].subject)
    """
    mails = await GRAPH_CLIENT.me.messages.get(
        GRAPH_CLIENT.me.messages.MessagesRequestBuilderGetRequestConfiguration(
            query_parameters=GRAPH_CLIENT.me.messages.MessagesRequestBuilderGetQueryParameters(
                search= '"' + search_value + '"', 
                select=['from', 'subject', 'sentDateTime', 'body'],
                top=top
            )
        )
    )
    received_mails = []
    for mail in mails.value:
        received_mails.append(
            MailInfo(
                from_address=mail.from_.email_address.address,
                subject=mail.subject,
                send_date_time= mail.sent_date_time,
                body = md(mail.body.content),
                id = mail.id
            )
        )
    return received_mails 

async def search_email_addresses(search_value: str, top_mails: int = 3) -> list[str]:
    """
    Extract unique email addresses from emails matching a search term.
    
    This function searches for emails based on a search term and extracts all unique
    email addresses from the sender (from), recipients (to), and carbon copy (cc) fields
    of the matching emails. This is useful for discovering contacts related to a specific
    topic or project.
    
    Args:
        search_value (str): The search term to look for in emails. This will be wrapped
                           in quotes for exact phrase matching.
        top_mails (int, optional): Maximum number of emails to search through for
                                  extracting addresses. Defaults to 3.
    
    Returns:
        list[str]: A list of unique email addresses found in the matching emails.
                  Duplicates are automatically removed.
    
    Example:
        >>> addresses = await search_email_addresses("quarterly report")
        >>> print(f"Found {len(addresses)} unique email addresses")
        >>> for addr in addresses:
        ...     print(addr)
    
    Note:
        The function searches through from, to_recipients, and cc_recipients fields
        to capture all email addresses associated with the matching emails.
    """
    mails = await GRAPH_CLIENT.me.messages.get(
        GRAPH_CLIENT.me.messages.MessagesRequestBuilderGetRequestConfiguration(
            query_parameters=GRAPH_CLIENT.me.messages.MessagesRequestBuilderGetQueryParameters(
                search= '"' + search_value + '"', 
                select=['from', 'toRecipients', 'ccRecipients'],
                top=top_mails
            )
        )
    )
    mail_addresses = set()
    for mail in mails.value:
        for audience in ['from_', 'to_recipients', 'cc_recipients']:
            field = getattr(mail, audience)
            if isinstance(field, list):
                for i in range(len(field)):
                    mail_addresses.add(field[i].email_address.address)
            else:
                mail_addresses.add(field.email_address.address)
    return list(mail_addresses)