# StudyPRO

A Streamlit study assistant with question analysis, image-based question input, study planning, account login, and MySQL-backed study history.

## Run locally

1. Install Python 3.10 or later and MySQL.
2. Create the schema with `1000.sql`.
3. Install dependencies with `pip install -r requirement.txt`.
4. Copy `.env.example` to `.env` and set your OpenAI and database credentials.
5. Run `streamlit run nav.py`.

The application expects `questionbank.questions`, `userdetails.app_users`, and `userdetails.study_process`. The database connection reads `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` from the environment. Set `DB_USER` to a dedicated MySQL account with only the required access to `questionbank.questions`, `userdetails.app_users`, and `userdetails.study_process`; do not run the app as MySQL root. Existing rows in `user_d` are not migrated; create an app account through the registration page. Do not commit `.env`.

## Data and privacy

The application sends typed prompts and uploaded question images to the configured OpenAI API. Review the API provider's data handling terms before using personal or sensitive material. Database credentials must be supplied locally and should not be stored in source code.

The progress chart uses daily correct and total question counts from `userdetails.study_process`. Practice a saved multiple-choice question on the Question Solver page to record one answer and update the chart. Passwords for new accounts are stored as salted PBKDF2 hashes.
