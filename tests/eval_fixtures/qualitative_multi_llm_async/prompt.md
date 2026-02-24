I need a Python script that processes customer feedback in bulk using the
Claude API. We get about 50-100 feedback entries per day and right now
someone is manually reading each one.

For each feedback entry, the script should:
1. Classify the sentiment (positive, negative, neutral, mixed)
2. Extract any product/feature mentions
3. Categorize it (bug report, feature request, praise, complaint, question)
4. Suggest a response priority (urgent, normal, low)

Here's a sample of the input data format:

```json
[
  {
    "id": "fb-001",
    "customer": "alice@example.com",
    "text": "The new dashboard is amazing! So much faster than before. Only thing missing is the ability to export to PDF.",
    "source": "in-app",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  {
    "id": "fb-002",
    "customer": "bob@example.com",
    "text": "App keeps crashing when I try to upload files larger than 10MB. This is blocking my work. Please fix ASAP.",
    "source": "support-ticket",
    "timestamp": "2024-01-15T11:45:00Z"
  },
  {
    "id": "fb-003",
    "customer": "carol@example.com",
    "text": "Would be nice to have dark mode. Not urgent but would appreciate it.",
    "source": "feedback-form",
    "timestamp": "2024-01-15T14:20:00Z"
  }
]
```

The output should be a JSON file with the analysis results for each entry.

Write the complete script. It needs to handle a real production workload
of ~100 entries without being painfully slow or hitting rate limits.
Use the anthropic Python SDK.
