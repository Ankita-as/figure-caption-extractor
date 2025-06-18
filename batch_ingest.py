import sys
from src.ingestor import process_paper
from src.logger import setup_logger, logger
from src.config_loader import load_config

def batch_ingest(file_path):
    try:
        with open(file_path, "r") as f:
            ids = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return
    
    for pid in ids:
        try:
            logger.info(f"Processing paper ID: {pid}")
            process_paper(pid)
            logger.info(f"Successfully processed {pid}")
        except Exception as e:
            logger.error(f"Failed to process {pid}: {e}")

if __name__ == "__main__":
    # Setup logger with DEBUG level to see detailed logs
    setup_logger(level="DEBUG")
    config = load_config()
    
    if len(sys.argv) < 2:
        logger.error("Usage: python batch_ingest.py paper_ids.txt")
        sys.exit(1)
    else:
        batch_ingest(sys.argv[1])
