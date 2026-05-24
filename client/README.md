# SMS Pytest Selenium Automation

A robust UI automation framework for the SMS (Student Management System) Panel, built with **Python**, **Pytest**, and **Selenium**. This project follows the **Page Object Model (POM)** design pattern and features automated driver management, configurable environments, and comprehensive reporting.

## 🚀 Features

- **Page Object Model (POM)**: Organized separation of UI elements, page actions, and test logic.
- **Automatic Driver Management**: Uses `webdriver-manager` for seamless handling of Chrome and Firefox binaries.
- **Multi-browser Support**: Toggle between `chrome` and `firefox` via configuration.
- **Headless Mode**: Supports GUI-less execution, perfect for CI/CD pipelines.
- **Environment Configuration**: Secure management of URLs and credentials using `.env` files.
- **Auto-Screenshots**: Captures screenshots automatically on test failures, stored in `reports/screenshots/`.
- **HTML Reporting**: Generates detailed, self-contained HTML reports with `pytest-html`.
- **Structured Test Suites**: Tests categorized into `smoke`, `regression`, `auth`, and `security`.
- **Random Data Generation**: Uses `Faker` to generate dynamic test data for student creation.

## 📋 Prerequisites

- **Python 3.8+**
- **Google Chrome** or **Mozilla Firefox** installed.

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd sms-pytest-selenium
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   BASE_URL=https://your-sms-panel-url.com
   BROWSER=chrome
   HEADLESS=true
   TIMEOUT=10
   VALID_USERNAME=admin@example.com
   VALID_PASSWORD=Secret123!
   ```

## 🏃 Running Tests

### CLI Commands

```bash
# Run all tests
pytest

# Run smoke tests only
pytest -m smoke

# Run authentication tests
pytest -m auth

# Run regression suite
pytest -m regression

# Run with headed browser (useful for debugging)
HEADLESS=false pytest

# Generate HTML report manually (though auto-configured in pytest.ini)
pytest --html=reports/report.html --self-contained-html
```

### View Reports

- **HTML Report**: `reports/report.html`
- **Screenshots**: `reports/screenshots/` (only for failed tests)

## 📂 Project Structure

```text
sms-pytest-selenium/
├── config/             # Configuration management
│   └── config.py       # Loads .env settings
├── pages/              # Page Object Model classes
│   ├── base_page.py    # Common selenium wrappers
│   ├── login_page.py   # Login page locators and actions
│   └── dashboard_page.py # Student dashboard interactions
├── tests/              # Test suites organized by type
│   ├── auth/           # Login and session tests
│   ├── regression/     # Full functional regression
│   ├── security/       # Navigation and access control
│   └── smoke/          # Critical path smoke tests
├── utils/              # Helper utilities
│   ├── random_payload_generator.py # Faker-based data gen
│   ├── table_filter_handler.py    # Table data extraction
│   └── table_reload_handler.py    # Table sync helpers
├── reports/            # Test execution artifacts
├── conftest.py         # Pytest fixtures and hooks
├── pytest.ini          # Pytest run configurations
└── requirements.txt    # Project dependencies
```

## 🏗️ Adding New Tests

1. **Define Locators**: Add new UI elements to the appropriate class in `pages/`.
2. **Implement Actions**: Add methods to interact with those elements.
3. **Write Tests**: Add a new test in the relevant `tests/` subdirectory.
4. **Use Markers**: Annotate tests with `@pytest.mark.<type>` for selective execution.

---
*Happy Testing!* 🧪
