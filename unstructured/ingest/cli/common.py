import logging
from typing import Optional

from click import ClickException

from unstructured.ingest.logger import ingest_log_streaming_init, logger

SENSITIVE_FIELDS = [
    "account_name",
    "account_key",
    "api_key",
    "token",
    "client_id",
    "client_cred",
    "password",
]


def run_init_checks(
    verbose: bool,
    local_input_path: Optional[str],
    download_dir: Optional[str],
    metadata_exclude: Optional[str],
    metadata_include: Optional[str],
    flatten_metadata: bool,
    fields_include: str,
    partition_by_api: bool,
    partition_endpoint: Optional[str],
    preserve_downloads: bool,
    download_only: bool,
    **kwargs,
):
    ingest_log_streaming_init(logging.DEBUG if verbose else logging.INFO)
    # Initial breaking checks
    if local_input_path is not None and download_dir:
        raise ClickException(
            "Files should already be in local file system: there is nothing to download, "
            "but --download-dir is specified.",
        )
    if metadata_exclude is not None and metadata_include is not None:
        raise ClickException(
            "Arguments `--metadata-include` and `--metadata-exclude` are "
            "mutually exclusive with each other.",
        )

    # Warnings
    if flatten_metadata and "metadata" not in fields_include:
        logger.warning(
            "`--flatten-metadata` is specified, but there is no metadata to flatten, "
            "since `--metadata` is not specified in `--fields-include`.",
        )
    if "metadata" not in fields_include and (metadata_include or metadata_exclude):
        logger.warning(
            "Either '--metadata-include` or `--metadata-exclude` is specified"
            " while metadata is not specified in fields-include.",
        )

    if (
        not partition_by_api
        and partition_endpoint != "https://api.unstructured.io/general/v0/general"
    ):
        logger.warning(
            "Ignoring --partition-endpoint because --partition-by-api was not set",
        )
    if (not preserve_downloads and not download_only) and download_dir:
        logger.warning(
            "Not preserving downloaded files but download_dir is specified",
        )

def replace_sensitive_values(sensitive_dict: dict, target_keys: list[str] = SENSITIVE_FIELDS):
    """
    Recursively replace values of sensitive fields in a dict with "*******"
    Be sure to send in a COPY of the dict because this function mutates the dict
    """
    print("***** party time *****")
    for key, value in sensitive_dict.items():
        if key in target_keys and value is not None:
            sensitive_dict[key] = "*******"
        elif isinstance(value, dict):
            replace_sensitive_values(value, target_keys)
    return sensitive_dict

def log_options(options: dict, verbose=False):
    ingest_log_streaming_init(logging.DEBUG if verbose else logging.INFO)
    options_to_log = replace_sensitive_values(options.copy(), SENSITIVE_FIELDS)
    # options_to_log = options.copy()
    # options_to_log.update(
    #     {
    #         k: "*******"
    #         for k, v in options_to_log.items()
    #         if k in SENSITIVE_FIELDS and v is not None
    #     },
    # )
    logger.debug(f"options: {options_to_log}")
