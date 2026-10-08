"""Where everything lives (paths) and the service's version. Change folders with environment variables, no code changes."""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # 05_explanation_api/
# the explanation FACTORY (plain Python): the SAME code that builds the published page — no copy of it here any more
FACTORY_DIR = os.environ.get("EXPLAIN_FACTORY_DIR", os.path.join(os.path.dirname(BASE_DIR), "02_question_factory"))
ENGINE_DIR = FACTORY_DIR                                                        # (old name, kept for older code)
PLAYER_DIR = os.path.join(FACTORY_DIR, "player")                                # the page's builder + its template
PAGE_TEMPLATE = os.path.join(PLAYER_DIR, "explain_template.html")               # built from 03_explain_player_src (build_explain_template.py)
SAMPLES_DIR = FACTORY_DIR                                                       # the 12 sample books (*_book_graph.json)
ART_FILE = os.path.join(BASE_DIR, "art", "art.json")                            # every character drawing, in ONE file
DATA_DIR = os.environ.get("EXPLAIN_DATA_DIR", os.path.join(BASE_DIR, "data"))   # generated explanations are kept here
GRAPHS_DIR = os.path.join(DATA_DIR, "graphs")                                   # the graphs we received
BOOKS_DIR = os.path.join(DATA_DIR, "books")                                     # one folder per book: lessons/<id>/explanations.json
SEED_SAMPLES = os.environ.get("EXPLAIN_SEED", "1") != "0"                      # first start with no books: make the 12 sample books
API_VERSION = "2.0.0"
CORS_ORIGINS = [o.strip() for o in os.environ.get("EXPLAIN_CORS_ORIGINS", "*").split(",") if o.strip()]
