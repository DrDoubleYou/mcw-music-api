# Contributing

Corrections, clearer setup instructions, and working creator examples are welcome.

1. Open an issue describing the problem or proposed improvement.
2. Make focused changes in a fork and open a pull request.
3. Run `python3 tests/smoke_test.py` for example changes. The tests use a local mock API and synthetic media; no account or real key is needed.

The test requirements are Python 3.10+, Node.js 22+, cURL, jq, FFmpeg, and ffprobe. GitHub Actions runs these checks for pull requests.

Keep credentials in environment variables, reject authenticated API redirects, and keep download requests free of API credentials. Save music attribution and license information with downloaded files. Document dependencies and expected output.

For changes to checked-in API documentation, compare against the live OpenAPI specification and update corresponding response examples. Do not present invented analysis scores or illustrative account usage as live data.

Never share API keys, sign-in links, tokens, email addresses, account IDs, or private analytics in issues, test fixtures, or pull requests. Use synthetic test values.

For account help or sensitive reports, use the [contact page](https://api.matthewcwright.com/contact/).
