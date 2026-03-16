from logic_utils import check_guess, update_score, parse_guess, get_range_for_difficulty


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


# ===== Challenge 1: Advanced Edge-Case Testing =====

# --- parse_guess edge cases ---

def test_parse_guess_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_guess_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_guess_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_float_string():
    # Entering "3.7" should be parsed as int 3
    ok, value, err = parse_guess("3.7")
    assert ok is True
    assert value == 3
    assert err is None


def test_parse_guess_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_parse_guess_negative_number():
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5
    assert err is None


def test_parse_guess_special_characters():
    ok, value, err = parse_guess("!@#")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


# --- check_guess edge cases ---

def test_check_guess_boundary_off_by_one():
    # Guess is 1 away from secret
    outcome, message = check_guess(51, 50)
    assert outcome == "Too High"


def test_check_guess_large_numbers():
    outcome, message = check_guess(99999, 1)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_check_guess_both_same_type():
    # Both int — should never hit TypeError
    outcome, message = check_guess(25, 25)
    assert outcome == "Win"


# --- update_score edge cases ---

def test_score_win_first_attempt():
    # Winning on attempt 1 should give max points: 100 - 10*1 = 90
    score = update_score(0, "Win", 1)
    assert score == 90


def test_score_win_late_attempt_floors_at_10():
    # Winning on attempt 20: 100 - 200 = -100, but floors at 10
    score = update_score(0, "Win", 20)
    assert score == 10


def test_score_too_low_deducts():
    score = update_score(50, "Too Low", 1)
    assert score == 45


def test_score_does_not_go_below_with_repeated_wrong():
    # Multiple wrong guesses can make score negative
    score = 0
    for i in range(5):
        score = update_score(score, "Too Low", i + 1)
    assert score == -25


# --- get_range_for_difficulty edge cases ---

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20


def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100


def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 200


def test_unknown_difficulty_defaults():
    low, high = get_range_for_difficulty("Unknown")
    assert low == 1
    assert high == 100
