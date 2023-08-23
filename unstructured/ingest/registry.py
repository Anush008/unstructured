import json
from typing import Dict, Type

from dataclasses_json import DataClassJsonMixin

from unstructured.ingest.connector.airtable import AirtableIngestDoc
from unstructured.ingest.connector.azure import AzureBlobStorageIngestDoc
from unstructured.ingest.connector.biomed import BiomedIngestDoc
from unstructured.ingest.connector.box import BoxIngestDoc
from unstructured.ingest.connector.confluence import ConfluenceIngestDoc
from unstructured.ingest.connector.discord import DiscordIngestDoc
from unstructured.ingest.connector.dropbox import DropboxIngestDoc
from unstructured.ingest.connector.elasticsearch import ElasticsearchIngestDoc
from unstructured.ingest.connector.gcs import GcsIngestDoc
from unstructured.ingest.connector.github import GitHubIngestDoc
from unstructured.ingest.connector.gitlab import GitLabIngestDoc
from unstructured.ingest.connector.google_drive import GoogleDriveIngestDoc
from unstructured.ingest.connector.local import LocalIngestDoc
from unstructured.ingest.connector.onedrive import OneDriveIngestDoc
from unstructured.ingest.connector.outlook import OutlookIngestDoc
from unstructured.ingest.connector.reddit import RedditIngestDoc
from unstructured.ingest.connector.s3 import S3IngestDoc
from unstructured.ingest.connector.sharepoint import SharepointIngestDoc
from unstructured.ingest.connector.slack import SlackIngestDoc
from unstructured.ingest.connector.wikipedia import (
    WikipediaIngestHTMLDoc,
    WikipediaIngestSummaryDoc,
    WikipediaIngestTextDoc,
)

INGEST_DOC_NAME_TO_CLASS: Dict[str, Type[DataClassJsonMixin]] = {
    "airtable": AirtableIngestDoc,
    "azure": AzureBlobStorageIngestDoc,
    "biomed": BiomedIngestDoc,
    "box": BoxIngestDoc,
    "confluence": ConfluenceIngestDoc,
    "discord": DiscordIngestDoc,
    "dropbox": DropboxIngestDoc,
    "elasticsearch": ElasticsearchIngestDoc,
    "gcs": GcsIngestDoc,
    "github": GitHubIngestDoc,
    "gitlab": GitLabIngestDoc,
    "google_drive": GoogleDriveIngestDoc,
    "local": LocalIngestDoc,
    "onedrive": OneDriveIngestDoc,
    "outlook": OutlookIngestDoc,
    "reddit": RedditIngestDoc,
    "s3": S3IngestDoc,
    "sharepoint": SharepointIngestDoc,
    "slack": SlackIngestDoc,
    "wikipedia_html": WikipediaIngestHTMLDoc,
    "wikipedia_text": WikipediaIngestTextDoc,
    "wikipedia_summary": WikipediaIngestSummaryDoc,
}


def create_instance_from_json(data_json: str) -> DataClassJsonMixin:
    data_dict = json.loads(data_json)
    registry_name = data_dict.pop("registry_name")
    try:
        ingest_doc_cls = INGEST_DOC_NAME_TO_CLASS[registry_name]
        return ingest_doc_cls.from_json(data_json)
    except KeyError:
        raise ValueError(
            f"Error: Received unknown IngestDoc name: {registry_name} while deserializing",
            "IngestDoc.",
        )
