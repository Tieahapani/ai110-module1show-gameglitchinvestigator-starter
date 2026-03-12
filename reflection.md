# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start
  (for example: "the secret number kept changing" or "the hints were backwards").

**Bug 1 — Hints were backwards:**
When I guessed a number lower than the secret, the game told me "Go LOWER!" instead of "Go HIGHER!", and vice versa. I expected the hints to guide me toward the correct answer, but they pointed me in the wrong direction every time. I confirmed this by opening the Developer Debug Info to see the secret number and comparing it to the hint shown.

**Bug 2 — Hints were inconsistent across attempts:**
On even-numbered attempts, the secret was silently converted from an integer to a string. This caused the comparison to use string/alphabetical ordering instead of numeric ordering, so the same guess could give different hints depending on whether it was an odd or even attempt. For example, guessing 60 when the secret was 75 would say "Go HIGHER!" on one attempt but "Go LOWER!" on the next. I expected the hints to be consistent for the same guess and secret.

**Bug 3 — Scoring was unfair and unpredictable:**
The score update logic treated "Too High" and "Too Low" guesses differently — a "Too High" guess on an even attempt actually gave +5 points (a reward for being wrong!), while "Too Low" always deducted 5 points. I expected both wrong-direction guesses to carry the same penalty. Additionally, the win bonus had an off-by-one error (`attempt_number + 1`), making the reward 10 points less than it should have been.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude Code (via VS Code extension) as my primary AI tool for this project. I gave it both `app.py` and `logic_utils.py` and asked it to identify what was wrong with the submit button.

**Correct suggestion:** Claude correctly identified that the hints in `check_guess` were swapped — "Too High" was displaying "Go HIGHER!" instead of "Go LOWER!". I verified this by opening the Developer Debug Info to see the secret number, then making a guess and comparing the hint to the actual direction I needed to go. The hint was indeed backwards.

**Misleading suggestion:** Claude initially suggested the `attempts` starting at 1 was causing the submit button to "crash," but the real user-facing issue was the swapped hints and the string conversion of the secret on even attempts. The attempts bug caused one fewer guess but didn't actually crash anything. I verified this by checking that the game still ran after the first submit — it didn't crash, it just gave wrong feedback.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was fixed by manually testing the game in the browser and using the Developer Debug Info panel to compare my guess, the secret number, and the hint displayed. If the hint pointed in the correct direction consistently across multiple attempts, I considered the hints bug fixed. For the scoring bug, I watched the score value in the debug panel after each guess to confirm that wrong guesses always deducted 5 points regardless of direction or attempt number.

For manual testing, I ran the app with the secret visible in debug mode, guessed a number I knew was too low, and confirmed the hint now said "Go HIGHER!" instead of the old broken "Go LOWER!". I repeated this on both odd and even attempts to make sure the string conversion bug was also resolved. AI helped me trace through the code logic to understand why even-numbered attempts behaved differently — it pointed out the `attempts % 2 == 0` condition that converted the secret to a string.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

The secret number would change if it were generated outside of `st.session_state`, because Streamlit re-executes the entire script from top to bottom every time the user interacts with any widget (like clicking a button or typing in an input). Without session state, a new random number would be generated on every rerun, making the game impossible to play.

I would explain Streamlit reruns to a friend like this: "Imagine every time you click a button on a webpage, the entire Python script runs again from scratch. Any variables you set are forgotten unless you store them in a special memory box called `session_state`. That memory box persists across reruns, so things like the secret number, your score, and your attempt count are remembered."

The app already used `if "secret" not in st.session_state` to only generate the secret once, which kept it stable. The key fix we made was ensuring the secret wasn't being silently modified during gameplay — on even attempts, the code was converting `st.session_state.secret` to a string before passing it to `check_guess`, which didn't change the stored value but did break comparisons.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to reuse is adding `# FixMe` comments at the exact location of each bug before fixing it. This "mark the crime scene" approach made it easy to track what was broken, communicate the issue clearly to the AI, and later review all the changes I made. It also serves as documentation for anyone reading the code later.

Next time I work with AI on a coding task, I would give it one bug at a time instead of asking it to analyze everything at once. When I asked Claude to check both files for all issues, it listed many bugs at once, which was overwhelming. Focusing on one bug per conversation keeps the fixes small and easier to verify.

This project showed me that AI-generated code can look clean and "production-ready" on the surface but still contain subtle logic errors — like swapped messages, type mismatches on certain conditions, and inconsistent scoring rules. You cannot trust AI code without actually running it and testing edge cases yourself.
