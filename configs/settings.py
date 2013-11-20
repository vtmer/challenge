#coding: utf-8

SESSION_COOKIE_NAME = 'dontdeleteme'


# session token key generating
CHALLENGE_KEY_LENGTH = 6  # (26 + 26 + 10) ^ 6 = 56800235584
CHALLENGE_SESSION_KEY_LENGTH = 16
CHALLENGE_FIRST_QUIZ = {
    'display_name': 'hello quiz',
    'quiz_name': 'hello'
}
CHALLENGE_QUIZ_MODULE = 'challenge.quizs'
