# Disaster Rescue Multi-Agent System

This repository contains a comparative implementation of a Multi-Agent System (MAS) designed to coordinate autonomous rescue robots during disaster scenarios. It demonstrates two distinct artificial intelligence paradigms to solve the same spatial task allocation and routing problem: 
1. **Modern Generative AI:** An LLM-based multi-agent architecture utilizing Prompt Engineering.
2. **Symbolic AI:** A Knowledge-Based system utilizing First-Order Logic (FOL) and Heuristic Search.

## Repository Structure

* `llm-based-agents/`: Contains the LLM-driven implementation using the Google Gemini API.
* `fol-based-agents/`: Contains the Symbolic AI implementation using formal logic and heuristic search optimization.

---

## Approach 1: LLM-Based Multi-Agent System
Located in `llm-based-agents/`

This module leverages the Google Gemini API to orchestrate an autonomous task allocation pipeline using three communicating agents[cite: 2]. The system communicates via strict JSON outputs to maintain programmatic reliability[cite: 2, 3].

* **Planner Agent:** Analyzes tasks (e.g., rescue victim, clear debris, map building) and generates an execution sequence based on priority levels and spatial costs[cite: 2, 3].
* **Assignment Agent:** Maps the sorted tasks to the available robots strictly based on their hardware capability sets[cite: 3].
* **Critic Agent:** Audits the proposed assignments against system rules and requests revisions if any capability mismatches are detected, ensuring a flawless operation before execution[cite: 3].
* **Informed Search Integration:** Resolves priority conflicts by utilizing the Manhattan Distance heuristic, effectively optimizing time and speed by prioritizing closer targets[cite: 3].
* **Execution & Cost:** Calculates the final operational time cost using the formula: `Estimated Time = Distance / Robot Speed`[cite: 3].

---

## Approach 2: Knowledge-Based System via First-Order Logic (FOL)
Located in `fol-based-agents/`

This module shifts from generative text inference to strict mathematical and logical constraint satisfaction[cite: 5]. It models the environment and operational conditions using formal FOL predicates and axioms[cite: 5].

* **Hard Constraints Satisfied:**
  * **Exact Assignment:** Every task is assigned to exactly one robot[cite: 5].
  * **Capability Matching:** Robots only execute tasks compatible with their hardware profiles[cite: 5].
  * **Priority Ordering:** Higher-priority tasks are strictly scheduled before lower-priority tasks[cite: 5].
* **Heuristic Cost Optimization:** The Assignment Agent explores the state-space matrix to minimize the global operational cost, defined as `Cost(r,t) = Distance(r,t) / Speed(r)`[cite: 5].
* **Sequential Constraints (Dynamic Tracking):** Unlike static assignment models, this system dynamically updates robot coordinates after each completed task to accurately calculate the cost of sequential deployments[cite: 5].
* **Performance Analysis:** The Critic Agent calculates both the Actual Cost and the Theoretical Optimal Cost (Lower Bound) to compute a final System Operational Efficiency ratio, successfully demonstrating the trade-off between strict logical safety guarantees and physical efficiency[cite: 4, 5].

---

## Tech Stack
* **Language:** Python
* **LLM Integration:** Google GenAI SDK (gemini-2.5-flash)[cite: 2]
* **Algorithms:** First-Order Logic (FOL), Manhattan Distance Heuristics, Informed Search
* **Environment:** Jupyter Notebook, standard Python execution

## How to Run
1. Navigate to the desired approach directory (`llm-based-agents` or `fol-based-agents`).
2. For the LLM approach, ensure a valid Gemini API key is configured in the script.
3. Run the Python script (`main.py`) or execute the Jupyter Notebook (`fol_heuristic_search.ipynb`) to view the complete simulation, agent communication, and final cost evaluation logs.
