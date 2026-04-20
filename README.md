# BDI Multi-Agent Academic Research System

## Overview

This project implements a multi-agent academic research system based on the Belief–Desire–Intention (BDI) model. The system retrieves research papers from the ArXiv API, processes and filters them based on relevance, and stores the results in a structured JSON format.

The architecture follows a modular agent-based design, where each agent performs a specific task and communicates through a shared environment (blackboard).

---

## System Architecture

The system consists of four specialised agents:

* SearchAgent – retrieves raw data from the ArXiv API
* ExtractionAgent – parses XML and extracts structured records
* ProcessingAgent – evaluates relevance using scoring and adaptive filtering
* StorageAgent – stores processed results in JSON format

All agents follow the perceive–deliberate–act cycle defined in a shared BDI base class.

Agents communicate indirectly via a shared Environment, enabling modularity, transparency, and loose coupling.

---

## How the System Works

1. The user provides a search query at runtime.
2. SearchAgent retrieves raw XML data from the ArXiv API.
3. ExtractionAgent parses and converts the XML into structured records.
4. ProcessingAgent:
   * assigns relevance scores based on keyword matching
   * ranks results in descending order
   * applies adaptive threshold filtering
   * applies fallback if no results are found
5. StorageAgent writes the final results to a JSON file.

---

## Project Structure

Since files are submitted individually, they should be organised into the following folder structure before execution:

BDI_MULTIAGENTSYSTEM/
│
├── agents/
│   ├── extraction_agent.py
│   ├── processing_agent.py
│   ├── search_agent.py
│   ├── storage_agent.py
│
├── core/
│   ├── bdi_agent.py
│   ├── environment.py
│   ├── scoring.py
│   ├── utils.py
│
├── tests/
│   └── test_system.py
│
├── main.py
├── README.md
├── requirements.txt


## How to Run the Application
### 1. Create and Activate Virtual Environment (Recommended)

python -m venv venv

Activate the environment:

On macOS/Linux:
source venv/bin/activate

On Windows:
venv\Scripts\activate

### 2. Install Requirements

pip install -r requirements.txt

---

### 3. Run the System

python main.py

---

### 4. Enter a Query

You will be prompted to enter a search term.

Example:
machine learning

If no input is provided, a default query is used.

---

### 5. Output

* Console logs showing agent behaviour and decision-making
* A JSON file (results.json) containing filtered research papers

---

## Testing

The system includes 24 unit tests covering all major components:

* Environment (data storage and retrieval)
* Scoring (relevance calculation)
* ProcessingAgent (filtering and adaptive behaviour)
* ExtractionAgent (XML parsing)
* SearchAgent (API handling using mocking)
* StorageAgent (JSON output)
* End-to-end pipeline (full system validation)

### Run Tests

python test_system.py

---

## What Testing Validates

* Correct behaviour of each agent in isolation
* Proper data flow through the shared environment
* Robust handling of edge cases (empty input, API failures)
* Correct coordination across the full pipeline

---

## Key Features

* BDI-based reasoning (perceive–deliberate–act cycle)
* Blackboard architecture for coordination
* Score-based relevance evaluation
* Adaptive threshold filtering with bounded iterations
* Fallback mechanism for robustness
* Modular and extensible design
* Comprehensive unit testing

---

## Limitations

* Rule-based scoring does not capture semantic meaning
* Adaptive filtering is heuristic and not learning-based
* System depends on external API availability and rate limits

---

## Future Improvements

* Integrate machine learning for ranking (e.g. scikit-learn)
* Apply NLP techniques for semantic search
* Improve adaptive filtering using learned thresholds
* Add caching and retry mechanisms for API reliability

---

## References

Bratman, M.E., Israel, D.J. and Pollack, M.E. (1988). Plans and resource-bounded practical reasoning. Computational Intelligence, 4(3), pp.349–355. doi:https://doi.org/10.1111/j.1467-8640.1988.tb00284.x.
Brooks, R.A. (1991). Intelligence without representation. Artificial Intelligence, 47(1-3), pp.139–159. doi:https://doi.org/10.1016/0004-3702(91)90053-m.
Maes, P. (1991). The agent network architecture (ANA). ACM SIGART Bulletin, 2(4), pp.115–120. doi:https://doi.org/10.1145/122344.122367.
Nii, H.P. (1986). The blackboard model of problem solving. AI Magazine, 7(2), pp.38–53. doi:https://doi.org/10.1609/aimag.v7i2.537.
Rao, A.S. and Georgeff, M.P. (1995). BDI Agents: From Theory to Practice. [online] Association for the Advancement of Artificial Intelligence. Available at: https://aaai.org/papers/icmas95-042-bdi-agents-from-theory-to-practice [Accessed 25 Mar. 2026].
Russell, S.J. and Norvig, P. (2021). Artificial Intelligence: a Modern Approach. 4th ed. London: Pearson.
Sommerville, I. (2016). Software engineering. 10th ed. Boston: Pearson Education Limited.
Wooldridge, M. J. (2009). An introduction to multiagent systems (2nd ed.). John Wiley & Sons.
