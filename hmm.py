#first index - kill count
#second index - win/lose
WIN = 0
LOSE = 1
p_obs_given_outcome = [
	[0.1,0.2],
	[0.1,0.2]
]

#first index - first outcome
#second index - secon outcome
p_outcome_given_prev_outcome = [
	[0.1, 0,2],
	[0.23, 0.5]
]

OUTCOME_TYPES = [WIN, LOSE] 
OBSERVATION_TYPES = [0, 1] # only doing kill range of 1 to 2 for now
"""
Gets the probability of a particular future observation given the outcome
"""
def get_obs_given_outcome(obs):
	total = 0
	for last_outcome in OUTCOME_TYPES:
		p_outcome_given_all_prev_obs = get_outcome_given_all_prev_obs(last_outcome)
		for next_outcome in OUTCOME_TYPES:
			hidden_step =  p_obs_given_outcome[obs][next_outcome]
			state_transition_step = p_outcome_given_prev_outcome[next_outcome][last_outcome]
			total += (hidden_step * state_transition_step * p_outcome_given_all_prev_obs)

	return total

def get_outcome_given_all_prev_obs(outcome):
	#return some shit
	return 0.3


def run():
	#get probabiliy of each observation
	prob_for_obs = {o: get_obs_given_outcome(o) for o in OBSERVATION_TYPES}
	print prob_for_obs

if __name__ == "__main__":
	run()

