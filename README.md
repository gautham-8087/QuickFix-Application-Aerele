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

### Part A - Table naming (bench console, write output in README_internals.md): 

Section - B2

1. Run: frappe.db.sql("SHOW TABLES LIKE '%Job%'") and list what you see. Explain the tab prefix convention.

-> In [1]: frappe.db.sql("SHOW TABLES LIKE '%Job%'")
   Out[1]: (('tabJob Card',), ('tabScheduled Job Log',), ('tabScheduled Job Type',))
   -> tab should be followed by the doctype name.For Ex: Job Card -> tabJob Card

2. Run: frappe.db.sql("DESCRIBE `tabJob Card`", as_dict=True) and list 5 column names you recognise from your DocType fields.

-> In [2]: frappe.db.sql("DESCRIBE `tabJob Card`", as_dict=True)
Out[2]: 
[{'Field': 'name',
  'Type': 'varchar(140)',
  'Null': 'NO',
  'Key': 'PRI',
  'Default': None,
  'Extra': ''},
 {'Field': 'creation',
  'Type': 'datetime(6)',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': 'modified',
  'Type': 'datetime(6)',
  'Null': 'YES',
  'Key': 'MUL',
  'Default': None,
  'Extra': ''},
 {'Field': 'modified_by',
  'Type': 'varchar(140)',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': 'owner',
  'Type': 'varchar(140)',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': 'docstatus',
  'Type': 'int(1)',
  'Null': 'NO',
  'Key': '',
  'Default': '0',
  'Extra': ''},
 {'Field': 'idx',
  'Type': 'int(8)',
  'Null': 'NO',
  'Key': '',
  'Default': '0',
  'Extra': ''},
 {'Field': 'amended_from',
  'Type': 'varchar(140)',
  'Null': 'YES',
  'Key': 'MUL',
  'Default': None,
  'Extra': ''},
 {'Field': '_user_tags',
  'Type': 'text',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': '_comments',
  'Type': 'text',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': '_assign',
  'Type': 'text',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': '_liked_by',
  'Type': 'text',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': 'customer_name',
  'Type': 'varchar(140)',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': 'customer_phone',
  'Type': 'varchar(140)',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': 'customer_email',
  'Type': 'varchar(140)',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': 'device_type',
  'Type': 'varchar(140)',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': 'device_brand',
  'Type': 'varchar(140)',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': 'device_model',
  'Type': 'varchar(140)',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': 'imei_or_serial',
  'Type': 'varchar(140)',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': 'problem_description',
  'Type': 'longtext',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': 'h',
  'Type': 'varchar(140)',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': 'assigned_technician',
  'Type': 'varchar(140)',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': 'diagnosis_notes',
  'Type': 'longtext',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': 'estimated_cost',
  'Type': 'decimal(21,9)',
  'Null': 'NO',
  'Key': '',
  'Default': '0.000000000',
  'Extra': ''},
 {'Field': 'diagnosis_date',
  'Type': 'date',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': 'priority',
  'Type': 'varchar(140)',
  'Null': 'YES',
  'Key': '',
  'Default': 'Normal',
  'Extra': ''},
 {'Field': 'parts_total',
  'Type': 'decimal(21,9)',
  'Null': 'NO',
  'Key': '',
  'Default': '0.000000000',
  'Extra': ''},
 {'Field': 'labour_charge',
  'Type': 'decimal(21,9)',
  'Null': 'NO',
  'Key': '',
  'Default': '500.000000000',
  'Extra': ''},
 {'Field': 'final_mount',
  'Type': 'decimal(21,9)',
  'Null': 'NO',
  'Key': '',
  'Default': '0.000000000',
  'Extra': ''},
 {'Field': 'payment_status',
  'Type': 'varchar(140)',
  'Null': 'YES',
  'Key': '',
  'Default': 'Unpaid',
  'Extra': ''},
 {'Field': 'delivery_date',
  'Type': 'date',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': 'remarks',
  'Type': 'text',
  'Null': 'YES',
  'Key': '',
  'Default': None,
  'Extra': ''},
 {'Field': 'status',
  'Type': 'varchar(140)',
  'Null': 'YES',
  'Key': '',
  'Default': 'Draft',
  'Extra': ''},
 {'Field': 'final_amount',
  'Type': 'decimal(21,9)',
  'Null': 'NO',
  'Key': '',
  'Default': '0.000000000',
  'Extra': ''}]

### Part D - DocStatus transitions (write answers in README_internals.md):

1. What are the three numeric values of docstatus and what state does each represent?

-> 0 - Draft (Can be edited freely)
   1 - Sumbitted (Cannot be edited)
   2 - Cancelled (No longer active)

2. Can you call doc.save() on a submitted document? What about doc.submit() on a cancelled one? Test in bench console and explain why.

->  doc.save() - No, Because it is already final, so you can’t edit it.
    doc.submit() -  No, Because it is already cancelled, so you can’t submit it again.

3. Why would you see a "Document has been modified after you have opened it" error and how does Frappe prevent concurrent overwrites?

-> Frappe checks the modified time to prevent overwriting someone else’s changes.

### Part E - Dangerous patterns (identify and fix) (add the correct version with explanation in README_internals.md):

1. The following snippet has TWO bugs related to document lifecycle. Identify both and writen the corrected version:
def validate(self):
    self.total = sum(r.amount for r in self.items)
    self.save()
    other = frappe.get_doc("Spare Part", self.part)
    other.stock_qty -= self.qty
    other.save()

-> self.save() - Wrong, Because validate() function already runs during save. So,Calling save() function again → causes recursion loop / crash 
-> other.save() - Wrong, Because You should not update another document in validate() Lifecycle rule violation 

### Section D1

In bench console: call frappe.get_doc_permissions(doc) on a Job Card while logged in as different users. Document what the return dict looks like.

    In [7]: doc = frappe.get_doc("Job Card", "JC-2026-00001")
    frappe.permissions.get_doc_permissions(doc)
    Out[7]: 
    {'select': 1,
    'read': 1,
    'write': 1,
    'create': 1,
    'delete': 1,
    'submit': 1,
    'cancel': 1,
    'amend': 1,
    'print': 1,
    'email': 1,
    'report': 1,
    'import': 0,
    'export': 1,
    'share': 1}

### Sections D2
What is the issues in using frappe.get_all in a whitelisted method that is exposed to guests
or low-privilege users. Explain it in the context of permission_query_conditions

-> It bypasses permission_query_conditions
-> Returns all records
-> Ignores user roles

### Section E1

1. Call self.save() inside on_update and see to the issues of it and explain them in the same readme_internals. Correct the pattern and explain it.

-> Calling self.save() inside on_update() causes infinite recursion because save() triggers on_update() again. This leads to a loop that crashes the system.

-> We can prevent in two methods.
    1. use the frappe.db.set_value, instead of self.save()
    2. Move the logic of on_update into validate or before_save

# Part B - Upgrade friction analysis:

 1. why is doc_events safer than override_doctype_class for most use cases?

 -> doc_events is considered safer because it extends behaviour without replacing the core controller class. It hooks into lifecycle events such as validate, before_save, on_submit, aloowing custom logic to run alongside existing framework logic.

# Part C - Controller method for Spare Part (frappe.db performance):

1. Which of the below pattern would you use and and explain why
        doc = frappe.get_doc("QuickFix Settings", "QuickFix Settings")
        threshold = doc.low_stock_threshold
        threshold = frappe.db.get_value("QuickFix Settings", None,
        "low_stock_threshold")

-> I will use frappe.db.get_value because it is faster to find data and fetches only required field.

# Section F1

1. in what order do they run? What happens if both raise a frappe.ValidationError?

-> Controller runs first; if it throws a frappe.ValidationError, execution stops and then the  doc_events hook won’t run.

2. Demonstrate: what happens when you register "*" AND a specific DocType handler for the same event? Do both run?

-> Both also runs but first the * will run and then the specific doctype handles of the event will run.