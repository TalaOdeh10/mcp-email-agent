from googleapiclient.discovery import build

from server.auth.gmail_auth import get_gmail_service


class GmailService:

    def __init__(self):
        credentials = get_gmail_service()

        self.service = build(
            "gmail",
            "v1",
            credentials=credentials
        )

    def list_emails(self, max_results: int = 10):

        results = self.service.users().messages().list(
            userId="me",
            maxResults=max_results,
            labelIds=["INBOX"]
        ).execute()

        messages = results.get("messages", [])

        emails = []

        for message in messages:

            email = self.service.users().messages().get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=[
                    "From",
                    "Subject",
                    "Date"
                ]
            ).execute()

            emails.append(
                self._format_email(email)
            )

        return emails

    def search_emails(
        self,
        query: str,
        max_results: int = 10
    ):

        results = self.service.users().messages().list(
            userId="me",
            q=query,
            maxResults=max_results
        ).execute()

        messages = results.get("messages", [])

        emails = []

        for message in messages:

            email = self.service.users().messages().get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=[
                    "From",
                    "Subject",
                    "Date"
                ]
            ).execute()

            emails.append(
                self._format_email(email)
            )

        return emails

    def get_email(self, email_id: str):

        return self.service.users().messages().get(
            userId="me",
            id=email_id,
            format="full"
        ).execute()

    @staticmethod
    def _format_email(email):

        headers = email.get(
            "payload",
            {}
        ).get(
            "headers",
            []
        )

        return {
            "id": email["id"],
            "snippet": email.get("snippet", ""),
            "headers": {
                header["name"]: header["value"]
                for header in headers
            }
        }