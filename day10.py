import requests
import time
from abc import ABC, abstractmethod

from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpInteger, LpStatus


class Clock:
    def __init__(self):
        self.start_time = 0
    def __enter__(self):
        self.start_time = time.time()
    def __exit__(self, *args, **kwargs):
        stop_time = time.time()
        print(f"[i] Took {int(stop_time - self.start_time) // 60} min. and {int(stop_time - self.start_time) % 60}s in total")


class AocMeta(ABC):

	def __init__(self, day, cookies):
		self.session = requests.Session()
		self.day = day		
		
		requests.utils.add_dict_to_cookiejar(self.session.cookies, cookies)
	
	
	@abstractmethod
	def process_input(self, inp: str) -> dict:
		...
		   
		    
	@abstractmethod
	def first_star(self, inp):
		...
		    
		    
	@abstractmethod
	def second_star(self, inp):
		...
	
	def get_input(self) -> dict:
		if self.session is None:
			raise ValueError("Improperly initialized")
			
		resp = self.session.get(f"https://adventofcode.com/2025/day/{self.day}/input")
		result = resp.content.decode()
		result = self.process_input(result)
		return result

	def submit_answer(self, level, answer):
		while True:
		    resp = self.session.post(f"https://adventofcode.com/2025/day/{self.day}/answer", data={"level": level, "answer": answer})
		    content = resp.content.decode()
		    if "That's not the right answer" in content:
		        return False
		    if "You gave an answer too recently" in content:
		        print("[*] Response sent too soon after each other")
		        time.sleep(30)
		        continue
		    return True
		
		
	def run(self):
		inp = self.get_input()
		first_answer = self.first_star(inp)
		correct = self.submit_answer(level=1, answer=first_answer)
		print(f"[*] First star result: {first_answer} ... {'correct' if correct else 'incorrect'}")
		if not correct:
			return False
			
		time.sleep(10)
		
		second_answer = self.second_star(inp)
		correct = self.submit_answer(level=2, answer=second_answer)
		print(f"[*] Second star result: {second_answer} ... {'correct' if correct else 'incorrect'}")
		
		return correct


class Solution(AocMeta):

	def process_input(self, inp: str) -> dict:
		machines = []
		for machine in inp.split("\n"):
			machine = machine.strip()
			if len(machine) == 0:
				continue
		
			target_state, machine = machine.split(" ", 1)
			buttons, joltage = machine.split("{")
			buttons = [tuple([int(x) for x in button.strip()[1:-1].split(",")]) for button in buttons.split(" ") if len(button.strip()) != 0]
			joltage = [int(x) for x in joltage.strip()[:-1].split(",")]
			target_state = list(target_state[1:-1])
			machines.append({"target_state": tuple(target_state), "buttons": buttons, "target_joltage": tuple(joltage)})
		return {"machines": machines}

	def _transform(self, button, state):
		resulting_state = list(state)
		for index in button:
			resulting_state[index] = "." if resulting_state[index] == "#" else "#"
		return tuple(resulting_state)

	def first_star(self, inp):
		already_seen = set()
		def breadth_first(target_state: list, buttons: list, depth: int, states: set):
			next_states = set()
			for state in states:
				for button in buttons:
					new_state = self._transform(state=state, button=button)
					if new_state in already_seen:
						continue
					if new_state == target_state:
						return depth
					next_states.add(new_state)
					already_seen.add(new_state)
			return breadth_first(target_state=target_state, buttons=buttons, depth=depth + 1, states=next_states)

		machines = inp["machines"]
		minimal_depths = []

		for machine in machines:
			target_state, buttons = machine["target_state"], machine["buttons"]

			initial_state = tuple(list("." * len(target_state)))
			already_seen.add(initial_state)
			minimal_depths.append(breadth_first(target_state=target_state, buttons=buttons, depth=1, states={initial_state}))
			already_seen.clear()

		return sum(minimal_depths)


	def second_star(self, inp):		

		def min_presses(buttons, counters):
			prob = LpProblem("ButtonPresses", LpMinimize)

			# Button variables
			x = [LpVariable(f"x{i}", lowBound=0, cat=LpInteger) for i in range(len(buttons))]

			# Minimize total presses of the buttons 
			prob += lpSum(x)

			# Add constraints tht sum of all buttons that change index j have to be sme as counter
			for j in range(len(counters)):
				prob += lpSum(x[i] for i, b in enumerate(buttons) if j in b) == counters[j]

			# Run the SAT solver
			status = prob.solve()

			# Solution wasnt found
			if LpStatus[status] != "Optimal":
				raise ValueError()

			# Solution found ... get how many times was each button pressed
			presses = [int(x[i].varValue) for i in range(len(buttons))]
			total = sum(presses)
			return total

		machines = inp["machines"]
		minimal_depths = []

		for machine in machines:
			target_joltage, buttons = machine["target_joltage"], machine["buttons"]

			minimal_depth = min_presses(buttons=buttons, counters=list(target_joltage))
			minimal_depths.append(minimal_depth)

		return sum(minimal_depths)
			



def main():
	day = "10"
	cookies = {"session": "<SESSION_ID>"}
	
	solution = Solution(day=day, cookies=cookies)
		
	with Clock():
		solution.run()



if __name__ == "__main__":
    main()
