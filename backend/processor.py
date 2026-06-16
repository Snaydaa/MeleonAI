import logging
import os
import time
import json
from pathlib import Path
from PIL import Image
import base64
import mimetypes
from openai import OpenAI
from dotenv import load_dotenv

BASISVERZEICHNIS = Path(__file__).resolve().parent.parent

env_pfad       = BASISVERZEICHNIS / ".env"
schluessel_pfad = BASISVERZEICHNIS / "schluessel.env"

if schluessel_pfad.exists():
    load_dotenv(dotenv_path=schluessel_pfad)
else:
    load_dotenv(dotenv_path=env_pfad)

if not os.getenv("OPENAI_API_KEY"):
    print("WARNUNG: Kein OPENAI_API_KEY gefunden! Bitte .env-Datei prüfen.")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("MarsProcessor")


class MarsProcessor:
    """Zentrales Backend-Gehirn. Steuert alle Phasen der Pipeline."""

    @classmethod
    def verarbeiten(cls, medienpfad: Path, eingabe: str, medientyp: str) -> dict:
        log.info(f"JOB START: {medienpfad.name}")

        ziel_nische  = "Motivation / Alpha / Sigma Grindset"
        sprach_stil  = eingabe

        # Phase 0: Smarte Schablone
        log.info("Phase 0: Smarte Schablone wird berechnet...")
        (
            vorbereiteter_pfad, ziel_b, ziel_h, neu_b, neu_h,
            massstab, offset_x, offset_y, orig_b, orig_h
        ) = cls.auf_bucket_padden(medienpfad)
        log.info(f"Phase 0 fertig -> Bucket {ziel_b}x{ziel_h}")

        # Phase 1: Scout
        log.info("Phase 1: Scout analysiert das Bild...")
        basis_json = cls.scout_phase_starten(vorbereiteter_pfad)
        log.info("Phase 1 fertig")
        print("\n" + "=" * 50)
        print("SCOUT JSON OUTPUT:")
        print(json.dumps(basis_json, indent=2))
        print("=" * 50 + "\n")

        # Phase 2: Artist
        log.info("Phase 2: Artist übersetzt den Text...")
        aenderungs_json = cls.artist_phase_starten(basis_json, ziel_nische, sprach_stil)
        log.info("Phase 2 fertig")
        print("\n" + "=" * 50)
        print("ARTIST JSON OUTPUT:")
        print(json.dumps(aenderungs_json, indent=2))
        print("=" * 50 + "\n")

        # Phase 2.5: Delta-Patch
        log.info("Phase 2.5: Delta-Patch wird angewendet...")
        render_json = cls.delta_patch_anwenden(basis_json, aenderungs_json)
        log.info("Phase 2.5 fertig")

        # Phase 3: Renderer (Mock)
        log.info("Phase 3: Renderer (Mock-Modus)...")
        time.sleep(1)
        bild_pfad = vorbereiteter_pfad
        log.info("Phase 3 fertig")

        # Phase 4: Zuschneiden
        log.info("Phase 4: Zurück zum Originalformat...")
        finales_bild = cls.originalformat_wiederherstellen(
            bild_pfad, offset_x, offset_y, neu_b, neu_h, orig_b, orig_h
        )
        log.info(f"Phase 4 fertig -> Bild gespeichert: {finales_bild}")

        ausgabe = (
            f"=== PHASE 1: SCOUT ===\n"
            f"{json.dumps(basis_json, indent=2)}\n\n"
            f"=== PHASE 2.5: PATCHED RENDER JSON ===\n"
            f"{json.dumps(render_json, indent=2)}"
        )

        return {"analysis": ausgabe}

    @staticmethod
    def _bild_kodieren(bildpfad: Path) -> str:
        mime_typ, _ = mimetypes.guess_type(bildpfad)
        if not mime_typ:
            mime_typ = "image/png"
        with open(bildpfad, "rb") as bilddatei:
            base64_daten = base64.b64encode(bilddatei.read()).decode("utf-8")
        return f"data:{mime_typ};base64,{base64_daten}"

    @staticmethod
    def scout_phase_starten(bildpfad: Path) -> dict:
        ki_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            timeout=60.0
        )
        base64_bild = MarsProcessor._bild_kodieren(bildpfad)

        system_anweisung = """/// SYSTEM_CORE_DIRECTIVE : MELEON_SCOUT_ULTRA_V3 ///
/// TASK_MODE: DETERMINISTIC_MULTIMODAL_OCR_LAYOUT_PARSER ///
/// OUTPUT_MODE: STRICT_STRUCTURED_JSON ///

INPUT_CONTRACT:
- Input is exactly ONE image.
- Your sole purpose is: OCR extraction, spatial layout mapping, typography estimation, and functional text classification.
- NEVER translate, summarize, or interpret semantic meaning beyond classification.
- NEVER invent missing text or auto-complete known memes.

GLOBAL_EXECUTION_RULES:
- Output ONLY valid JSON. Self-correct before responding if syntax is broken.
- TYPE_CONSTRAINTS: Numbers must be numeric (no strings), booleans must be true/false, null must be null.
- Preserve deterministic structure and field ordering.
- Unicode normalization is forbidden. Preserve emojis, zero-width characters, and spacing tricks exactly.

HARD_ANTI_HALLUCINATION_RULES:
- Extract ONLY visible characters. Cropped/blurred text must NOT be reconstructed.
- EMPTY_TEXT_RULE: Containers with empty \"text\" are ONLY allowed if `ocr_confidence` < 0.20 AND `functional_classification` = \"DECORATIVE\". Otherwise, they are forbidden.

COORDINATE_SYSTEM & GEOMETRY:
- Use ONLY normalized coordinates (0.000 → 1.000). Origin: top-left [0,0].
- `rotation_angle`: Must represent the baseline text angle in degrees. 0 = perfectly horizontal. Negative/positive values for tilt.

CONTAINER & MULTI_LINE_RULES:
- Group text sharing alignment, typography, and semantic structure into ONE container.
- Floating overlays, subtitles, watermarks, and independent captions must become separate containers.

READING_ORDER & LAYERING:
- Process in deterministic order: top-to-bottom, left-to-right, then z-index.
- Assign sequential integer IDs (starting from 1) and explicit `reading_order_index`.
- z_index = 0 is background text. Higher values represent overlapping foreground elements.

OCR_CONFIDENCE_RULES:
- 0.95–1.00 = perfectly readable
- 0.80–0.94 = minor uncertainty
- 0.72–0.79 = noticeable ambiguity
- below 0.72 = unreliable (blur, motion, cropped, extreme styling)

TYPOGRAPHY_RULES:
- `font_class`: \"sans-serif\", \"serif\", \"handwritten\", \"display/meme\", \"system-ui\".
- `font_weight`: \"light\", \"normal\", \"bold\", \"heavy\".

FUNCTIONAL_CLASSIFICATION_RULES:
- \"MAIN_QUOTE\": Core meme/caption message.
- \"WATERMARK_HANDLE\": Creator handles, @usernames, logos with text.
- \"UI_ELEMENT\": Platform UI text, timestamps.
- \"CTA\": Calls to action.
- \"DECORATIVE\": Unreadable background typography.

SAFETY_LIMITS:
- MAX_CONTAINER_LIMIT: If containers > 80, aggressively reduce by merging or completely omitting low-information UI_ELEMENTs to prevent JSON explosion.

OUTPUT_SCHEMA:
{
  \"operation_status\": \"SUCCESS\",
  \"image_metadata\": {
    \"global_readability_score\": 0.00,
    \"background_complexity\": \"solid\"
  },
  \"containers\": [
    {
      \"id\": 1,
      \"reading_order_index\": 1,
      \"text\": \"Example text\",
      \"detected_language\": \"en\",
      \"ocr_confidence\": 0.95,
      \"bounding_box\": {\"x_min\": 0.000, \"y_min\": 0.000, \"x_max\": 0.000, \"y_max\": 0.000},
      \"rotation_angle\": 0.0,
      \"z_index\": 0,
      \"is_distorted\": false,
      \"typography\": {
        \"font_class\": \"sans-serif\",
        \"font_weight\": \"bold\",
        \"has_outline_or_shadow\": true,
        \"is_uppercase_dominant\": true,
        \"text_alignment\": \"center\",
        \"text_color\": \"#FFFFFF\"
      },
      \"functional_classification\": \"MAIN_QUOTE\"
    }
  ]
}

FINAL_VALIDATION_LOOP:
Before output, silently verify:
1. Is output 100% valid JSON?
2. Are all fields properly typed (no string-numbers)?
3. Are reading_order_index and IDs strictly increasing with NO duplicates?
4. Are all bounding_box coordinates strictly inside bounds [0.000 to 1.000]?
5. Are there any forbidden ghost containers (empty text without DECORATIVE classification)?
6. Is the rotation_angle logically estimated?"""

        antwort = ki_client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_anweisung},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this image and return the JSON according to the schema."},
                        {"type": "image_url", "image_url": {"url": base64_bild}}
                    ]
                }
            ]
        )

        return json.loads(antwort.choices[0].message.content)

    @staticmethod
    def artist_phase_starten(basis_json: dict, ziel_nische: str, sprach_stil: str) -> dict:
        ki_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            timeout=60.0
        )

        system_anweisung = """/// SYSTEM_CORE_DIRECTIVE : MELEON_ARTIST_ULTRA_V7 ///
/// TASK_MODE: DETERMINISTIC_DELTA_PATCH_ENGINE ///
/// OUTPUT_MODE: STRICT_JSON_ONLY ///

INPUT_CONTRACT:
- Input is a PRE-FILTERED BASE_JSON generated and sanitized upstream from SCOUT_ULTRA_V3.
- PRE-FILTERING GUARANTEE (enforced by upstream Python pipeline before this call):
    → All containers with ocr_confidence < 0.72 have already been removed.
    → All containers with functional_classification IN [\"WATERMARK_HANDLE\", \"UI_ELEMENT\", \"DECORATIVE\"]
      have already been removed.
- Every container present in BASE_JSON is a candidate for translation. No confidence or
  classification filtering is required or permitted inside this system.
- SCOUT data is the SINGLE SOURCE OF TRUTH and fully IMMUTABLE.
- This system ONLY generates text transformation PATCHES.
- No reconstruction, no reasoning about layout, no reinterpretation of SCOUT data.

UPSTREAM_TRUST_MANDATE (ABSOLUTE):
- `functional_classification` is FINAL.
- `ocr_confidence` is FINAL.
- `detected_language` is FINAL.

IMMUTABILITY_CORE:
- The only valid reference key for output is `id`.
- SCOUT geometry fields (bounding_box, rotation_angle, z_index, typography, is_distorted,
  ocr_confidence, detected_language, functional_classification) are OUTPUT-FORBIDDEN.
  They must NEVER appear in any output entry.
- TRANSLATION_CONTEXT_EXCEPTION (read-only, output-forbidden):
    → `reading_order_index` MAY be silently read to understand narrative structure
      (e.g., premise → punchline dynamics, speaker attribution, sequential joke flow).
    → This field must NEVER be reproduced, referenced, or included in any output field.
    → It is a silent reasoning aid only.
- No inference about visual position or rendering is allowed.

TRANSLATION EXECUTION RULES (Driven by TARGET_NICHE / LANGUAGE_STYLE):
IF functional_classification == \"MAIN_QUOTE\":
    → Translate into TARGET_LANGUAGE, adapting to TARGET_NICHE style.
    → Use reading_order_index context (read-only) to preserve narrative flow and
      punchline dynamics across related containers.
    → Preserve core meaning, tone, and sentence structure.
    → Max ±25% length deviation. No semantic expansion.

IF functional_classification == \"CTA\":
    → Translate + localize naturally.
    → Keep short, action-driven, platform-native.

OUTPUT BEHAVIOR MODEL:
- Each output entry represents a PATCH operation.
- All PATCHES are explicit \"REPLACE text\" operations.

OUTPUT_SCOPE (STRICT LIMIT):
Each container object in the output array MUST contain ONLY:
  - id (Integer)
  - op (String, MUST ALWAYS be \"replace\")
  - text_translated (String)
NO OTHER FIELDS ARE ALLOWED.

EDGE CASE RULE:
If no containers qualify for translation (BASE_JSON is empty or all are non-translatable),
return:
{ \"operation_status\": \"no_translation_required\", \"containers\": [] }

OUTPUT_SCHEMA:
{
  \"operation_status\": \"SUCCESS\",
  \"containers\": [
    {
      \"id\": 1,
      \"op\": \"replace\",
      \"text_translated\": \"Der übersetzte Text hier.\"
    }
  ]
}

HARD FAILURE RULE:
If any rule is violated:
1. Output MUST still be valid JSON.
2. Must NOT hallucinate missing fields.
3. Must NEVER include SCOUT metadata in output.
4. Must NEVER include skipped containers.

FINAL_VALIDATION_LOOP (MANDATORY):
Before response, silently verify:
1. Validate JSON correctness.
2. Ensure ONLY allowed fields exist (`id`, `op`, `text_translated`).
3. Ensure `op` == \"replace\" for all entries.
4. Ensure NO SCOUT fields (geometry, typography, confidence, etc.) are present in output.
5. Ensure `reading_order_index` is NOT reproduced in any output field.
6. Ensure the narrative/punchline flow of related containers is semantically preserved
   where reading_order_index context was used."""

        nutzer_eingabe = f"""[RUNTIME_VARIABLES]
TARGET_NICHE: {ziel_nische}
LANGUAGE_STYLE: {sprach_stil}
TARGET_LANGUAGE: German

[BASE_JSON]
{json.dumps(basis_json)}"""

        antwort = ki_client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_anweisung},
                {"role": "user", "content": nutzer_eingabe}
            ]
        )

        return json.loads(antwort.choices[0].message.content)

    @staticmethod
    def delta_patch_anwenden(basis_json: dict, aenderungs_json: dict) -> dict:
        original = {c["id"]: c.copy() for c in basis_json["containers"]}

        for aenderung in aenderungs_json.get("containers", []):
            patch_id = aenderung.get("id")

            if patch_id not in original:
                log.warning(f"Ghost ID ignoriert: {patch_id}")
                continue

            neuer_text = aenderung.get("text_translated", "").strip()
            if neuer_text:
                original[patch_id]["text"] = neuer_text

        sortierte_container = sorted(
            original.values(), key=lambda x: x.get("reading_order_index", 0)
        )

        return {
            "operation_status": "SUCCESS",
            "containers": sortierte_container
        }

    @staticmethod
    def auf_bucket_padden(bildpfad: Path):
        with Image.open(bildpfad) as bild:
            orig_b, orig_h = bild.size
            seitenverhaeltnis = orig_b / orig_h

            if seitenverhaeltnis < 0.8:
                ziel_b, ziel_h = 1024, 1536
            elif seitenverhaeltnis > 1.2:
                ziel_b, ziel_h = 1536, 1024
            else:
                ziel_b, ziel_h = 1024, 1024

            massstab = min(ziel_b / orig_b, ziel_h / orig_h)
            neu_b    = int(orig_b * massstab)
            neu_h    = int(orig_h * massstab)

            skaliert = bild.resize((neu_b, neu_h), Image.Resampling.LANCZOS)
            leinwand = Image.new("RGB", (ziel_b, ziel_h), (0, 0, 0))

            offset_x = (ziel_b - neu_b) // 2
            offset_y = (ziel_h - neu_h) // 2
            leinwand.paste(skaliert, (offset_x, offset_y))

            vorbereiteter_pfad = bildpfad.with_name(f"{bildpfad.stem}_padded.png")
            leinwand.save(vorbereiteter_pfad)

        return (vorbereiteter_pfad, ziel_b, ziel_h, neu_b, neu_h,
                massstab, offset_x, offset_y, orig_b, orig_h)

    @staticmethod
    def originalformat_wiederherstellen(
        vorbereiteter_bildpfad: Path,
        offset_x: int, offset_y: int,
        neu_b: int, neu_h: int,
        orig_b: int, orig_h: int
    ):
        with Image.open(vorbereiteter_bildpfad) as bild:
            links  = offset_x
            oben   = offset_y
            rechts = offset_x + neu_b
            unten  = offset_y + neu_h

            ausgeschnitten = bild.crop((links, oben, rechts, unten))
            fertig = ausgeschnitten.resize((orig_b, orig_h), Image.Resampling.LANCZOS)

            ausgabe_pfad = vorbereiteter_bildpfad.with_name(
                f"{vorbereiteter_bildpfad.stem}_final.png"
            )
            fertig.save(ausgabe_pfad)

        return ausgabe_pfad
