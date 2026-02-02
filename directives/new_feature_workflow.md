# New Feature Workflow

**Goal**: Implement a new feature in the Travel Guide App reliably.

## Workflow

### 1. Planning (Level 2)
-   **Analyze Request**: Understand what the user wants.
-   **Check Directives**: Is there a specific directive for this type of feature?
-   **Check Existing Tools**: Are there `execution/` scripts that can be reused?
-   **Create Plan**:
    -   Create `implementation_plan.md` artifact.
    -   Define changes in Backend (FastAPI) and Frontend (Next.js).
    -   Identify necessary new `directives` or `execution` scripts.

### 2. Implementation (Level 3)
-   **Backend First**:
    -   Implement API changes.
    -   Update `models/` and `routes/`.
-   **Frontend Second**:
    -   Update `lib/api` to match backend.
    -   Create/Update components.
    -   Update pages.
-   **Determinism**:
    -   If a complex operation is needed (e.g., data migration, scraping), create a Python script in `execution/` instead of doing it manually.

### 3. Verification
-   **Automated Tests**: Run existing tests if available.
-   **Manual Verification**:
    -   Use `directives/run_dev_env.md` to start the app.
    -   Verify the feature in the browser.
-   **Documentation**:
    -   Update `README.md` if the feature is significant.
    -   create/update `walkthrough.md`.

## Output
-   Verified, working feature code.
-   Updated documentation.
