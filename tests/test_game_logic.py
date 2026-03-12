from logic_utils import check_guess, update_score


# Existing starter tests (fixed to unpack tuples from check_guess)

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# Bug fix tests — targeting the specific bugs we fixed

def test_too_high_hint_says_lower():
    # FixMe test: hints were swapped — "Too High" should say "LOWER", not "HIGHER"
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message


def test_too_low_hint_says_higher():
    # FixMe test: hints were swapped — "Too Low" should say "HIGHER", not "LOWER"
    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message


def test_score_too_high_even_attempt_deducts():
    # FixMe test: "Too High" on even attempts was giving +5 instead of -5
    score = update_score(100, "Too High", 2)
    assert score == 95


def test_score_too_high_odd_attempt_deducts():
    # "Too High" on odd attempts should also deduct 5
    score = update_score(100, "Too High", 3)
    assert score == 95
