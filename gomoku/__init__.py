from gym.envs.registration import register

register(
    id='gomoku-v0',
    entry_point='gomoku.envs:GomokuEnv',
    kwargs={},
)