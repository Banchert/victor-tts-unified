# Tests Directory

This directory contains test files for the VICTOR TTS Unified project.

## Test Files

### test_api.py
Comprehensive API testing script that tests all endpoints of the TTS system including:
- Health check
- Model listing
- Voice listing
- TTS only functionality
- TTS + RVC unified functionality
- TTS + RVC full functionality
- Audio file saving

### test_text_limits.py
Tests for text length limits and system boundaries including:
- Text length limit testing
- Edge TTS limits
- Unified endpoint testing
- Full TTS endpoint testing
- N8N compatibility testing

## Running Tests

To run the tests, make sure the main API server is running first:

```bash
python main_api_server.py
```

Then run the tests:

```bash
# Run API tests
python tests/test_api.py

# Run text limit tests
python tests/test_text_limits.py
```

## Test Output

Test results will be displayed in the console with detailed information about:
- Request/response status
- Processing times
- Generated audio files (if applicable)
- Error messages (if any)

## Notes

- Tests require the main API server to be running
- Some tests may generate temporary audio files
- Test files are automatically cleaned up after execution
- All tests are designed to work with the N8N integration 