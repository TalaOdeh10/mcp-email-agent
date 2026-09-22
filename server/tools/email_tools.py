from server.services.gmail_service import GmailService


gmail_service = GmailService()


def list_emails(max_results: int = 10) -> list:
    """List recent emails from the Gmail inbox."""

    return gmail_service.list_emails(
        max_results=max_results
    )


def search_emails(
    query: str,
    max_results: int = 10
) -> list:
    """Search Gmail emails using a Gmail search query."""

    return gmail_service.search_emails(
        query=query,
        max_results=max_results
    )


def get_email(email_id: str) -> dict:
    """Get the full content of one Gmail email by ID."""

    return gmail_service.get_email(
        email_id=email_id
    )