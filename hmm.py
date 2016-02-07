#first index - kill count
#second index - win/lose
WIN = 0
LOSE = 1

#all the uncapitalised globals will be generated from historical data.
#just mocking out some crap for now
p_obs_given_outcome = [
	[0,0],
	[0,0],
	[0,0.14],
	[0.14,0.14],
	[0.14,0],
	[0,0.14],
	[0.14,0],
	[0,0],
	[0.14,0],
	[0,0],
]

#first index - first outcome
#second index - secon outcome
p_outcome_given_prev_outcome = [
	[0.6, 0.4],
	[0.5, 0.5]
]

p_outcome = [0.57, 0.43]


#obs = [0.6, 0.3, 0.4, 0.7, 0.5, 0.9]
obs = [5, 2, 3, 6, 4, 8]


OUTCOME_TYPES = [WIN, LOSE] 
OBSERVATION_TYPES = [0,1,2,3,4,5,6,7,8,9] # only doing kill range of 1 to 2 for now
GAME_COUNT = len(obs)
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

	ans = [
			p_outcome_given_prev_outcome[outcome][prev_outcome]
			*
			forward(prev_outcome, t-1)
			for prev_outcome in OUTCOME_TYPES
	]

	return p_obs_given_outcome[obs[t-1]][outcome] * sum(ans)


def backward(outcome, t, max_t):
	if t == max_t:
		return 1

	ans = [
			p_obs_given_outcome[obs[t-1]][next_outcome]
			*
			p_outcome_given_prev_outcome[next_outcome][outcome]
			*
			backward(outcome, t+1, max_t)

			for next_outcome in OUTCOME_TYPES
		]

	return sum(ans)

def run():
	#get probabiliy of each observation
	prob_for_obs = {o: get_obs_given_outcome(o, GAME_COUNT) for o in OBSERVATION_TYPES}
	print prob_for_obs # expected = {0: 0.2999999999999996, 1: 0.39999999999999947}

if __name__ == "__main__":
	run()

