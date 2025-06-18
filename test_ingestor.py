import logging
from src.ingestor import fetch_paper_json
from src.ingestor import extract_figure_captions  # assuming this function is in ingestor.py

# Setup logger to print to console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("figure-caption-extractor")

test_paper_ids = ["PMC8680561", "PMC3991889", "PMC7000011"]

for pid in test_paper_ids:
    logger.info(f"Testing extraction for paper {pid}")
    paper_json = fetch_paper_json(pid)
    if paper_json is None:
        logger.error(f"Failed to fetch JSON for {pid}")
        continue
    captions = extract_figure_captions(paper_json)
    logger.info(f"Extracted {len(captions)} captions from {pid}")
    for i, caption in enumerate(captions, start=1):
        print(f"Caption {i}: {caption[:200]}...\n")  # Show first 200 chars of each caption
