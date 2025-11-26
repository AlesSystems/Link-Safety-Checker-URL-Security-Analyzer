# GitHub Actions Workflows for Link Safety Checker

This document outlines recommended GitHub Actions workflows that can be implemented for the Link Safety Checker - URL Security Analyzer project.

## Table of Contents

- [Setting Up GitHub Actions](#setting-up-github-actions)
- [CI/CD Workflows](#cicd-workflows)
- [Code Quality Workflows](#code-quality-workflows)
- [Security Workflows](#security-workflows)
- [Documentation Workflows](#documentation-workflows)
- [Release Workflows](#release-workflows)
- [Dependency Management Workflows](#dependency-management-workflows)

---

## Setting Up GitHub Actions

This section provides step-by-step instructions for setting up GitHub Actions workflows in your repository through the GitHub website.

### Prerequisites

- A GitHub repository (public or private)
- Repository admin or write access
- Basic understanding of YAML syntax

---

### Step 1: Enable GitHub Actions

1. **Navigate to your repository** on GitHub
2. **Click on the "Settings" tab** (located in the repository navigation bar)
3. **Scroll down to "Actions"** in the left sidebar
4. **Under "Actions permissions"**, ensure one of the following is selected:
   - "Allow all actions and reusable workflows" (recommended for full functionality)
   - "Allow local actions and reusable workflows" (more restrictive)
5. **Click "Save"** if you made any changes

**Note:** If you don't see the Settings tab, you don't have admin access to the repository.

---

### Step 2: Create the Workflows Directory

You can create workflow files either through the GitHub web interface or by cloning the repository locally.

#### Option A: Using GitHub Web Interface

1. **Navigate to your repository** on GitHub
2. **Click "Add file"** → **"Create new file"**
3. **Type `.github/workflows/`** in the file path (GitHub will create the directories automatically)
4. **Name your workflow file** (e.g., `ci.yml`)
5. **Add your workflow YAML content**
6. **Click "Commit new file"** at the bottom

#### Option B: Using Git Commands

1. **Clone your repository** locally (if not already cloned)
2. **Create the workflows directory:**
   ```bash
   mkdir -p .github/workflows
   ```
3. **Create your workflow file** in `.github/workflows/`
4. **Commit and push:**
   ```bash
   git add .github/workflows/
   git commit -m "Add GitHub Actions workflow"
   git push
   ```

---

### Step 3: Create Your First Workflow

1. **Go to the "Actions" tab** in your repository
2. **Click "New workflow"** (or "set up a workflow yourself" if you see suggested workflows)
3. **Choose a template** or start with a blank workflow
4. **GitHub will create a file** at `.github/workflows/main.yml` (you can rename it)
5. **Edit the workflow YAML** in the web editor
6. **Click "Start commit"** → **"Commit new file"**

**Recommended:** Start with a simple CI workflow to test that Actions are working.

---

### Step 4: Configure Repository Secrets

Secrets are encrypted environment variables that can be used in workflows without exposing sensitive data.

#### Adding Secrets via GitHub Website

1. **Navigate to your repository** → **"Settings"** tab
2. **Click "Secrets and variables"** → **"Actions"** in the left sidebar
3. **Click "New repository secret"**
4. **Enter the secret:**
   - **Name:** Enter a name (e.g., `GOOGLE_SAFE_BROWSING_API_KEY`)
   - **Secret:** Paste the actual secret value
5. **Click "Add secret"**

#### Common Secrets for This Project

- `GOOGLE_SAFE_BROWSING_API_KEY` - For Google Safe Browsing API integration
- `CODECOV_TOKEN` - For code coverage reporting (if using Codecov)
- `PYPI_API_TOKEN` - For publishing to PyPI (if applicable)
- `SLACK_WEBHOOK_URL` - For notifications (if using Slack)

#### Using Secrets in Workflows

Reference secrets in your workflow files using:
```yaml
env:
  API_KEY: ${{ secrets.GOOGLE_SAFE_BROWSING_API_KEY }}
```

---

### Step 5: Set Up Dependabot (For Dependency Scanning)

Dependabot is GitHub's built-in dependency management tool.

1. **Navigate to your repository** → **"Settings"** tab
2. **Click "Code security and analysis"** in the left sidebar
3. **Find "Dependabot alerts"** and click **"Enable"**
4. **Find "Dependabot security updates"** and click **"Enable"**
5. **Optionally, enable "Dependabot version updates":**
   - Click "Enable" next to "Dependabot version updates"
   - Click "Create config file"
   - GitHub will create `.github/dependabot.yml`
   - Customize the file for your project's dependency files (e.g., `requirements.txt`, `package.json`)

---

### Step 6: Enable Secret Scanning

GitHub automatically scans for secrets in public repositories. For private repositories:

1. **Navigate to your repository** → **"Settings"** tab
2. **Click "Code security and analysis"** in the left sidebar
3. **Find "Secret scanning"** and click **"Enable"**
4. **Optionally enable "Push protection"** to block pushes containing secrets

---

### Step 7: Configure Branch Protection Rules (Optional but Recommended)

Protect your main branch to ensure workflows pass before merging:

1. **Navigate to your repository** → **"Settings"** tab
2. **Click "Branches"** in the left sidebar
3. **Click "Add rule"** or edit existing rule for your main branch
4. **Configure the rule:**
   - **Branch name pattern:** `main` (or your default branch)
   - **Require status checks to pass before merging:** ✓
   - **Select the required status checks** (your CI workflow)
   - **Require branches to be up to date before merging:** ✓
5. **Click "Create"** or **"Save changes"**

---

### Step 8: Test Your Workflow

1. **Make a small change** to your repository (e.g., update README)
2. **Commit and push** the change
3. **Go to the "Actions" tab** in your repository
4. **You should see your workflow running**
5. **Click on the workflow run** to see detailed logs
6. **Verify the workflow completes successfully**

---

### Step 9: Monitor Workflow Runs

1. **Navigate to the "Actions" tab** in your repository
2. **View all workflow runs** and their status
3. **Click on a run** to see:
   - Which jobs ran
   - Step-by-step logs
   - Duration and status
   - Artifacts (if any were created)
4. **Set up notifications:**
   - Go to **"Settings"** → **"Notifications"**
   - Configure email or web notifications for workflow failures

---

### Step 10: Customize Workflow Permissions

For enhanced security, limit workflow permissions:

1. **Navigate to your repository** → **"Settings"** tab
2. **Click "Actions"** → **"General"**
3. **Under "Workflow permissions"**, choose:
   - **"Read and write permissions"** (if workflows need to push changes)
   - **"Read repository contents and packages permissions"** (more restrictive, recommended)
4. **Optionally, allow GitHub Actions to create and approve pull requests**
5. **Click "Save"**

---

### Troubleshooting Common Issues

#### Workflows Not Running

- **Check Actions are enabled:** Settings → Actions → Actions permissions
- **Verify workflow file syntax:** Use a YAML validator
- **Check file location:** Must be in `.github/workflows/` directory
- **Verify file extension:** Should be `.yml` or `.yaml`

#### Workflow Failing

- **Check workflow logs:** Actions tab → Click on failed run → Review error messages
- **Verify secrets are set:** Settings → Secrets and variables → Actions
- **Check permissions:** Ensure workflow has necessary permissions
- **Test locally:** Run commands locally to identify issues

#### Secrets Not Working

- **Verify secret name:** Must match exactly (case-sensitive)
- **Check scope:** Repository secrets vs. organization secrets
- **Restart workflow:** Secrets are loaded at workflow start

#### Dependabot Not Working

- **Verify config file exists:** `.github/dependabot.yml`
- **Check package manager:** Ensure correct package manager is configured
- **Review Dependabot logs:** Settings → Code security and analysis → Dependabot

---

### Quick Start Checklist

- [ ] GitHub Actions enabled in repository settings
- [ ] `.github/workflows/` directory created
- [ ] First workflow file created (e.g., `ci.yml`)
- [ ] Required secrets added (API keys, tokens)
- [ ] Dependabot enabled (for dependency scanning)
- [ ] Secret scanning enabled
- [ ] Workflow tested with a test commit
- [ ] Branch protection rules configured (optional)
- [ ] Workflow permissions configured

---

### Next Steps

After completing the setup:

1. **Start with Phase 1 workflows** (see Recommended Workflow Priority section)
2. **Monitor workflow runs** to ensure they're working correctly
3. **Gradually add more workflows** as needed
4. **Customize workflows** based on your project's specific requirements
5. **Set up notifications** to stay informed about workflow status

---

## CI/CD Workflows

### 1. Continuous Integration (CI) Pipeline
**Purpose:** Automatically test code on every push and pull request

**Triggers:**
- Push to any branch
- Pull request events (opened, synchronize, reopened)
- Manual workflow dispatch

**Steps:**
- Checkout code
- Set up Python environment (or appropriate language runtime)
- Install dependencies
- Run linters (flake8, pylint, black, etc.)
- Run unit tests
- Run integration tests
- Generate test coverage reports
- Upload coverage reports to code coverage service (Codecov, Coveralls)

**Benefits:**
- Catch bugs early
- Ensure code quality before merging
- Maintain test coverage standards

---

### 2. Multi-Platform Testing
**Purpose:** Ensure the application works across different operating systems

**Triggers:**
- Push to main/develop branches
- Pull requests targeting main/develop

**Platforms:**
- Ubuntu Latest
- Windows Latest
- macOS Latest

**Steps:**
- Run full test suite on each platform
- Verify API integration works on all platforms
- Test URL parsing across different environments

**Benefits:**
- Cross-platform compatibility assurance
- Identify OS-specific issues early

---

### 3. Build and Package Workflow
**Purpose:** Build distributable packages for the application

**Triggers:**
- Push of version tags (v*)
- Release creation
- Manual workflow dispatch

**Steps:**
- Build application package
- Create distribution artifacts (wheel, source distribution for Python)
- Upload artifacts to GitHub Releases
- Optionally publish to package registries (PyPI, npm, etc.)

**Benefits:**
- Automated release packaging
- Consistent build process
- Easy distribution

---

## Code Quality Workflows

### 4. Code Linting and Formatting
**Purpose:** Enforce code style and catch potential issues

**Triggers:**
- Push to any branch
- Pull request events
- Scheduled runs (daily)

**Steps:**
- Run linters (flake8, pylint, eslint, etc.)
- Check code formatting (black, prettier, etc.)
- Run type checking (mypy, TypeScript compiler)
- Comment PR with linting results
- Optionally auto-fix and commit formatting issues

**Benefits:**
- Consistent code style
- Early detection of code quality issues
- Reduced review time

---

### 5. Code Coverage Analysis
**Purpose:** Monitor and enforce test coverage thresholds

**Triggers:**
- Push to any branch
- Pull request events

**Steps:**
- Run test suite with coverage
- Generate coverage reports
- Check coverage thresholds (e.g., minimum 80% coverage)
- Upload coverage reports
- Comment PR with coverage changes
- Fail if coverage drops below threshold

**Benefits:**
- Maintain high test coverage
- Track coverage trends over time
- Identify untested code areas

---

## Security Workflows

### 6. Dependency Vulnerability Scanning
**Purpose:** Identify and alert on vulnerable dependencies

**Triggers:**
- Push to any branch
- Pull request events
- Scheduled runs (daily or weekly)

**Steps:**
- Scan dependencies for known vulnerabilities
- Use tools like Dependabot, Snyk, or GitHub Security Advisories
- Generate security reports
- Create issues for high/critical vulnerabilities
- Comment PR with vulnerability findings

**Benefits:**
- Proactive security monitoring
- Compliance with security best practices
- Protection against known vulnerabilities

---

### 7. Secret Scanning
**Purpose:** Prevent accidental exposure of secrets and API keys

**Triggers:**
- Push to any branch
- Pull request events

**Steps:**
- Scan code for hardcoded secrets (API keys, passwords, tokens)
- Use GitHub Secret Scanning or tools like truffleHog
- Block PRs with detected secrets
- Alert maintainers immediately

**Benefits:**
- Prevent credential leaks
- Protect API keys and sensitive data
- Maintain security posture

---

### 8. SAST (Static Application Security Testing)
**Purpose:** Find security vulnerabilities in source code

**Triggers:**
- Push to main/develop branches
- Pull requests
- Scheduled runs (weekly)

**Steps:**
- Run static analysis tools (Bandit for Python, ESLint security plugins, etc.)
- Scan for common vulnerabilities (OWASP Top 10)
- Generate security reports
- Create issues for high-severity findings

**Benefits:**
- Early detection of security issues
- Code security best practices
- Compliance with security standards

---

## Documentation Workflows

### 9. Documentation Build and Validation
**Purpose:** Ensure documentation is up-to-date and builds correctly

**Triggers:**
- Push to any branch
- Changes to documentation files
- Pull request events

**Steps:**
- Build documentation (Sphinx, MkDocs, Jekyll, etc.)
- Validate markdown syntax
- Check for broken links
- Deploy documentation to GitHub Pages (on main branch)
- Preview documentation in PR comments

**Benefits:**
- Always up-to-date documentation
- Catch documentation errors early
- Easy access to latest docs

---

### 10. API Documentation Generation
**Purpose:** Automatically generate API documentation from code

**Triggers:**
- Push to main/develop branches
- Changes to API-related code

**Steps:**
- Extract API documentation from code comments/docstrings
- Generate API reference documentation
- Update API documentation in repository
- Deploy to documentation site

**Benefits:**
- Synchronized API documentation
- Reduced manual documentation work
- Better developer experience

---

## Release Workflows

### 11. Automated Versioning and Changelog
**Purpose:** Automate version bumping and changelog generation

**Triggers:**
- Push to main branch
- Manual workflow dispatch with version type (major/minor/patch)

**Steps:**
- Analyze commits since last release
- Determine version bump type (conventional commits)
- Update version in project files
- Generate changelog from commit messages
- Create release branch
- Open PR with version changes

**Benefits:**
- Consistent versioning
- Automated changelog generation
- Semantic versioning compliance

---

### 12. Release Creation and Publishing
**Purpose:** Automate the release process

**Triggers:**
- Push of version tags
- Release creation event

**Steps:**
- Build release artifacts
- Run full test suite
- Create GitHub Release
- Attach release artifacts
- Publish release notes
- Optionally publish to package registries
- Notify team of new release

**Benefits:**
- Streamlined release process
- Consistent release quality
- Reduced manual errors

---

## Dependency Management Workflows

### 13. Dependency Update Automation
**Purpose:** Keep dependencies up-to-date automatically

**Triggers:**
- Scheduled runs (weekly)
- Manual workflow dispatch

**Steps:**
- Check for outdated dependencies
- Create pull requests for dependency updates
- Test updated dependencies
- Group related updates
- Notify maintainers

**Benefits:**
- Security patches applied quickly
- Latest features and bug fixes
- Reduced maintenance burden

---

### 14. Dependency License Compliance
**Purpose:** Ensure all dependencies comply with project license requirements

**Triggers:**
- Push to any branch
- Pull request events
- Scheduled runs (weekly)

**Steps:**
- Scan all dependencies for licenses
- Check against allowed license list
- Generate license report
- Block PRs with incompatible licenses
- Generate attribution file

**Benefits:**
- License compliance
- Legal risk mitigation
- Transparent dependency licensing

---

## Recommended Workflow Priority

### Phase 1 (Essential)
1. Continuous Integration (CI) Pipeline
2. Code Linting and Formatting
3. Dependency Vulnerability Scanning

### Phase 2 (Important)
4. Code Coverage Analysis
5. Secret Scanning
6. Build and Package Workflow

### Phase 3 (Nice to Have)
7. Multi-Platform Testing
8. Documentation Build and Validation
9. Release Creation and Publishing

### Phase 4 (Advanced)
10. SAST (Static Application Security Testing)
11. Automated Versioning and Changelog
12. Dependency Update Automation

---

## Setting Up Specific Workflows

### Setting Up Code Coverage (Workflow #5)

1. **Choose a coverage service:**
   - **Codecov:** Free for open source projects
   - **Coveralls:** Free tier available
   - **GitHub Actions Artifacts:** Built-in, no external service needed

2. **For Codecov:**
   - Sign up at [codecov.io](https://codecov.io) with your GitHub account
   - Add your repository
   - Copy the upload token
   - Add token as secret: `CODECOV_TOKEN`

3. **For Coveralls:**
   - Sign up at [coveralls.io](https://coveralls.io) with your GitHub account
   - Add your repository
   - Copy the repo token
   - Add token as secret: `COVERALLS_REPO_TOKEN`

### Setting Up Dependency Vulnerability Scanning (Workflow #6)

1. **Enable Dependabot** (see Step 5 in Setup Guide)
2. **Configure Dependabot** by creating/editing `.github/dependabot.yml`
3. **Enable GitHub Security Advisories:**
   - Settings → Code security and analysis
   - Enable "Dependabot alerts"
   - Enable "Dependabot security updates"

### Setting Up Secret Scanning (Workflow #7)

1. **Enable Secret Scanning** (see Step 6 in Setup Guide)
2. **For enhanced scanning, add a workflow** using tools like:
   - `truffleHog` action
   - `git-secrets` action
   - Custom regex-based scanning

### Setting Up Documentation (Workflow #9)

1. **Enable GitHub Pages:**
   - Settings → Pages
   - Source: Deploy from a branch (usually `gh-pages` or `main`)
   - Select branch and folder
   - Save

2. **Configure workflow permissions:**
   - Workflow needs write permissions to deploy to Pages
   - Settings → Actions → General → Workflow permissions → Read and write

### Setting Up Release Workflows (Workflow #12)

1. **Create a Personal Access Token (PAT)** for publishing:
   - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate new token with `repo` and `write:packages` scopes
   - Add as secret: `GITHUB_TOKEN` (or custom name)

2. **For PyPI publishing:**
   - Create account on [pypi.org](https://pypi.org)
   - Generate API token
   - Add as secret: `PYPI_API_TOKEN`

### Setting Up Notifications

1. **Email Notifications:**
   - Settings → Notifications → Email
   - Enable "Actions" notifications

2. **Slack Integration:**
   - Create Slack webhook URL
   - Add as secret: `SLACK_WEBHOOK_URL`
   - Use Slack action in workflows

3. **Discord Integration:**
   - Create Discord webhook URL
   - Add as secret: `DISCORD_WEBHOOK_URL`
   - Use Discord action in workflows

---

## Implementation Notes

- **Workflow Files Location:** `.github/workflows/`
- **Naming Convention:** Use descriptive names like `ci.yml`, `security-scan.yml`, `release.yml`
- **Secrets Management:** Store API keys and sensitive data in GitHub Secrets
- **Matrix Strategy:** Use matrix builds for testing multiple Python versions or platforms
- **Caching:** Implement caching for dependencies to speed up workflows
- **Conditional Execution:** Use workflow conditions to run steps only when needed
- **Notifications:** Configure Slack, email, or other notification channels for workflow results

---

## Example Workflow Structure

Each workflow should follow this general structure:

```yaml
name: Workflow Name

on:
  # Triggers

jobs:
  job-name:
    runs-on: ubuntu-latest
    steps:
      - name: Step description
        # Actions
```

---

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)

---

**Last Updated:** Based on current project requirements and best practices for Python-based security analysis tools.

