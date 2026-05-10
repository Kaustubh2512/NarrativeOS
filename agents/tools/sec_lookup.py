from __future__ import annotations

import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


def lookup_sec_filings(ticker: str, max_results: int = 3) -> list[str]:
    filings: list[str] = []

    data_dir = Path(__file__).resolve().parent.parent.parent / "data" / "actors" / "sec-scraper" / "storage" / "key_value_stores" / "default"
    output_file = data_dir / "OUTPUT.json"
    if output_file.exists():
        try:
            with open(output_file) as f:
                raw = json.load(f)
            if isinstance(raw, list):
                for filing in raw[:max_results]:
                    name = filing.get("company_name", ticker)
                    form = filing.get("form_type", "N/A")
                    date = filing.get("filing_date", "")
                    filings.append(f"{name} - {form} ({date})")
        except Exception as e:
            logger.warning("Failed to read SEC output: %s", e)

    if not filings:
        filings.append(f"{ticker}: SEC data not cached. Run sec-scraper actor first.")

    return filings
