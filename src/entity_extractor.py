import spacy
import requests

# Load the biomedical NER model from scispaCy
try:
    nlp = spacy.load("en_ner_bionlp13cg_md")
except Exception as e:
    print(f"❌ Failed to load scispaCy model: {e}")
    nlp = None

def extract_figure_captions(paper_json):
    """
    Extracts figure captions from a BioC-formatted JSON.
    Returns a list of captions with associated figure URLs.
    """
    captions = []

    if isinstance(paper_json, list):
        paper_doc = paper_json[0]
    elif isinstance(paper_json, dict):
        paper_doc = paper_json
    else:
        print("⚠️ Unexpected JSON structure")
        return captions

    documents = paper_doc.get("documents", [])
    print(f"DEBUG: Number of documents found: {len(documents)}")

    if not documents:
        print("⚠️ No documents present in JSON")
        return captions

    for doc_idx, document in enumerate(documents):
        passages = document.get("passages", [])
        print(f"DEBUG: Document {doc_idx} contains {len(passages)} passages")

        for passage_idx, passage in enumerate(passages):
            section_type = passage.get("infons", {}).get("section_type", "").strip().upper()
            print(f"DEBUG: Passage {passage_idx} - section_type: {section_type}")

            if section_type == "FIG":
                caption_text = passage.get("text", "").strip()
                figure_url = passage.get("infons", {}).get("url", "N/A")

                if caption_text:
                    print(f"🖼️ FIG caption extracted: {caption_text[:80]}...")
                    captions.append({
                        "caption": caption_text,
                        "figure_url": figure_url
                    })

    if not captions:
        print("⚠️ No figure captions extracted.")

    return captions


def get_entities_from_caption_local(caption_text):
    """
    Extract biomedical entities locally using a scispaCy NER model.
    Returns a list of {'mention': ..., 'type': ...} dictionaries.
    """
    if not nlp:
        print("❌ scispaCy model not loaded. Skipping entity extraction.")
        return []

    try:
        doc = nlp(caption_text)
        entities = [{"mention": ent.text, "type": ent.label_} for ent in doc.ents]
        return entities
    except Exception as e:
        print(f"❌ Error during local NER processing: {e}")
        return []


def get_entities_from_caption_pubtator(caption_text):
    """
    Extract biomedical entities using the PubTator API.
    Returns a list of {'id': ..., 'type': ..., 'text': ..., 'start': ..., 'end': ...}.
    """
    url = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/annotate/"
    headers = {"Content-Type": "text/plain"}
    
    try:
        response = requests.post(url, data=caption_text.encode('utf-8'), headers=headers)
        response.raise_for_status()
        annotations = response.json()
        
        entities = []
        for ann in annotations.get('annotations', []):
            entities.append({
                'id': ann.get('id'),
                'type': ann.get('type'),
                'text': ann.get('text'),
                'start': ann.get('start'),
                'end': ann.get('end')
            })
        return entities
    except Exception as e:
        print(f"❌ PubTator API call failed: {e}")
        return []

# Example helper to select method:
def get_entities_from_caption(caption_text, method='local'):
    """
    Wrapper to get entities from caption using specified method:
    - 'local' : scispaCy NER
    - 'pubtator' : PubTator API
    """
    if method == 'local':
        return get_entities_from_caption_local(caption_text)
    elif method == 'pubtator':
        return get_entities_from_caption_pubtator(caption_text)
    else:
        print(f"⚠️ Unknown extraction method: {method}")
        return []

