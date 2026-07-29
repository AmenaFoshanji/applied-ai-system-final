# Reproducible Execution Evidence

## Test suite

Command:

```bash
pytest -q
```

Output:

```text
....                                                                     [100%]
4 passed in 0.06s
```

## Retrieval evaluation harness

Command:

```bash
python evaluation.py
```

Output:

```text
Running retrieval evaluation...

Passed: 7/8
Hit rate: 0.88

Query: Where is the auth token generated?
  Expected: ['AUTH.md']
  Retrieved: ['AUTH.md', 'AUTH.md', 'AUTH.md']
  Hit: True

Query: What environment variables are required for authentication?
  Expected: ['AUTH.md']
  Retrieved: ['AUTH.md', 'AUTH.md', 'SETUP.md']
  Hit: True

Query: How do I connect to the database?
  Expected: ['DATABASE.md']
  Retrieved: ['DATABASE.md', 'SETUP.md', 'SETUP.md']
  Hit: True

Query: Which endpoint lists all users?
  Expected: ['API_REFERENCE.md']
  Retrieved: ['DATABASE.md', 'API_REFERENCE.md', 'API_REFERENCE.md']
  Hit: True

Query: What does the /api/projects/<project_id> route return?
  Expected: ['API_REFERENCE.md']
  Retrieved: ['DATABASE.md', 'API_REFERENCE.md', 'API_REFERENCE.md']
  Hit: True

Query: Is there any mention of payment processing in these docs?
  Expected: []
  Retrieved: []
  Hit: False

Query: How does a client refresh an access token?
  Expected: ['AUTH.md']
  Retrieved: ['AUTH.md', 'AUTH.md', 'API_REFERENCE.md']
  Hit: True

Query: Which fields are stored in the users table?
  Expected: ['API_REFERENCE.md', 'DATABASE.md']
  Retrieved: ['DATABASE.md', 'API_REFERENCE.md', 'API_REFERENCE.md']
  Hit: True
```
