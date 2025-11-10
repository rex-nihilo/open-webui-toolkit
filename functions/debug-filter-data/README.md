# Debug Filter Data

A powerful and configurable Function Filter plugin for Open WebUI that helps developers debug and understand the internal data flow of inlet, outlet, and stream processes.

`Debug Filter Data` is part of the `Open WebUI Toolkit` project.

[![Version](https://img.shields.io/badge/version-0.4.008-green.svg?style=flat-square)](https://github.com/rex-nihilo/open-webui-toolkit) [![License MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT) [![OpenWebUI](https://img.shields.io/badge/OpenWebUI-Filter-blue.svg?style=flat-square&logo=github)](https://github.com/open-webui/open-webui) [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat-square&logo=python)](https://www.python.org/)

## 📋 Overview

Debug Filter Data is an essential tool for Open WebUI plugin developers and system administrators who need to:

- Understand the data structure flowing through the system
- Debug custom filters and pipelines
- Monitor model interactions and responses
- Track user messages and metadata
- Analyze streaming responses

## ✨ Features

### Core Functionality

- **Multi-point Logging**: Capture data at inlet (incoming), outlet (outgoing), and stream (real-time) stages
- **Flexible Output**: Send debug information to chat interface, console, and/or rotating log files
- **Selective Data Display**: Choose exactly which data fields to log (body, user, metadata, messages, etc.)
- **Custom Key Tracking**: Monitor specific nested data paths with dot notation support (e.g., `body.model.name` or `messages[0].content`)

### Security & Privacy

- **Data Obfuscation**: Automatically mask sensitive fields (emails, API keys, passwords)
- **Configurable Masking**: Define which keys should be obfuscated
- **Safe Error Handling**: Graceful degradation without exposing sensitive information

### User Experience

- **Real-time Status Updates**: Visual feedback during filter execution
- **Chat History Cleaning**: Automatically remove old debug reports
- **Formatted Output**: Beautiful JSON formatting with proper indentation
- **Size Information**: Display data sizes in human-readable format (B/KB/MB/GB)

### Developer Tools

- **Summary Reports**: Quick overview of model, user, message count, and available keys
- **File Rotation**: Automatic log file management with configurable size limits
- **Debug Modes**: Console logging for plugin development
- **Priority Control**: Set execution order when multiple filters are active

## 🚀 Installation

1. **Access Open WebUI Admin Panel**
  
  - Navigate to Settings → Admin Settings → Functions
2. **Add New Function**
  
  - Click `+ New Function` button to create a new function
  - Select "New Function"
3. **Import the Plugin**
  
  - Copy the entire content of [debug-filter-data.py](https://github.com/rex-nihilo/open-webui-toolkit/blob/main/functions/debug-filter-data/debug-filter-data.py)
  - Paste it into the function editor
  - For "Function Name", use "Debug Filter Data"
  - Add a description in "Function Description"
  - Save the function
4. **Enable the Function**
  
  - Toggle the function ON
  - Configure Valves according to your needs (See the Configuration section above for help).
5. **Enable for model**
  
  - To use with a specific model, go to the model settings and enable "Debug Filter Data" filter.
  - To use with all default models, click `...` (More) on the function page and activate "Global".
6. **In the Chat**
  
  - Click on the "Integrations" icon and enable "Debug Filter Data".
  - For each response, it is possible to enable or disable this filter here.

## ⚙️ Configuration

### Valves (UI Configuration)

#### Priority

- **priority**: Execution order when multiple filters are active (default: `0`)

#### Interaction to Debug

- **log_inlet**: Capture incoming request data (default: `true`)
- **log_outlet**: Capture outgoing response data (default: `true`)
- **log_stream**: Capture streaming response events (default: `false`)
  WARNING: If the response is long, a lot of data may be returned.

#### Send To

- **send_to_chat**: Display debug info in chat interface (default: `true`)
- **send_to_console**: Output to console/terminal (default: `true`) 
  The prefix [DEBUG FILTER DATA] is used.
- **send_to_file**: Write to log file (default: `false`)
- **file_path**: Location of log file (default: `/app/backend/data/debug_filter_data.log`)
  This is the path usually used if Open WebUI is installed via Docker.

#### Data to Show

- **show_summary**: Display summary information (default: `true`)
- **show_body**: Show request/response body (default: `false`)
- **show_user**: Show user information (default: `false`)
- **show_metadata**: Show metadata (default: `false`)
- **show_model**: Show model information (default: `false`)
- **show_messages**: Show message history (default: `false`)
- **show_chat_id**: Show chat identifier (default: `false`)
- **show_session_id**: Show session identifier (default: `false`)
- **show_message_id**: Show message identifier (default: `false`)
- **show_event_emitter**: Show event emitter object (default: `false`)
- **show_event_call**: Show event call object (default: `false`)
- **show_files**: Show attached files (default: `false`)
- **show_request**: Show HTTP request object (default: `false`)
- **show_task**: Show task information (default: `false`)
- **show_task_body**: Show task body (default: `false`)
- **show_tools**: Show available tools (default: `false`)
- **show_custom_key**: Track specific nested data path (e.g., `body.model.ollama.name`, `body.messages[0].content`)
  Useful if you only want to track a single piece of data.

## 📖 Usage Examples

### Basic Debugging

1. Enable the filter in Open WebUI
2. Set `show_summary` to `true` in Valves
3. Send a message to your chat (Don't forget to activate the filter in "Integrations")
4. Check the debug report at the end of the assistant's response

### Tracking Custom Data

To monitor a specific field:

```
show_custom_key: body.messages[0].content
```

This will extract and display the content of the first message.

### Console-Only Logging

For development without cluttering the chat:

- Set `send_to_chat` to `false`
- Set `send_to_console` to `true`
- Monitor your terminal/console for debug output

### Stream Analysis

To understand how responses are generated:

- Set `log_stream` to `true`
- Check console/file output for each streaming event
- Useful for debugging streaming issues or understanding token generation

## 🔧 Advanced Configuration

### Code-Level Customization

All default values are centralized in the `Config` class. Developers can modify these constants directly in the code for permanent changes:

```python
class Config:
    # Debug options
    DEBUG_INFO = False # Enable info messages
    DEBUG_WARNING = True  # Enable warnings
    DEBUG_ERROR = True  # Enable error messages

    # Log options
    LOG_BACKUP_COUNT = 5  # Number of backup files
    LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
    LOG_SIZE = 10  # Max log file size in MB

    # Message options
    MESSAGE_CLEAN_CHAT_HISTORY = True # Clean the message history
    MESSAGE_REMOVE_OLD_REPORT = True # Remove old reports from the chat

    # Security options
    SECURITY_OBFUSCATE = True
    SECURITY_OBFUSCATE_DATA = ["email", "date_of_birth", "api_key"]
    SECURITY_OBFUSCATE_MASK = "**** OBFUSCATED ****"
```

### Custom Key Path Syntax

The `show_custom_key` valve supports dot notation and array indexing:

- **Simple key**: `body.model`
- **Nested key**: `body.model.ollama.name`
- **Array index**: `messages[0]`
- **Complex path**: `body.messages[0].content`
- **Metadata filter**: `__metadata__.filter_ids`

## 📊 Output Format

### Chat Output

Debug reports in chat are formatted with:

- Clear section headers (🔵 INLET, 🟢 OUTLET, ⚡️ STREAM)
- Formatted JSON with syntax highlighting
- Size information for each section
- Timestamps for tracking
- Model and user information

### Console Output

Terminal logs include:

- Delimiter lines for easy scanning
- Timestamps
- Structured JSON output
- Debug level indicators

### File Output

Log files contain:

- Automatic rotation when size limit is reached
- Timestamp prefixes
- Complete data dumps
- Configurable log level filtering

## 🛡️ Security Considerations

1. **Sensitive Data**: By default, the plugin obfuscates common sensitive fields
2. **Production Use**: Consider disabling `send_to_chat` in production to avoid exposing internal data
3. **File Permissions**: Ensure log file directory has appropriate permissions
4. **Custom Keys**: Be careful when tracking custom keys that might contain sensitive information

## 🐛 Troubleshooting

### Plugin Not Showing Output

- Check that the filter toggle is ON in the UI
- Ensure that the function is enabled (globally or for the selected model).
- Verify at least one "send_to" option is enabled
- Ensure at least one "log_" interaction is enabled
- Ensure that the filter is enabled in the chat (Integrations icon below the chat).

### File Logging Fails

- Verify the file path exists and is writable
- Check Docker container permissions if using containerized Open WebUI
- Review console for error messages

### Missing Data in Reports

- Enable the specific `show_*` valve for the data you need
- Check if the data actually exists in the context (some fields are optional)
- Review console logs for warnings about missing keys

### Stream Logging Not Working

- Ensure `log_stream` is set to `true`
- Check console output (stream data is very verbose)
- Verify the model supports streaming

## 🔄 Version History

### v0.4.008 (2025-11-10) First public release

- Custom key path tracking with dot notation and array indexing
- Improved error handling and resilience
- Enhanced documentation and code comments
- Optimized data serialization for complex objects
- Better obfuscation system

## 📌 Todo

- Better memory management (TTL/cleanup)
- Improve the obfuscation system
- Multiple custom keys

## 📝 Requirements

- **Open WebUI**: v0.6.10 or higher
- **Tested On**: Open WebUI v0.6.36
- **Python**: 3.8+

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://mit-license.org/) file for details.

## 👤 Author

**Rex Nihilo**

- GitHub: [@rex-nihilo](https://github.com/rex-nihilo)
- Project: [Open WebUI Toolkit](https://github.com/rex-nihilo/open-webui-toolkit)
- Website: [https://rexnihilo.com](https://rexnihilo.com)

## 💖 Support

If you find this plugin helpful:

- ⭐ Star the repository
- 🐛 Report bugs and issues
- 💡 Suggest new features
- 📢 Share with other developers

## 🙏 Acknowledgments

- Open WebUI team for creating an amazing platform
- The Open WebUI community for feedback and support
- All contributors who help improve this tool

---

**Note**: This is a development and debugging tool. Use with caution in production environments and always be mindful of sensitive data exposure.
