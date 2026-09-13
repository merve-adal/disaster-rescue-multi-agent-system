"""
Project: Disaster Rescue Operation Simulation with an LLM-Based Multi-Agent System
Merve ADALI 
Student ID: 211805049
Description: Coordinates autonomous rescue robots using LLM agents (Planner, Assignment, Critic) 
and Informed Search (Manhattan Distance) to optimize task assignment and priority handling.
"""
import random
import json
from google import genai
from google.genai import types

# 1. Task Types and Priorities
task_types = {
    "rescue victim": "high",
    "deliver medicine": "medium",
    "clear debris": "medium",
    "map building": "low"
}

# 2. Robot Capabilities, Speed Classes, and Speed Multipliers
robot_specs = {
    "search and mapping": {"speed_class": "fast", "speed_val": 3},
    "medical support": {"speed_class": "medium", "speed_val": 2},
    "heavy debris removal": {"speed_class": "slow", "speed_val": 1}
}

# 3. Manhattan Distance Calculator (Informed Search: h(n))
def calculate_heuristic(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# 4. Disaster Area Generation
def generate_disaster_area(num_tasks=5):
    tasks = []
    for i in range(num_tasks):
        t_type = random.choice(list(task_types.keys()))
        loc = (random.randint(0, 10), random.randint(0, 10))
        distance = calculate_heuristic((0,0), loc)
        
        tasks.append({
            "id": f"T{i+1}",
            "type": t_type,
            "priority": task_types[t_type],
            "location": loc,
            "distance": distance
        })
    
    robots = [
        {"id": "R1", "capability": "search and mapping", "speed": "fast", "speed_val": 3, "location": (0,0)},
        {"id": "R2", "capability": "medical support", "speed": "medium", "speed_val": 2, "location": (0,0)},
        {"id": "R3", "capability": "heavy debris removal", "speed": "slow", "speed_val": 1, "location": (0,0)}
    ]
    return tasks, robots

# 5. LLM Agent Class
class RescueSystemAgent:
    def __init__(self, name, role_instruction):
        self.name = name
        self.role = role_instruction
        self.client = genai.Client(api_key="AIzaSyAp0RxZziUlzVPneP0WVepMsYMm9kyDkGE") # Your API Key

    def process(self, input_data):
        prompt = f"Input Data: {input_data}"
        response = self.client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.role,
                temperature=0.0 # Using 0.0 for strict and mathematical logic
            )
        )
        return response.text

# 6. Agent Roles 
planner_role = """
You are a Planner Agent. Your task is to analyze the tasks in the disaster area and create an execution plan (ordered list).
Rules:
1. Priority Order: 'high' must be at the top, 'medium' in the middle, and 'low' at the bottom.
2. Efficiency: IF two tasks have the same priority, place the one with the LOWER 'distance' value (closer one) higher in the list.
Provide the output ONLY as a valid JSON list containing the FULL task dictionaries (keep all properties like id, type, priority, location, and distance). Do not just output the IDs. Do not use Markdown.
"""

assignment_role = """
You are an Assignment Agent. You will assign the tasks ordered by the Planner to the robots.
Rules (Capability Matching):
- Assign 'map building' tasks -> to the 'search and mapping' robot (R1)
- Assign 'rescue victim' and 'deliver medicine' tasks -> to the 'medical support' robot (R2)
- Assign 'clear debris' tasks -> to the 'heavy debris removal' robot (R3).
Provide the output ONLY as a JSON format dictionary: {"T1": "R2", "T2": "R3" ...}. Do not use Markdown.
"""

critic_role = """
You are a Critic Agent. You will audit the assignments made by the Assignment Agent.
Rules:
1. All 'rescue victim' and 'deliver medicine' tasks must strictly be assigned to R2.
2. All 'clear debris' tasks must strictly be assigned to R3.
3. All 'map building' tasks must strictly be assigned to R1.
If all assignments comply 100% with the rules, simply write "DONE".
If there is even a single mismatch, write "Revisions Required: [Reason for the error]" and request a correction.
"""

# 7. Main Coordination Loop
def start_rescue_operation():
    print("=== WORLD MODEL AND INFORMED SEARCH INITIALIZATION ===\n")
    tasks, robots = generate_disaster_area()
    
    print("Tasks (With Calculated Distances):")
    print(json.dumps(tasks, indent=2, ensure_ascii=False))
    print("\n" + "="*50 + "\n")
    
    planner = RescueSystemAgent("Planner", planner_role)
    assignment = RescueSystemAgent("Assignment", assignment_role)
    critic = RescueSystemAgent("Critic", critic_role)
    
    print("--- 1. PLANNER AGENT: CREATING STRATEGY ---")
    plan = planner.process(json.dumps(tasks, ensure_ascii=False))
    print(f"Planned Sequence:\n{plan}\n")
    
    print("--- 2. ASSIGNMENT AGENT: DISTRIBUTING TASKS ---")
    assign_data = f"Plan: {plan}\nRobots: {json.dumps(robots, ensure_ascii=False)}"
    current_assignment = assignment.process(assign_data)
    print(f"Proposed Assignments:\n{current_assignment}\n")
    
    print("--- 3. CRITIC AGENT: AUDIT AND APPROVAL ---")
    max_rounds = 3
    for i in range(max_rounds):
        critic_data = f"Robots: {json.dumps(robots, ensure_ascii=False)}\nTasks: {plan}\nAssignments: {current_assignment}"
        feedback = critic.process(critic_data)
        print(f"Critic Feedback (Round {i+1}): {feedback}\n")
        
        if "DONE" in feedback.upper():
            print(">>> SYSTEM APPROVAL RECEIVED! RESCUE OPERATION INITIATED. <<<\n")
            
            # --- 4. EXECUTION PHASE ---
            print("=== 4. EXECUTION PHASE (ROBOTS ON MISSION) ===")
            try:
                plan_list = json.loads(plan)
                assignment_dict = json.loads(current_assignment)
                
                for task in plan_list:
                    t_id = task["id"]
                    t_type = task["type"]
                    r_id = assignment_dict.get(t_id)
                    
                    if r_id:
                        # Calculating duration by finding the robot's speed (Distance / Speed)
                        r_speed = next((r["speed_val"] for r in robots if r["id"] == r_id), 1)
                        time_taken = task["distance"] / r_speed
                        
                        print(f"-> Robot {r_id} deployed to coordinates {task['location']}.")
                        print(f"   [Action]: {t_type} (Priority: {task['priority']})")
                        print(f"   [Cost]: Distance {task['distance']} units, Estimated Time: {time_taken:.1f} time units.\n")
            except json.JSONDecodeError:
                print("Error: Execution phase skipped as agent output was not in strict JSON format.")
                
            print("=== ALL TASKS SUCCESSFULLY COMPLETED! ===")
            break
        else:
            print("--- REVISION REQUESTED, RE-ASSIGNING ---")
            rev_req = f"Previous Faulty Assignment: {current_assignment}\nCriticism: {feedback}\nPlease provide only a JSON dictionary complying with the rules."
            current_assignment = assignment.process(rev_req)
            print(f"Corrected Assignments:\n{current_assignment}\n")

if __name__ == "__main__":
    start_rescue_operation()