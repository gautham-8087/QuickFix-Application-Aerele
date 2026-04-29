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

### Trace a Request End-to-End - Step 1 - Routing (write answers in README.md):

Section  - B1

1. When a browser hits /api/method/quickfix.api.get_job_summary - what Python function handles this request and how does Frappe find it?

-> When a browser hits this URL,Frappe treats it as a method call.It looks at the path and calls the
Python function: quickfix/api.py → get_job_summary().This request is handled by frappe.handler, which dynamically imports and executes the function.The function must be decorated with @frappe.whitelist().

2. When a browser hits /api/resource/Job Card/JC-2024-0001 - what happens differently compared to /api/method/?

-> When a browser hits /api/resource/Job Card/JC-2024-0001, same handler handles this request but unlike api/method, it goes to REST resource handler. it doesn't require any whitelist method like api/method. api/resourse is working only on DocTypes.

3. When a browser hits /track-job - which file/function handles it and why?

->  When the browser hits /track-job, it actually a website, not an API, so it has been handle by the router and website renderer. it checks whether the files are present inside the www folder and fetch the content using the get_context() and renders jinja HTML

### Step 2 - Session & CSRF (write answers in README.md):

1. Open your Frappe site in browser devtools. Find the X-Frappe-CSRF-Token in a POST request. Where does this value come from and what would happen if you omitted it?

->  X-Frappe-CSRF-Token is generated for the session and it stored in the cache or frappe.local. if you omitted it, post request was rejected and it throws a CSRF Validation error. it mainly  used for prevent the malicious user to make request for logged-in users.

2. In bench console, run: import frappe; frappe.session.data and describe what it
contains

-> frappe.session.data contains the data about the logged-in user details such as the user, user type, session id, role and login time.

### Step 3 - Error visibility (write answers in README.md):

1. With developer_mode: 1 - trigger a Python exception in one of your whitelisted
methods. What does the browser receive?

-> It shows a full traceback which includes line number and file name. it really useful for the developer to easy to debug

2. Set developer_mode: 0 - repeat. What does the browser receive now? Why is this important for production?

-> It shows generic error for the user and actual error goes to server log and error doctype. this is important for production because if the full traceback shows, it might reveals the secret and it leads to security risks

3. Where do production errors go if they are hidden from the browser?

->  It remains stay in the error doctype which stores the error logs

### Step 4 - Permission check location:

1. In a whitelisted method, call frappe.get_doc("Job Card", name) WITHOUT ignore_permissions. Then log in as a QF Technician user who is NOT assigned to that job. What error is raised and at what layer does Frappe stop the request?

-> frappe.permissionError is raised in this situation and Frappe does stop the request at the frappe.model.Document.get_doc. normally permission is enforced in the data accesss layer.
