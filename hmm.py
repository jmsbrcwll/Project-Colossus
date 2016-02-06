#first index - kill count
#second index - win/lose
WIN = 0
LOSE = 1

#all the uncapitalised globals will be generated from historical data.
#just mocking out some crap for now
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

p_outcome = [0.5, 0.5]

obs = [0,1,0,1] # the number of kills from the last n games

OUTCOME_TYPES = [WIN, LOSE] 
OBSERVATION_TYPES = [0, 1] # only doing kill range of 1 to 2 for now
GAME_COUNT = 4
"""
Gets the probability of a particular future observation given the outcome
"""
def get_obs_given_outcome(obs, t):
	total = 0
	for last_outcome in OUTCOME_TYPES:
		p_outcome_given_all_prev_obs = get_outcome_given_all_prev_obs(last_outcome, t)
		for next_outcome in OUTCOME_TYPES:
			hidden_step =  p_obs_given_outcome[obs][next_outcome]
			state_transition_step = p_outcome_given_prev_outcome[next_outcome][last_outcome]
			total += (hidden_step * state_transition_step * p_outcome_given_all_prev_obs)

	return total
"""
Should perform the forward-backward algorithm to get p(outcome | observations 1:t)
"""
def get_outcome_given_all_prev_obs(outcome, t):
	num = forward(outcome, t) * backward(outcome, 1, t)
	den = sum([forward(o, t) * backward(o, 1, t) for o in OUTCOME_TYPES])
	return num / den

def forward(outcome, t):
	if t == 1:
		return p_outcome[outcome]
	
	return sum([p_outcome_given_prev_outcome[outcome][prev_outcome] * forward(prev_outcome, t-1) for prev_outcome in OUTCOME_TYPES])


def backward(outcome, t, max_t):
	if t == max_t:
		return 1

	return sum([p_obs_given_outcome[obs[t-1]][next_outcome] * p_outcome_given_prev_outcome[next_outcome][outcome] * backward(outcome, t+1, max_t) for next_outcome in OUTCOME_TYPES])

def run():
	#get probabiliy of each observation
	prob_for_obs = {o: get_obs_given_outcome(o, GAME_COUNT) for o in OBSERVATION_TYPES}
	print prob_for_obs

if __name__ == "__main__":
	run()

