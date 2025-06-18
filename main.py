import sys
import time
from src.db import init_db, insert_captions
from src.ingestor import fetch_paper_data
from src.entity_extractor import extract_figure_captions, get_entities_from_caption

def run_demo(pmc_id):
    print(f"\n📄 Fetching paper data for: {pmc_id}...\n")

    try:
        paper_data = fetch_paper_data(pmc_id)
        if not paper_data:
            print("❌ Failed to fetch or parse paper data.")
            return False

        print(f"DEBUG: Type of fetched JSON data: {type(paper_data)}")
        if isinstance(paper_data, list):
            print(f"DEBUG: Sample JSON data keys: {paper_data[0].keys() if len(paper_data) > 0 else 'Empty list'}")
        elif isinstance(paper_data, dict):
            print(f"DEBUG: JSON keys: {paper_data.keys()}")

        captions = extract_figure_captions(paper_data)
        if not captions:
            print("⚠️ No figure captions found.")
            return False

        for i, cap in enumerate(captions):
            print(f"\n🖼️ Figure {i + 1}:")
            print(f"Caption: {cap['caption']}")
            print(f"Figure URL: {cap['figure_url']}")

            entities = get_entities_from_caption(cap['caption'])
            cap["entities"] = entities

            print("Entities:")
            if entities:
                for ent in entities:
                    print(f"  - {ent['mention']} ({ent['type']})")
            else:
                print("  - No entities found.")

        insert_captions(pmc_id, captions)
        print("\n✅ Data saved to DuckDB.")
        return True
    except Exception as e:
        print(f"❌ Error processing {pmc_id}: {e}")
        return False

def watch_folder(path="./watched"):
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    import os

    class IngestHandler(FileSystemEventHandler):
        def on_created(self, event):
            if event.is_directory or not event.src_path.endswith(".txt"):
                return
            try:
                with open(event.src_path, "r") as f:
                    pmc_ids = [line.strip() for line in f if line.strip()]
                print(f"\n📁 New file detected: {event.src_path}")
                for pmc_id in pmc_ids:
                    success = run_demo(pmc_id)
                    status = "✅ Success" if success else "❌ Failure"
                    print(f"{pmc_id}: {status}")
            except Exception as e:
                print(f"❌ Error reading {event.src_path}: {e}")

    print(f"👀 Watching folder: {path}")
    event_handler = IngestHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    init_db()
    args = sys.argv[1:]

    if "--watch-folder" in args:
        watch_folder()
    else:
        pmc_ids = args or ["PMC3787942", "PMC1012345"]
        all_success = True
        for pmc_id in pmc_ids:
            success = run_demo(pmc_id)
            all_success = all_success and success

        sys.exit(0 if all_success else 1)
