### QuickFix

QuickFix

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app quickfix
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/quickfix
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

mit

### Answer the Questions

Section - A2

1. what each config file is for, and what breaks if you accidentally put a secret in common_site_config.json

-> common_site_config.json is shared across all sites, while site_config.json is specific to one site and stores sensitive data. Putting secrets in common_site_config.json is risky because all sites can access them, leading to security leaks.

2. list the 4 processes bench start launches (web, worker, scheduler,socketio) and explain what happens to background jobs if the worker process crashes. 

-> bench start runs four processes: web (handles requests), worker (executes background jobs), scheduler (runs scheduled tasks), and socketio (real-time updates). If the worker crashes, background jobs stay in the queue and are not executed until the worker restarts, causing delays.

### Child Table Internals

Section - C1

1. When you append a row to Job Card.parts_used and save, what 4 columns does Frappe automatically set on the child table row?

-> There are 4 columns:
    parent → name of the parent document
    parenttype → parent DocType 
    parentfield → field name 
    idx → row order

2. What is the DB table name for the Part Usage Entry DocType?

-> tabPart Usage Entry

3. If you delete row at idx=2 and re-save, what happens to idx values of remaining rows?

-> Frappe automatically reorders the rows. So, before -> 1 2 3 After -> 1 2 (No Gaps)

###  Renaming task - write in README.md:

Section - C3

1. Rename one of your test Technician records using the Rename Document feature. Then check: does the assigned_technician field on linked Job Cards automatically update? Why or why not? What does "track changes" mean in this context?

-> When a Technician record is renamed using the Rename Document feature, the assigned_technician field in linked Job Cards automatically updates.This happens because Frappe maintains link integrity, so all references to that Technician are updated everywhere.Track Changes means Frappe records all changes made to the document (like rename or field updates).When enabled, we can see the old value -> new value like (0-1) (1-0)

2. Explain unique constraints: what is the difference between setting a field as "unique" in the DocType vs doing a frappe.db.exists() check in validate()?

-> When a field is set as unique, it means the same value cannot be repeated in that field.
If you try to save a duplicate value, the system will throw an error and not allow it.So, in unique field database will block the duplicae values but in frappe.db.exists we need to manually check the code
