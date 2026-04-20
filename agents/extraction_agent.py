import xml.etree.ElementTree as ET
from core.bdi_agent import BDIAgent
from core.utils import log, handle_error

class ExtractionAgent(BDIAgent):
    """
    Extracts structured data from XML.
    WHY: Converts raw API response into usable format for reasoning.
    """

    def __init__(self):
        # Initialise base BDI agent with name
        super().__init__("ExtractionAgent")

        # Initialise list to store extracted entries
        self.extracted_data = []

        # Define intention (BDI concept)
        self.intention = None


    def perceive(self, env):
        # Retrieve raw XML data from environment
        self.raw_data = env.get("raw_data")

        log("[ExtractionAgent] Retrieved raw data from environment")


    def deliberate(self):
        # Set intention for extraction
        self.intention = "extract_data"

        log(f"[ExtractionAgent] Intention set: {self.intention}")


    def act(self, env):
        try:
            # Check if raw data exists
            if not self.raw_data:
                # No data means extraction cannot proceed
                log("[ExtractionAgent] No raw data available. Waiting...")
                env.update("extracted_data", None)
                return

            # Attempt to parse XML
            try:
                root = ET.fromstring(self.raw_data)
                log("[ExtractionAgent] XML parsing successful")

            except Exception as e:
                # Handle XML parsing errors
                log(f"[ExtractionAgent] XML parsing failed: {str(e)}")
                env.update("extracted_data", None)
                return

            # Define namespace used by ArXiv API
            namespace = {"atom": "http://www.w3.org/2005/Atom"}

            # Reset extracted data list
            self.extracted_data = []

            # Iterate over each entry in XML
            for entry in root.findall("atom:entry", namespace):
                try:
                    # Extract title text
                    title = entry.find("atom:title", namespace).text.strip()

                    # Extract summary text
                    summary = entry.find("atom:summary", namespace).text.strip()

                    # Append structured record
                    self.extracted_data.append({
                        "title": title,
                        "summary": summary
                    })

                except Exception as e:
                    # Skip malformed entries but continue processing
                    log(f"[ExtractionAgent] Skipping malformed entry: {str(e)}")
                    continue

            # Check if extraction produced results
            if not self.extracted_data:
                log("[ExtractionAgent] No valid entries extracted")
                env.update("extracted_data", None)
                return

            # Store structured data in environment
            env.update("extracted_data", self.extracted_data)

            # Log success with count
            log(f"[ExtractionAgent] Extracted {len(self.extracted_data)} records")

        except Exception as e:
            # Catch unexpected errors
            handle_error("ExtractionAgent", e)

            # Ensure system consistency
            env.update("extracted_data", None)
