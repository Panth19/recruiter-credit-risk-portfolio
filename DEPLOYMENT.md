# Publish these apps

The deployment bundle is a Git repository with three Streamlit app entrypoints. To make recruiter-accessible live links:

1. Publish this repository to GitHub with **Public** visibility. It contains source code, SEC-derived public company facts, and illustrative synthetic trades/limits only; do not add credentials or private portfolio data.
2. Sign in at https://share.streamlit.io and connect that GitHub account.
3. Create three apps from repository `recruiter-credit-risk-portfolio`, branch `main`, choosing these entrypoint paths:
   - `01-counterparty-exposure-limit-monitor/app.py`
   - `02-corporate-counterparty-scoring/app.py`
   - `03-credit-risk-dashboard/app.py`
4. Choose readable Streamlit subdomains for each app and share the resulting `*.streamlit.app` URLs.

Streamlit Community Cloud supports multiple app entrypoints in one repository. Its deployment form requires a repository, branch, and entrypoint path. See [deployment docs](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy) and [file organization](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization).

In this session, the local GitHub CLI credential is invalid and could not reach GitHub. A GitHub connection is needed to publish the repository. After the connection is active, push this local repository and deploy the three entrypoints above.
