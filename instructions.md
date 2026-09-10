# 31. ENGINEERING STANDARDS — DO NOT VIBE CODE

This project must be developed like a real open-source software project, not like an AI-generated demo.

Use the engineering discipline seen in mature open-source repositories such as Unsloth: focused changes, clear motivation, reproducible setup, meaningful documentation, careful error handling, and testable code.

Reference:
https://github.com/unslothai/unsloth

Do NOT copy Unsloth's implementation, code, branding, architecture, or proprietary project-specific patterns. Adopt only the general engineering practices.

---

## A. NO VIBE CODING

Do not generate large amounts of code without understanding how the pieces connect.

Before implementing a feature:

1. Understand the requirement.
2. Identify affected modules.
3. Identify database changes.
4. Identify API changes.
5. Identify frontend changes.
6. Identify security implications.
7. Implement the smallest coherent change.
8. Test it.
9. Fix problems.
10. Only then move to the next feature.

Never create code simply because "the feature probably needs it."

Every file and function must have a clear purpose.

---

## B. DO NOT OVER-ENGINEER

This is a modular monolithic Flask application.

Do NOT introduce:

* unnecessary microservices
* Kubernetes
* message brokers
* complicated event buses
* excessive design patterns
* unnecessary abstraction layers
* dozens of tiny utility classes
* unnecessary AI agents
* unnecessary external services

Prefer simple, explicit solutions.

A student should be able to explain the architecture during a viva.

---

## C. IMPLEMENT FEATURES COMPLETELY

Never create fake functionality.

Bad:

```python
def find_matches():
    pass
```

or:

```python
# TODO: implement AI matching
```

while the UI pretends the feature works.

If a feature is displayed in the UI, its backend behavior must actually exist.

If a feature cannot be implemented yet, clearly label it as unavailable rather than pretending it works.

---

## D. NO FAKE AI

Do not add meaningless "AI" terminology.

The image matching system must actually perform:

image
→ preprocessing
→ embedding generation
→ similarity calculation
→ candidate ranking
→ final score

Document exactly which model/library is being used.

Explain:

* why the model was chosen
* what an embedding represents
* how similarity is calculated
* limitations of the approach
* what happens when no good match exists

Do not claim that the model "understands" ownership.

The system identifies potential visual matches only.

---

## E. MAKE THE CODE LOOK HUMAN-MAINTAINED

Avoid patterns commonly produced by low-quality AI-generated code.

Do NOT:

* add unnecessary comments to every line
* write comments that merely restate the code
* use generic names such as `data`, `temp`, `result2`, `thing`
* create huge functions containing everything
* duplicate similar logic
* create enormous route files
* put SQL, business logic, validation, and response formatting into one function
* generate unused helper functions
* create unused imports
* leave dead code
* leave debugging `print()` statements
* swallow exceptions with empty `except` blocks
* return inconsistent API formats
* hardcode secrets
* hardcode environment-specific paths
* add dependencies without justification

Comments should explain WHY something is done when the reason is not obvious.

---

## F. SMALL, FOCUSED CHANGES

Treat each feature like a focused pull request.

For example:

Feature:

"Add lost-item reporting"

Should involve only the necessary:

* database model
* migration/schema
* service
* API route
* validation
* frontend form
* frontend API call
* tests

Do not simultaneously refactor unrelated parts of the project.

Keep changes focused and reviewable.

This follows the spirit of mature open-source contribution practices, where focused changes and clear motivation are preferred.

---

## G. GIT DISCIPLINE

Structure development as meaningful commits.

Use commits such as:

```text
feat: add user authentication
feat: add lost item reporting
feat: add found item reporting
feat: add image upload validation
feat: add image embedding generation
feat: add candidate matching
feat: add match scoring
feat: add match notifications
feat: add internal messaging
feat: add admin analytics
fix: handle invalid image uploads
fix: prevent unauthorized item deletion
test: add matching service tests
docs: add local setup instructions
```

Do NOT make commits such as:

```text
update
changes
final
final2
final-final
AI generated
working
done
```

Each commit should represent a coherent change.

---

## H. VERIFY BEFORE MOVING FORWARD

After every major implementation step, run:

1. Application startup check
2. Database connection check
3. Relevant unit tests
4. API tests
5. Frontend functionality check
6. Error-path check

Do not assume code works simply because it was generated successfully.

If something fails:

1. Read the actual error.
2. Identify the root cause.
3. Fix the root cause.
4. Re-run the relevant test.
5. Continue only after verification.

Never hide an error by disabling the failing functionality.

---

## I. TEST REAL BEHAVIOR

Tests should verify behavior, not merely that functions execute.

For example:

BAD:

```python
def test_matching():
    assert matching_service is not None
```

GOOD:

```text
Given two visually similar images,
the matching service should produce
a higher similarity score than for
two unrelated images.
```

Test:

* valid inputs
* invalid inputs
* missing inputs
* unauthorized users
* nonexistent resources
* duplicate data
* edge cases
* failure conditions

---

## J. KEEP BUSINESS LOGIC OUT OF ROUTES

Avoid:

```python
@app.route("/matches")
def matches():
    # 150 lines of matching logic
```

Instead:

```text
Route
  ↓
Service
  ↓
Repository / Model
```

For example:

```python
@matches_bp.route("/<int:item_id>")
def get_matches(item_id):
    matches = matching_service.find_matches(item_id)
    return jsonify(matches)
```

The actual matching algorithm belongs in the matching service.

---

## K. DATABASE DISCIPLINE

Do not casually modify the database schema.

For every schema change:

1. Explain the change.
2. Update the schema/migration.
3. Update affected models.
4. Update affected services.
5. Update tests.
6. Update seed data if necessary.

Use:

* foreign keys
* indexes
* appropriate constraints
* timestamps
* normalized relationships

Avoid storing large blobs directly in MySQL unless there is a clear reason.

Images should normally be stored as files/object storage, with references stored in the database.

---

## L. API CONSISTENCY

All API responses should follow a consistent structure.

Success:

```json
{
  "success": true,
  "data": {},
  "message": "Item created successfully"
}
```

Failure:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_IMAGE",
    "message": "The uploaded image format is not supported."
  }
}
```

Do not randomly return different response formats from different endpoints.

Use appropriate HTTP status codes.

Examples:

```text
200 OK
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Unprocessable Entity
500 Internal Server Error
```

---

## M. LOGGING INSTEAD OF RANDOM PRINTS

Do not use:

```python
print("something went wrong")
```

Use structured application logging.

Log useful information such as:

* request failures
* matching failures
* unexpected exceptions
* authentication failures
* important administrative actions

Never log:

* passwords
* tokens
* private messages
* sensitive personal information

---

## N. CONFIGURATION

Never hardcode:

* database passwords
* secret keys
* API keys
* absolute Windows paths
* production URLs

Use environment variables.

Provide:

```text
.env.example
```

Example:

```text
FLASK_ENV=development
SECRET_KEY=change-me
DATABASE_URL=mysql+pymysql://user:password@localhost/campus_lost_found
UPLOAD_FOLDER=uploads
```

Never commit `.env`.

---

## O. DEPENDENCY DISCIPLINE

Do not add a package just because it is convenient.

Before adding a dependency:

1. Determine whether the functionality can be implemented with the standard library/current stack.
2. If a dependency is needed, explain why.
3. Pin or constrain versions appropriately.
4. Add it to the dependency file.
5. Test installation from a clean environment.

Keep `requirements.txt` intentional and minimal.

---

## P. REPRODUCIBLE DEVELOPMENT

A fresh developer should be able to clone the repository and understand how to run it.

README must clearly explain:

```text
Prerequisites
↓
Create virtual environment
↓
Install dependencies
↓
Configure .env
↓
Create MySQL database
↓
Initialize schema
↓
Seed development data
↓
Start backend
↓
Open frontend
```

Do not assume the developer already knows the setup.

Document Windows instructions because this project is being developed on Windows.

---

## Q. DOCUMENT DECISIONS

When making a non-obvious technical decision, document it.

Create:

```text
docs/
    architecture.md
    matching-algorithm.md
    database.md
    api.md
```

For example:

### Why embeddings?

Explain why raw pixel comparison is insufficient.

### Why cosine similarity?

Explain what it measures and why it is suitable.

### Why weighted scoring?

Explain why image similarity alone can produce false positives.

This makes the project easier to defend during a viva.

---

## R. MEASURE THE IMAGE MATCHING SYSTEM

Do not simply say:

"Image matching works."

Create a small evaluation dataset.

For example:

```text
Dataset
├── same_item/
├── similar_item/
└── unrelated_item/
```

Evaluate whether:

```text
same item > similar item > unrelated item
```

in similarity score.

Report basic observations in the documentation.

Also document limitations such as:

* different lighting
* different camera angles
* occlusion
* visually similar objects
* low-quality photographs
* multiple identical products

---

## S. USE REALISTIC SAMPLE DATA

Do not populate the database with:

```text
Test User 1
Test User 2
Item 1
Item 2
ABC
XYZ
Lorem ipsum
```

Use realistic but fictional campus data.

Example:

```text
Ananya Sharma
CSE
Black Lenovo laptop bag
Library
```

Make it clear that the data is fictional/demo data.

---

## T. UI SHOULD NOT LOOK AI-GENERATED

Avoid:

* excessive gradients
* random glassmorphism
* giant hero sections
* unnecessary animations
* excessive emojis
* generic dashboard cards everywhere
* huge rounded buttons
* meaningless statistics

Prioritize usability.

The design should feel like an actual college product.

Use consistent:

* spacing
* typography
* component sizes
* colors
* button styles
* status badges
* error states
* loading states
* empty states

---

## U. NO PLACEHOLDER UI

Do not create buttons that don't work.

Avoid:

```text
[AI MAGIC]
[Coming Soon]
[Generate]
[Analyze]
```

unless the functionality genuinely exists.

If a feature is not implemented, don't expose it as a finished feature.

---

## V. HANDLE LOADING AND FAILURE STATES

Every asynchronous frontend operation should consider:

```text
Loading
Success
Empty
Error
```

Example:

While matching:

```text
Analyzing your image...
Finding visually similar items...
```

If no matches:

```text
No strong matches found yet.

We'll continue showing new potential matches
when relevant found-item reports are submitted.
```

If matching fails:

```text
We couldn't analyze this image.
Please try uploading a clearer photograph.
```

---

## W. ACCESSIBILITY

Use:

* semantic HTML
* labels for form fields
* keyboard-accessible controls
* useful alt text
* sufficient contrast
* clear validation messages
* visible focus states

Do not rely only on color to communicate status.

For example:

BAD:

red = lost
green = found

GOOD:

[LOST]
[FOUND]

with color as additional visual information.

---

## X. SECURITY REVIEW BEFORE COMPLETION

Before calling the project complete, perform a security review.

Check:

* authentication
* authorization
* password storage
* file uploads
* SQL injection
* XSS
* CSRF where applicable
* session security
* access control
* IDOR vulnerabilities
* sensitive information exposure
* unsafe filenames
* unrestricted file types
* unrestricted upload sizes

Especially verify:

A student must NOT be able to modify/delete another student's item simply by changing an ID in the URL.

---

## Y. CODE REVIEW BEFORE FINAL DELIVERY

Before declaring the project complete, perform a self-review.

Look for:

* unused imports
* dead code
* duplicate functions
* overly large functions
* inconsistent naming
* missing validation
* missing error handling
* security issues
* hardcoded secrets
* broken links
* placeholder UI
* TODOs
* fake features
* incorrect documentation
* missing tests

Then fix the issues found.

---

# 32. DEFINITION OF DONE

A feature is NOT considered complete merely because the code exists.

A feature is complete only when:

* implementation exists
* database changes work
* API works
* frontend works
* validation exists
* error states exist
* authorization is correct
* relevant tests exist
* documentation is updated
* the feature has been manually tested

Do not say "complete" until these conditions are satisfied.

---

# 33. DEVELOPMENT LOG

Maintain a simple:

```text
docs/development-log.md
```

Record significant decisions:

```text
## 2026-08-27

### Implemented
- Flask project structure
- MySQL connection
- User model

### Decisions
- Chose Flask because the project is a modular monolith.
- Chose MySQL because relational data and relationships are important.

### Issues
- None

### Next
- Authentication
```

Keep this concise.

This is not a diary. It is an engineering record.

---

# 34. FINAL PRINCIPLE

The goal is NOT:

"Generate as much code as possible."

The goal is:

"Build a small, understandable, tested, maintainable software system that happens to use AI for one important feature."

Prefer:

simple + correct + tested

over:

large + impressive-looking + fragile.

If you are uncertain between a clever solution and a simple reliable solution, choose the simple reliable solution and document why.
