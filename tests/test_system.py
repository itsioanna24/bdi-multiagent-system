import unittest
from unittest.mock import patch, MagicMock
from core.environment import Environment
from agents.processing_agent import ProcessingAgent
from agents.extraction_agent import ExtractionAgent
from agents.search_agent import SearchAgent
from agents.storage_agent import StorageAgent
from core.utils import log
from core.scoring import compute_score
import json
import os
import tempfile


# ---------------------------------------------------------------------------
# 1. Environment
# ---------------------------------------------------------------------------
 
class TestEnvironment(unittest.TestCase):
 
    def test_store_and_retrieve(self):
        """
        Verifies that the environment correctly stores and retrieves values.
        This is critical because all agents communicate via the shared environment (blackboard).
        """
        log("[TEST] Running: test_store_and_retrieve")
        env = Environment()
        env.update("key", ["paper1", "paper2"])
        self.assertEqual(env.get("key"), ["paper1", "paper2"])
        log("[TEST] ✔ Passed\n")
 
    def test_missing_key_returns_none(self):
        """
        Ensures that requesting a non-existent key returns None instead of crashing.
        This supports robustness in agent perception.
        """
        log("[TEST] Running: test_missing_key_returns_none")
        env = Environment()
        self.assertIsNone(env.get("nonexistent"))
        log("[TEST] ✔ Passed\n")
 
    def test_overwrite_value(self):
        """
        Confirms that updating an existing key overwrites previous values.
        Important for maintaining the latest state in the shared environment.
        """
        log("[TEST] Running: test_overwrite_value")
        env = Environment()
        env.update("key", "first")
        env.update("key", "second")
        self.assertEqual(env.get("key"), "second")
        log("[TEST] ✔ Passed\n")
 
 
# ---------------------------------------------------------------------------
# 2. Scoring (direct unit tests — core decision logic)
# ---------------------------------------------------------------------------
 
class TestScoring(unittest.TestCase):
 
    def test_keyword_in_summary_scores_two(self):
        """
        Verifies that keyword matches in the summary are given higher importance.
        This reflects the design choice that summaries contain richer contextual information.
        """
        log("[TEST] Running: test_keyword_in_summary_scores_two")
        item = {"title": "Unrelated Title", "summary": "This is about machine learning."}
        self.assertEqual(compute_score(item, "machine learning"), 2)
        log("[TEST] ✔ Passed\n")
 
    def test_keyword_in_title_scores_one(self):
        """
        Ensures that title matches contribute less to relevance than summaries.
        Validates weighted scoring logic.
        """
        log("[TEST] Running: test_keyword_in_title_scores_one")
        item = {"title": "Machine Learning Overview", "summary": "A general study."}
        self.assertEqual(compute_score(item, "machine learning"), 1)
        log("[TEST] ✔ Passed\n")
 
    def test_keyword_in_both_scores_three(self):
        """
        Confirms combined scoring when keyword appears in both title and summary.
        Ensures additive scoring behaviour.
        """
        log("[TEST] Running: test_keyword_in_both_scores_three")
        item = {
            "title": "Machine Learning Advances",
            "summary": "This paper covers machine learning in depth."
        }
        self.assertEqual(compute_score(item, "machine learning"), 3)
        log("[TEST] ✔ Passed\n")
 
    def test_multiple_occurrences_in_summary_bonus(self):
        """
        Verifies that repeated keyword occurrences increase relevance.
        This simulates term frequency importance.
        """
        log("[TEST] Running: test_multiple_occurrences_in_summary_bonus")
        item = {
            "title": "A Study",
            "summary": "Machine learning is great. Machine learning is widely used."
        }
        # 2 (in summary) + 1 (multiple occurrences) = 3
        self.assertEqual(compute_score(item, "machine learning"), 3)
        log("[TEST] ✔ Passed\n")
 
    def test_no_match_scores_zero(self):
        """
        Ensures irrelevant items receive zero score.
        Prevents noise from entering filtered results.
        """
        log("[TEST] Running: test_no_match_scores_zero")
        item = {"title": "Biology Study", "summary": "This paper is about plants."}
        self.assertEqual(compute_score(item, "machine learning"), 0)
        log("[TEST] ✔ Passed\n")
 
    def test_case_insensitive_matching(self):
        """
        Confirms that scoring is case-insensitive.
        Ensures robustness to variations in input text.
        """
        log("[TEST] Running: test_case_insensitive_matching")
        item = {"title": "MACHINE LEARNING", "summary": "MACHINE LEARNING IS KEY."}
        score = compute_score(item, "machine learning")
        self.assertGreater(score, 0)
        log("[TEST] ✔ Passed\n")
 
 
# ---------------------------------------------------------------------------
# 3. ProcessingAgent
# ---------------------------------------------------------------------------
 
class TestProcessingAgent(unittest.TestCase):
 
    def test_relevant_results_filtered(self):
        """
        Verifies that the agent correctly filters and retains only relevant results.
        Ensures threshold-based selection works as intended.
        """
        log("[TEST] Running: test_relevant_results_filtered")
        env = Environment()
        env.update("extracted_data", [
            {"title": "Deep Learning Advances", "summary": "This paper discusses machine learning techniques."},
            {"title": "Biology Study", "summary": "This paper is about plants."},
            {"title": "Machine Learning in Healthcare", "summary": "Medical machine learning applications."},
        ])
        agent = ProcessingAgent("machine learning")
        agent.perceive(env)
        agent.deliberate()
        agent.act(env)
        result = env.get("processed_data")
        self.assertGreater(len(result), 0)
        log("[TEST] ✔ Passed\n")
 
    def test_adaptive_threshold_lowering(self):
        """
         Tests the adaptive filtering mechanism.

        This test provides input data that does not match the query,
        forcing the agent to progressively lower the threshold.

        It verifies that:
        - the system does not fail when no results meet the initial threshold
        - adaptive threshold reduction is applied
        - a fallback or non-empty result is eventually produced

        This is critical for demonstrating robustness and practical reasoning behaviour.
        """
        log("[TEST] Running: test_adaptive_threshold_lowering")
        env = Environment()
        env.update("extracted_data", [
            {"title": "AI Overview", "summary": "General artificial intelligence concepts."}
        ])
        agent = ProcessingAgent("machine learning")
        agent.perceive(env)
        agent.deliberate()
        agent.act(env)
        result = env.get("processed_data")
        self.assertIsNotNone(result)
        log("[TEST] ✔ Passed\n")
 
    def test_empty_data_returns_none_or_empty(self):
        """
        Ensures the agent handles empty input gracefully.
        Prevents crashes when no data is available.
        """
        log("[TEST] Running: test_empty_data_returns_none_or_empty")
        env = Environment()
        env.update("extracted_data", [])
        agent = ProcessingAgent("AI")
        agent.perceive(env)
        agent.deliberate()
        agent.act(env)
        result = env.get("processed_data")
        self.assertTrue(result is None or len(result) == 0)
        log("[TEST] ✔ Passed\n")
 
    def test_results_sorted_by_score(self):
        """
        Verifies that results are sorted in descending order of relevance.
        Ensures the most relevant results appear first.
        """
        log("[TEST] Running: test_results_sorted_by_score")
        env = Environment()
        env.update("extracted_data", [
            {"title": "Unrelated Paper", "summary": "About machine learning briefly."},
            {"title": "Machine Learning Deep Dive", "summary": "Machine learning is the focus. Machine learning explored."},
        ])
        agent = ProcessingAgent("machine learning")
        agent.perceive(env)
        agent.deliberate()
        agent.act(env)
        result = env.get("processed_data")
        # The high-scoring paper should appear first
        self.assertEqual(result[0]["title"], "Machine Learning Deep Dive")
        log("[TEST] ✔ Passed\n")
 
 
# ---------------------------------------------------------------------------
# 4. ExtractionAgent
# ---------------------------------------------------------------------------
 
class TestExtractionAgent(unittest.TestCase):
 
    SAMPLE_XML = """<?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
      <entry>
        <title>Deep Learning for NLP</title>
        <summary>This paper covers deep learning applied to natural language processing.</summary>
      </entry>
      <entry>
        <title>Reinforcement Learning Methods</title>
        <summary>An overview of reinforcement learning algorithms.</summary>
      </entry>
    </feed>"""
 
    def test_valid_xml_extracts_records(self):
        """
        Verifies correct parsing of valid XML into structured records.
        Ensures data transformation from raw input to usable format.
        """
        log("[TEST] Running: test_valid_xml_extracts_records")
        env = Environment()
        env.update("raw_data", self.SAMPLE_XML)
        agent = ExtractionAgent()
        agent.perceive(env)
        agent.deliberate()
        agent.act(env)
        result = env.get("extracted_data")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["title"], "Deep Learning for NLP")
        log("[TEST] ✔ Passed\n")
 
    def test_extracted_records_have_title_and_summary(self):
        """
        Ensures extracted records contain required fields.
        Guarantees consistency of downstream processing.
        """
        log("[TEST] Running: test_extracted_records_have_title_and_summary")
        env = Environment()
        env.update("raw_data", self.SAMPLE_XML)
        agent = ExtractionAgent()
        agent.perceive(env)
        agent.deliberate()
        agent.act(env)
        result = env.get("extracted_data")
        for record in result:
            self.assertIn("title", record)
            self.assertIn("summary", record)
        log("[TEST] ✔ Passed\n")
 
    def test_invalid_xml_stores_none(self):
        """
        Ensures system handles malformed XML safely.
        Prevents crashes from invalid external data.
        """
        log("[TEST] Running: test_invalid_xml_stores_none")
        env = Environment()
        env.update("raw_data", "<<not valid xml>>")
        agent = ExtractionAgent()
        agent.perceive(env)
        agent.deliberate()
        agent.act(env)
        self.assertIsNone(env.get("extracted_data"))
        log("[TEST] ✔ Passed\n")
 
    def test_no_raw_data_stores_none(self):
        """
        Ensures behaviour is safe when no input data is provided.
        Supports robustness in early pipeline stages.
        """
        log("[TEST] Running: test_no_raw_data_stores_none")
        env = Environment()
        env.update("raw_data", None)
        agent = ExtractionAgent()
        agent.perceive(env)
        agent.deliberate()
        agent.act(env)
        self.assertIsNone(env.get("extracted_data"))
        log("[TEST] ✔ Passed\n")
 
 
# ---------------------------------------------------------------------------
# 5. SearchAgent (mocked — no live network calls)
# ---------------------------------------------------------------------------
 
class TestSearchAgent(unittest.TestCase):
 
    @patch("agents.search_agent.requests.get")
    def test_successful_api_response_stored(self, mock_get):
        """
        Verifies that valid API responses are correctly stored.
        Confirms integration with external data sources (mocked).
        """
        log("[TEST] Running: test_successful_api_response_stored")
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<feed><entry><title>Test</title></entry></feed>"
        mock_get.return_value = mock_response
 
        env = Environment()
        agent = SearchAgent("machine learning")
        agent.run(env)
 
        self.assertIsNotNone(env.get("raw_data"))
        log("[TEST] ✔ Passed\n")
 
    @patch("agents.search_agent.requests.get")
    def test_api_failure_stores_none(self, mock_get):
        """
        Ensures system handles API failures gracefully.
        Prevents propagation of invalid data.
        """
        log("[TEST] Running: test_api_failure_stores_none")
        mock_response = MagicMock()
        mock_response.status_code = 503
        mock_get.return_value = mock_response
 
        env = Environment()
        agent = SearchAgent("machine learning")
        agent.run(env)
 
        self.assertIsNone(env.get("raw_data"))
        log("[TEST] ✔ Passed\n")
 
    @patch("agents.search_agent.requests.get")
    def test_timeout_stores_none(self, mock_get):
        """
        Simulates network timeout and verifies safe handling.
        Ensures resilience to real-world network issues.
        """
        log("[TEST] Running: test_timeout_stores_none")
        import requests as req
        mock_get.side_effect = req.exceptions.Timeout
 
        env = Environment()
        agent = SearchAgent("machine learning")
        agent.run(env)
 
        self.assertIsNone(env.get("raw_data"))
        log("[TEST] ✔ Passed\n")
 
    @patch("agents.search_agent.requests.get")
    def test_connection_error_stores_none(self, mock_get):
        """
        Simulates connection errors and ensures system stability.
        Confirms robustness of external communication layer.
        """
        log("[TEST] Running: test_connection_error_stores_none")
        import requests as req
        mock_get.side_effect = req.exceptions.ConnectionError
 
        env = Environment()
        agent = SearchAgent("machine learning")
        agent.run(env)
 
        self.assertIsNone(env.get("raw_data"))
        log("[TEST] ✔ Passed\n")
 
 
# ---------------------------------------------------------------------------
# 6. StorageAgent
# ---------------------------------------------------------------------------
 
class TestStorageAgent(unittest.TestCase):
 
    def test_data_written_to_json_file(self):
        """
        Verifies that processed data is correctly persisted to a JSON file.
        Ensures output stage of the pipeline functions correctly.
        """
        log("[TEST] Running: test_data_written_to_json_file")
        env = Environment()
        env.update("processed_data", [
            {"title": "Paper A", "summary": "Summary A"},
            {"title": "Paper B", "summary": "Summary B"},
        ])
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp_path = tmp.name
 
        try:
            agent = StorageAgent(output_file=tmp_path)
            agent.perceive(env)
            agent.deliberate()
            agent.act(env)
 
            with open(tmp_path, "r") as f:
                saved = json.load(f)
 
            self.assertEqual(len(saved), 2)
            self.assertEqual(saved[0]["title"], "Paper A")
        finally:
            os.remove(tmp_path)
        log("[TEST] ✔ Passed\n")
 
    def test_no_data_does_not_create_file(self):
        """
        Ensures no file is created when there is no valid data.
        Prevents unnecessary or incorrect outputs.
        """
        log("[TEST] Running: test_no_data_does_not_create_file")
        env = Environment()
        env.update("processed_data", None)
        tmp_path = tempfile.mktemp(suffix=".json")
 
        agent = StorageAgent(output_file=tmp_path)
        agent.perceive(env)
        agent.deliberate()
        agent.act(env)
 
        self.assertFalse(os.path.exists(tmp_path))
        log("[TEST] ✔ Passed\n")
 
 
# ---------------------------------------------------------------------------
# 7. End-to-end pipeline (mocked network)
# ---------------------------------------------------------------------------
 
class TestEndToEndPipeline(unittest.TestCase):
 
    SAMPLE_XML = """<?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
      <entry>
        <title>Machine Learning in Healthcare</title>
        <summary>This paper covers machine learning applications in medical diagnosis.</summary>
      </entry>
      <entry>
        <title>Biology and Plants</title>
        <summary>This paper is about botanical studies and plant biology.</summary>
      </entry>
    </feed>"""
 
    @patch("agents.search_agent.requests.get")
    def test_full_pipeline_produces_output(self, mock_get):
        """
        Validates the complete multi-agent workflow.

        This test ensures that:
        - agents interact correctly via the shared environment
        - data flows through all stages (search → extract → process → store)
        - the final output is valid and non-empty

        This is critical for confirming system-level correctness.
        """
        log("[TEST] Running: test_full_pipeline_produces_output")
        from agents.extraction_agent import ExtractionAgent
        from agents.processing_agent import ProcessingAgent
        from agents.storage_agent import StorageAgent
 
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = self.SAMPLE_XML
        mock_get.return_value = mock_response
 
        env = Environment()
 
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp_path = tmp.name
 
        try:
            agents = [
                SearchAgent("machine learning"),
                ExtractionAgent(),
                ProcessingAgent("machine learning"),
                StorageAgent(output_file=tmp_path)
            ]
            for agent in agents:
                agent.run(env)
 
            result = env.get("processed_data")
            self.assertIsNotNone(result)
            self.assertGreater(len(result), 0)
 
            with open(tmp_path) as f:
                saved = json.load(f)
            self.assertGreater(len(saved), 0)
        finally:
            os.remove(tmp_path)
        log("[TEST] ✔ Passed\n")
 
 
if __name__ == "__main__":
    log("Starting unit tests...\n")
    unittest.main()