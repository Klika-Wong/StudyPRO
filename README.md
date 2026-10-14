# StudyPRO

A Streamlit study assistant with question analysis, image-based question input, study planning, and MySQL-backed question history.

## Run locally

1. Install Python 3.10 or later and MySQL.
2. Create the schema with `1000.sql`.
3. Install dependencies with `pip install -r requirement.txt`.
4. Copy `.env.example` to `.env` and set your OpenAI and database credentials.
5. Run `streamlit run nav.py`.

The application expects the `questionbank.questions` table from `1000.sql`. The database connection reads `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` from the environment. Do not commit `.env`.

## Data and privacy

The application sends typed prompts and uploaded question images to the configured OpenAI API. Review the API provider's data handling terms before using personal or sensitive material. Database credentials must be supplied locally and should not be stored in source code.
