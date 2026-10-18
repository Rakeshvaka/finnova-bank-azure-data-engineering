# Upload to GitHub without connecting ChatGPT

1. Sign in to GitHub.
2. Click **New repository**.
3. Suggested name: `finnova-bank-azure-data-engineering`.
4. Add description: `Azure data engineering portfolio using ADF, ADLS Gen2, Databricks, PySpark and Delta Lake`.
5. Choose Public only after reviewing every file; otherwise choose Private.
6. Create the repository.
7. Extract this ZIP. Upload the extracted contents, not just the ZIP file.
8. In the repository, choose **Add file → Upload files** and drag in the extracted files/folders.
9. Commit with message `Add FinNova Bank Azure data engineering project`.
10. Verify the README renders and folders are visible.

Before publishing, search for passwords, access keys, SAS tokens, connection strings, private endpoints, personal emails, and customer data. Replace placeholders. Do not upload screenshots that reveal secrets or account details.

## Optional Git workflow
```bash
git init
git add .
git commit -m "Add FinNova Bank Azure data engineering project"
git branch -M main
git remote add origin https://github.com/<your-username>/finnova-bank-azure-data-engineering.git
git push -u origin main
```
Authenticate through GitHub's browser/credential flow; never paste credentials into source files.
