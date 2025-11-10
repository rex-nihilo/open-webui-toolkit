"""
title: Debug Filter Data
author: Rex Nihilo
author_url: https://github.com/rex-nihilo/open-webui-toolkit
funding_url: https://github.com/open-webui
required_open_webui_version: 0.6.10
tested_open_webui_version: 0.6.36
version: 0.4.008
date: 2025-11-10
license: MIT

description: A configurable Function Filter for Open WebUI to debug and log inlet/outlet/stream data. Logs to chat, console, or file with options for data selection, obfuscation, and rotation. Ideal for plugin development and understanding Open WebUI internals.

"""

import json
import os
import re
from datetime import datetime
from typing import Optional, Callable, List, Any
from pydantic import BaseModel, Field
from collections.abc import Mapping, Sequence
import logging
from logging.handlers import RotatingFileHandler


class Config:
    """Centralized configuration constants for the plugin.

    This class holds all default values for Valves, options, and other settings.
    Users/devs can override these in code for customization without UI changes.
    """

    # Valves: Priority by default
    VALVES_PRIORITY = 0 # Priority level for filter execution order (int)

    # Valves: Interaction to debug by default
    VALVES_LOG_INLET = True # Log inlet data (incoming requests) (bool)
    VALVES_LOG_OUTLET = True # Log outlet data (outgoing requests) (bool)
    VALVES_LOG_STREAM = False # Log stream data (streamed model responses) (bool)

    # Valves: Send to by default
    VALVES_SEND_TO_CHAT = True # Send debug info directly in chat interface (bool)
    VALVES_SEND_TO_CONSOLE = True # Send debug info to console (bool)
    VALVES_SEND_TO_FILE = False # Send debug info to file (bool)
    VALVES_FILE_PATH = "/app/backend/data/debug_filter_data.log" # Path of log file (str)

    # Valves: Data to show by default
    VALVES_SHOW_SUMMARY = True # Show summary info (bool)
    VALVES_SHOW_BODY = False # Show body info (bool)
    VALVES_SHOW_USER = False # Show __user__ info (bool)
    VALVES_SHOW_METADATA = False # Show __metadata__ info (bool)
    VALVES_SHOW_MODEL = False # Show __model__ info (bool)
    VALVES_SHOW_MESSAGES = False # Show __messages__ info (bool)
    VALVES_SHOW_CHAT_ID = False # Show __chat_id__ info (bool)
    VALVES_SHOW_SESSION_ID = False # Show __session_id__ info (bool)
    VALVES_SHOW_MESSAGE_ID = False # Show __message_id__ info (bool)
    VALVES_SHOW_EVENT_EMITTER = False # Show __event_emitter__ info (bool)
    VALVES_SHOW_EVENT_CALL = False # Show __event_call__ info (bool)
    VALVES_SHOW_FILES = False # Show __files__ info (bool)
    VALVES_SHOW_REQUEST = False # Show __request__ info (bool)
    VALVES_SHOW_TASK = False # Show __task__ info (bool)
    VALVES_SHOW_TASK_BODY = False # Show __task_body__ info (bool)
    VALVES_SHOW_TOOLS = False # Show __tools__ info (bool)

    # Debug options
    DEBUG_INFO = False # Enable debug info in console (for plugin development ONLY) (recommended: False) (bool)
    DEBUG_WARNING = True # Enable warning features in console (recommended: True) (bool)
    DEBUG_ERROR = True # Enable error features in console (recommended: True) (bool)

    # Log options
    LOG_BACKUP_COUNT = 5  # Number of backup log files to keep (int)
    LOG_ERROR_WARNING = True  # Show warnings in console if file logging fails (bool)
    LOG_LEVEL = "INFO"  # Log level for file (DEBUG, INFO, WARNING, ERROR) (str)
    LOG_SIZE = 10  # Limit log size (in MB) (int)

    # Message options
    MESSAGE_CLEAN_CHAT_HISTORY = True # Clean the message history of the plugin content displayed in the chat (recommended: True) (bool)
    MESSAGE_REMOVE_OLD_REPORT = True # Remove old reports from the chat to keep only the latest one (bool)

    # Result options in the chat
    RESULT_HEADER = True # Show info (title, model, etc) in chat result (bool)
    RESULT_FOOTER = True # Show footer in chat result (bool)
    RESULT_KEYWORD_BEGIN = "---- DFD REPORT BEGIN ----" # Keyword at the beginning of the report in the chat, used by 'MESSAGE_CLEAN_CHAT_HISTORY' (str)
    RESULT_KEYWORD_END = "---- DFD REPORT END ----" # Keyword at the end of the report in the chat, used by 'MESSAGE_CLEAN_CHAT_HISTORY' (str)

    # Security options
    SECURITY_OBFUSCATE = True # Obfuscate sensitive data (recommended: True) (bool)
    SECURITY_OBFUSCATE_DATA = ["email","date_of_birth", "api_key"] # List of keys whose values must be obfuscated (list)
    SECURITY_OBFUSCATE_MASK = "**** OBFUSCATED ****" # Text used to indicate that the value is obfuscated (str)

    # Status features in Open WebUI chat
    STATUS_USE = True # Show status info when running (bool)
    STATUS_INFO_START = "🗐 Debug Filter Data is running..." # Text of the status at the start (str)
    STATUS_INFO_INLET_START = "🗐 Debug Filter Data - Step inlet..." # Text of the status at the inlet start (str)
    STATUS_INFO_INLET_OK = "🗐 Debug Filter Data - Step inlet OK" # Text of the status at the inlet end (str)
    STATUS_INFO_OUTLET_START = "🗐 Debug Filter Data - Step outlet..." # Text of the status at the inlet start (str)
    STATUS_INFO_OUTLET_OK = "🗐 Debug Filter Data - Step outlet OK" # Text of the status at the inlet end (str)
    STATUS_INFO_STREAM_START = "🗐 Debug Filter Data - Step stream..." # Text of the status at the stream start (str)
    STATUS_INFO_STREAM_OK = "🗐 Debug Filter Data - Step stream OK" # Text of the status at the stream end (str)
    STATUS_INFO_COMPLETED = "🗐 Debug Filter Data completed" # Text of the status at the end (str)

    # Title options
    TITLE_DEBUG = "DEBUG FILTER DATA RESULT" # Main title (str)
    TITLE_INLET = "🔵 INLET DATA" # Title for intlet data (str)
    TITLE_OUTLET = "🟢 OUTLET DATA" # Title for outlet data (str)
    TITLE_STREAM = "⚡️ STREAM DATA" # Title for stream data (str)

    # Other data
    KEYS_UPPERCASE = ["summary"] # Keys displayed in uppercase (list)
    SWITCH_ICON = """data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPCEtLSBHZW5lcmF0b3I6IHZpc2lvbmNvcnRleCBWVHJhY2VyIDAuNi40IC0tPgo8c3ZnIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iMTI4IiBoZWlnaHQ9IjEyOCI+CjxwYXRoIGQ9Ik0wIDAgQzI1LjQxIDAgNTAuODIgMCA3NyAwIEM3NyAzLjk2IDc3IDcuOTIgNzcgMTIgQzgxLjYyIDEyIDg2LjI0IDEyIDkxIDEyIEM5MSAxNS45NiA5MSAxOS45MiA5MSAyNCBDOTUuNjIgMjQgMTAwLjI0IDI0IDEwNSAyNCBDMTA1IDU3LjY2IDEwNSA5MS4zMiAxMDUgMTI2IEM3Ny45NCAxMjYgNTAuODggMTI2IDIzIDEyNiBDMjMgMTIxLjM4IDIzIDExNi43NiAyMyAxMTIgQzE5LjM3IDExMiAxNS43NCAxMTIgMTIgMTEyIEMxMiAxMDcuMzggMTIgMTAyLjc2IDEyIDk4IEM4LjA0IDk4IDQuMDggOTggMCA5OCBDMCA2NS42NiAwIDMzLjMyIDAgMCBaIE00IDQgQzQgMzMuNyA0IDYzLjQgNCA5NCBDNi42NCA5NCA5LjI4IDk0IDEyIDk0IEMxMiA2Ni45NCAxMiAzOS44OCAxMiAxMiBDMzIuMTMgMTIgNTIuMjYgMTIgNzMgMTIgQzczIDkuMzYgNzMgNi43MiA3MyA0IEM1MC4yMyA0IDI3LjQ2IDQgNCA0IFogTTE2IDE2IEMxNiA0Ni4zNiAxNiA3Ni43MiAxNiAxMDggQzE4LjMxIDEwOCAyMC42MiAxMDggMjMgMTA4IEMyMyA4MC4yOCAyMyA1Mi41NiAyMyAyNCBDNDQuMTIgMjQgNjUuMjQgMjQgODcgMjQgQzg3IDIxLjM2IDg3IDE4LjcyIDg3IDE2IEM2My41NyAxNiA0MC4xNCAxNiAxNiAxNiBaIE0yOCAyOCBDMjggNTkuMDIgMjggOTAuMDQgMjggMTIyIEM1Mi4wOSAxMjIgNzYuMTggMTIyIDEwMSAxMjIgQzEwMSA5MC45OCAxMDEgNTkuOTYgMTAxIDI4IEM3Ni45MSAyOCA1Mi44MiAyOCAyOCAyOCBaICIgZmlsbD0iIzAwMDAwMCIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMTIsMSkiLz4KPHBhdGggZD0iTTAgMCBDMTcuODIgMCAzNS42NCAwIDU0IDAgQzU0IDEuMzIgNTQgMi42NCA1NCA0IEMzNi4xOCA0IDE4LjM2IDQgMCA0IEMwIDIuNjggMCAxLjM2IDAgMCBaICIgZmlsbD0iIzAwMDAwMCIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNDksMTA4KSIvPgo8cGF0aCBkPSJNMCAwIEMxNy44MiAwIDM1LjY0IDAgNTQgMCBDNTQgMS4zMiA1NCAyLjY0IDU0IDQgQzM2LjE4IDQgMTguMzYgNCAwIDQgQzAgMi42OCAwIDEuMzYgMCAwIFogIiBmaWxsPSIjMDAwMDAwIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSg0OSw5NCkiLz4KPHBhdGggZD0iTTAgMCBDMTcuODIgMCAzNS42NCAwIDU0IDAgQzU0IDEuMzIgNTQgMi42NCA1NCA0IEMzNi4xOCA0IDE4LjM2IDQgMCA0IEMwIDIuNjggMCAxLjM2IDAgMCBaICIgZmlsbD0iIzAwMDAwMCIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNDksODApIi8+CjxwYXRoIGQ9Ik0wIDAgQzE3LjgyIDAgMzUuNjQgMCA1NCAwIEM1NCAxLjMyIDU0IDIuNjQgNTQgNCBDMzYuMTggNCAxOC4zNiA0IDAgNCBDMCAyLjY4IDAgMS4zNiAwIDAgWiAiIGZpbGw9IiMwMDAwMDAiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDQ5LDY2KSIvPgo8cGF0aCBkPSJNMCAwIEMxNy44MiAwIDM1LjY0IDAgNTQgMCBDNTQgMS4zMiA1NCAyLjY0IDU0IDQgQzM2LjE4IDQgMTguMzYgNCAwIDQgQzAgMi42OCAwIDEuMzYgMCAwIFogIiBmaWxsPSIjMDAwMDAwIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSg0OSw1MikiLz4KPHBhdGggZD0iTTAgMCBDMTcuODIgMCAzNS42NCAwIDU0IDAgQzU0IDEuMzIgNTQgMi42NCA1NCA0IEMzNi4xOCA0IDE4LjM2IDQgMCA0IEMwIDIuNjggMCAxLjM2IDAgMCBaICIgZmlsbD0iIzAwMDAwMCIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNDksMzkpIi8+Cjwvc3ZnPgo=""" # Icon for UI (with a Data URI) will show up as a little image next to the filter's name. You can use any SVG as long as it's Data URI encoded (str)


class Filter:
    """Main filter class for intercepting inlet/outlet/stream in Open WebUI.

    Manages temp storage, logging, and data processing with configurable options.
    """

    class Valves(BaseModel):
        """Configurable settings exposed in Open WebUI Valves UI.

        These fields control logging, display, and priority. Defaults from Config.
        Changes here override Config constants dynamically.
        """

        # Priority
        priority: int = Field(
            default=Config.VALVES_PRIORITY,
            description=f"Priority level for filter execution order (default: '{Config.VALVES_PRIORITY}')",
        )

        # Interaction to debug
        log_inlet: bool = Field(
            default=Config.VALVES_LOG_INLET,
            description=f"Log inlet (incoming requests) (default: '{Config.VALVES_LOG_INLET}')",
        )
        log_outlet: bool = Field(
            default=Config.VALVES_LOG_OUTLET,
            description=f"Log outlet (outgoing responses) (default: '{Config.VALVES_LOG_OUTLET}')",
        )
        log_stream: bool = Field(
            default=Config.VALVES_LOG_STREAM,
            description=f"Log stream (streamed model responses) (default: '{Config.VALVES_LOG_STREAM}')",
        )

        # Send to
        send_to_chat: bool = Field(
            default=Config.VALVES_SEND_TO_CHAT,
            description=f"Send debug info directly in chat interface (default: '{Config.VALVES_SEND_TO_CHAT}')",
        )
        send_to_console: bool = Field(
            default=Config.VALVES_SEND_TO_CONSOLE,
            description=f"Send debug info to console (default: '{Config.VALVES_SEND_TO_CONSOLE}')",
        )
        send_to_file: bool = Field(
            default=Config.VALVES_SEND_TO_FILE,
            description=f"Send debug info to log file (default: '{Config.VALVES_SEND_TO_FILE}')",
        )
        file_path: str = Field(
            default=Config.VALVES_FILE_PATH,
            description=f"Path of log file (default: '{Config.VALVES_FILE_PATH}')",
        )

        # Data to show
        show_summary: bool = Field(
            default=Config.VALVES_SHOW_SUMMARY,
            description=f"Show SUMMARY info (default: '{Config.VALVES_SHOW_SUMMARY}')",
        )
        show_body: bool = Field(
            default=Config.VALVES_SHOW_BODY,
            description=f"Show 'body' info (default: '{Config.VALVES_SHOW_BODY}')",
        )
        show_user: bool = Field(
            default=Config.VALVES_SHOW_USER,
            description=f"Show '__user__' info (default: '{Config.VALVES_SHOW_USER}')",
        )
        show_metadata: bool = Field(
            default=Config.VALVES_SHOW_METADATA,
            description=f"Show '__metadata__' info (default: '{Config.VALVES_SHOW_METADATA}')",
        )
        show_model: bool = Field(
            default=Config.VALVES_SHOW_MODEL,
            description=f"Show '__model__' info (default: '{Config.VALVES_SHOW_MODEL}')",
        )
        show_messages: bool = Field(
            default=Config.VALVES_SHOW_MESSAGES,
            description=f"Show '__messages__' info (default: '{Config.VALVES_SHOW_MESSAGES}')",
        )
        show_chat_id: bool = Field(
            default=Config.VALVES_SHOW_CHAT_ID,
            description=f"Show '__chat_id__' info (default: '{Config.VALVES_SHOW_CHAT_ID}')",
        )
        show_session_id: bool = Field(
            default=Config.VALVES_SHOW_SESSION_ID,
            description=f"Show '__session_id__' info (default: '{Config.VALVES_SHOW_SESSION_ID}')",
        )
        show_message_id: bool = Field(
            default=Config.VALVES_SHOW_MESSAGE_ID,
            description=f"Show '__message_id__' info (default: '{Config.VALVES_SHOW_MESSAGE_ID}')",
        )
        show_event_emitter: bool = Field(
            default=Config.VALVES_SHOW_EVENT_EMITTER,
            description=f"Show '__event_emitter__' info (default: '{Config.VALVES_SHOW_EVENT_EMITTER}')",
        )
        show_event_call: bool = Field(
            default=Config.VALVES_SHOW_EVENT_CALL,
            description=f"Show '__event_call__' info (default: '{Config.VALVES_SHOW_EVENT_CALL}')",
        )
        show_files: bool = Field(
            default=Config.VALVES_SHOW_FILES,
            description=f"Show '__files__' info (default: '{Config.VALVES_SHOW_FILES}')",
        )
        show_request: bool = Field(
            default=Config.VALVES_SHOW_REQUEST,
            description=f"Show '__request__' info (default: '{Config.VALVES_SHOW_REQUEST}')",
        )
        show_task: bool = Field(
            default=Config.VALVES_SHOW_TASK,
            description=f"Show '__task__' info (default: '{Config.VALVES_SHOW_TASK}')",
        )
        show_task_body: bool = Field(
            default=Config.VALVES_SHOW_TASK_BODY,
            description=f"Show '__task_body__' info (default: '{Config.VALVES_SHOW_TASK_BODY}')",
        )
        show_tools: bool = Field(
            default=Config.VALVES_SHOW_TOOLS,
            description=f"Show '__tools__' info (default: '{Config.VALVES_SHOW_TOOLS}')",
        )
        show_custom_key: str = Field(
            default="",
            description="Custom key path to track (e.g., 'body.model.ollama.name' or 'body.messages[0].content' or '__metadata__.filter_ids'). Leave empty to disable."
        )

        # This 'pass' helps for parsing and is recommended
        pass


    def __init__(self):
        self.valves = self.Valves() # Initialize Valves instance
        self.toggle = True # Create switch UI in Open WebUI
        self.icon = Config.SWITCH_ICON # Icon for UI
        self.debug_inlet_temp = {} # Init debug temp to get inlet data from outlet data
        self.debug_stream_temp = {} # Init debug temp to get stream data from outlet data

        # Setup logger for file output with rotation
        self.logger = logging.getLogger("debug_filter_data")
        try:
            handler = RotatingFileHandler(
                self.valves.file_path,
                maxBytes=Config.LOG_SIZE * 1024 * 1024,
                backupCount=Config.LOG_BACKUP_COUNT
            )
            handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
            self.logger.addHandler(handler)
            self.logger.setLevel(getattr(logging, Config.LOG_LEVEL.upper()))
            self.logger.propagate = False
        except Exception as e:

            #DEBUG ERROR
            if Config.DEBUG_ERROR:
                print(f"[DEBUG FILTER DATA] ERROR | Failed to initialize logger: {e}")

            # Fallback to NullHandler to avoid crashes
            self.logger.addHandler(logging.NullHandler())

        # DEBUG INFO
        if Config.DEBUG_INFO:
            print(f"[DEBUG FILTER DATA] INFO | Init")


    def _format_json(self, data: dict | None = None) -> str:
        """Format data as indented JSON string, with obfuscation and fallback for non-serializables.

        Converts callables/objects to str representations to avoid errors.
        """

        # No data
        if data is None:
            return "{}"  # Return empty JSON string instead of dict

        # Obfuscate sensitive data if enabled
        obfuscated_data = self._obfuscate_data(data) if Config.SECURITY_OBFUSCATE else data

        # Pre-convert non-serializable items (e.g., functions) to str
        def make_serializable(obj):

            if isinstance(obj, dict):
                return {k: make_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [make_serializable(item) for item in obj]
            elif callable(obj):  # Functions or callables
                return f"<callable: {str(obj)}>"
            elif not isinstance(obj, (str, int, float, bool, type(None))):  # Other non-serializables
                return str(obj)

            return obj
        
        serializable_data = make_serializable(obfuscated_data)

        # Format
        try:
            # Json format
            formatted_data = json.dumps(serializable_data, indent=2, ensure_ascii=False)

        # Format error
        except Exception as e:
            # Error: no format
            formatted_data = str(serializable_data)  # Fallback if problem (use serializable data)

            # DEBUG ERROR
            if Config.DEBUG_ERROR:
                print(f"[DEBUG FILTER DATA] ERROR | Error formatting data: {e}")
                print(f"[DEBUG FILTER DATA] DEBUG | {serializable_data}\n")

        return formatted_data


    def _format_size(self, size: int) -> str:
        """Format byte size into human-readable string (B/KB/MB/GB).

        Handles negative/invalid sizes gracefully.
        """

        # Negative or Zero size
        if not isinstance(size, int) or size < 0:
            return "0"

        # Units
        units = ["bytes", "KB", "MB", "GB", "TB"]
        i = 0

        # Get unit
        while size >= 1024 and i < len(units) - 1:
            size /= 1024
            i += 1

        # Return new format
        if i == 0:
            return f"{size} {units[i]}"
        else:
            return f"{size:.2f} {units[i]}".rstrip('0').rstrip('.')


    def _get_by_path(self, data: dict | list | None, path: str) -> Any:
        """Extract value from nested dict/list using dot-path with [index] support.

        Safe against invalid paths/indexes; returns None on failure with optional warning log.
        """

        # Empty
        if not path or data is None:
            return None
        
        # Tokenize path: find all keys and [indexes] with regex
        # Matches keys or [num]
        tokens = []
        # Regex to split on '.' but capture [num] separately
        parts = re.findall(r'[^.\[\]]+|\[\d+\]', path)
        for part in parts:
            if part.startswith('[') and part.endswith(']'):
                index_str = part[1:-1]
                if index_str.isdigit():
                    tokens.append(int(index_str))
                else:

                    # DEBUG WARNING
                    if Config.DEBUG_WARNING:
                        print(f"[DEBUG FILTER DATA] WARNING | Invalid index in path '{path}': {index_str}")

                    return None
            else:
                tokens.append(part)

        # Check path
        current = data
        try:
            for token in tokens:
                if isinstance(token, int) and isinstance(current, list):
                    current = current[token]  # List index
                elif isinstance(current, dict):
                    current = current.get(token)  # Dict key
                else:
                    return None
                if current is None:
                    return None
            return current

        # Invalid path
        except (IndexError, ValueError, TypeError, KeyError) as e:

            # DEBUG WARNING
            if Config.DEBUG_WARNING:
                print(f"[DEBUG FILTER DATA] WARNING | Invalid custom key path '{path}': {e}")

            return None


    def _get_json_size(self, data: Any) -> int:
        """Calculate the byte size of JSON-serialized data.

        Returns 0 on failure or None. Used for size display in logs/chat.
        """

        # No data
        if data is None:
            return 0

        # Size
        try:
            json_str = json.dumps(data, ensure_ascii=False)  # To include non-ASCII characters without escaping them
            return len(json_str.encode('utf-8'))

        # Size error
        except Exception as e:

            # DEBUG ERROR
            if Config.DEBUG_ERROR:
                print(f"[DEBUG FILTER DATA] ERROR | Failed to get JSON size: {e}")

            return 0


    def _log(
        self,
        message: str | None = None,  # The message to log
        data: dict | None = None,  # The data to log
        indent: bool = True,  # Indent the data
        delimiters: str | None = None  # Delimiters to log (top/bottom)
        ):
        """Log message and/or data to console, file, and/or chat based on settings.

        Handles formatting, sending to destinations, and error resilience.
        """

        # Init
        log_entry = ""

        # Top delimiter
        if delimiters == "all" or delimiters == "top":
            log_entry += f"\n{'='*80}\n"

        # Message
        if message is not None:
            log_entry += f"{message}\n"

        # Data
        if data:
            # Format data
            if indent:
                log_entry += self._format_json(data) + "\n"
            else:
                log_entry += str(data) + "\n"

        # Bottom delimiter
        if delimiters == "all" or delimiters == "bottom":
            log_entry += f"\n{'='*80}\n"

        # Log to console
        if self.valves.send_to_console:
            print(log_entry)

        # Log to file
        if self.valves.send_to_file:

            try:
                self.logger.info(log_entry)
            except Exception as e:

                # DEBUG WARNING
                if Config.LOG_ERROR_WARNING:
                    print(f"[DEBUG FILTER DATA] WARNING | File logging failed: {e}")


    def _obfuscate_data(self, data: Any, depth: int = 0) -> Any:
        """Recursively obfuscate sensitive keys in data structures.

        Limits depth to prevent infinite recursion. Uses Config.SECURITY_* settings.
        """

        # Limit recursion depth
        if depth > 10:
            return data

        # Check
        if isinstance(data, dict):
            return {k: Config.SECURITY_OBFUSCATE_MASK if (Config.SECURITY_OBFUSCATE and k.lower() in [key.lower() for key in Config.SECURITY_OBFUSCATE_DATA]) else self._obfuscate_data(v, depth + 1) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._obfuscate_data(item) for item in data]
        elif isinstance(data, (set, tuple)):
            return type(data)(self._obfuscate_data(item) for item in data)
        else:
            return data


    def _select(self, data: dict | None = None) -> dict | None:
        """Filter and select specific keys from data based on Valves show_* settings.

        Includes custom key if enabled. Returns None on failure.
        """

        # No data
        if data is None:
            return None

        # Select data
        try:
            selected_data = {}

            # Summary
            if self.valves.show_summary:
                selected_data["summary"] = data.get("summary")

            # Body
            if self.valves.show_body:
                selected_data["body"] = data.get("body")

            # __user__
            if self.valves.show_user:
                selected_data["__user__"] = data.get("__user__")

            # __metadata__
            if self.valves.show_metadata:
                selected_data["__metadata__"] = data.get("__metadata__")

            # __model__
            if self.valves.show_model:
                selected_data["__model__"] = data.get("__model__")

            # __messages__
            if self.valves.show_messages:
                selected_data["__messages__"] = data.get("__messages__")

            # __chat_id__
            if self.valves.show_chat_id:
                selected_data["__chat_id__"] = data.get("__chat_id__")

            # __session_id__
            if self.valves.show_session_id:
                selected_data["__session_id__"] = data.get("__session_id__")

            # __message_id__
            if self.valves.show_message_id:
                selected_data["__message_id__"] = data.get("__message_id__")

            # __event_emitter__
            if self.valves.show_event_emitter:
                selected_data["__event_emitter__"] = data.get("__event_emitter__")

            # __event_call__
            if self.valves.show_event_call:
                selected_data["__event_call__"] = data.get("__event_call__")

            # __files__
            if self.valves.show_files:
                selected_data["__files__"] = data.get("__files__")

            # __request__
            if self.valves.show_request:
                selected_data["__request__"] = data.get("__request__")

            # __task__
            if self.valves.show_task:
                selected_data["__task__"] = data.get("__task__")

            # __task_body__
            if self.valves.show_task_body:
                selected_data["__task_body__"] = data.get("__task_body__")

            # __tools__
            if self.valves.show_tools:
                selected_data["__tools__"] = data.get("__tools__")

            # Custom key (new logic)
            if self.valves.show_custom_key:
                custom_value = self._get_by_path(data, self.valves.show_custom_key)
                custom_key_display = f"CUSTOM KEY {self.valves.show_custom_key}"
                if custom_value is not None:
                    selected_data[custom_key_display] = custom_value  # Obfuscate will apply later in _format_json
                else:
                    selected_data[custom_key_display] = "**** CUSTOM KEY NOT FOUND ****"

            return selected_data

        # Select failed
        except Exception as e:

            # DEBUG ERROR
            if Config.DEBUG_ERROR:
                print(f"[DEBUG FILTER DATA] ERROR | Select data failed: {e}")

            return None


    async def inlet(
        self, # self
        body: dict, # A dict usually destined to go almost directly to the model. Although it is not strictly a special argument, it is included here for easier reference and because it contains itself some special arguments
        __user__: Optional[dict] = None, # A dict with user information
        __metadata__: Optional[dict] = None, # A dict with wide ranging information about the chat, model, files, etc...
        __model__: Optional[dict] = None, # A dict with information about the model
        __messages__: Optional[List] = None, # A list of the previous messages
        __chat_id__: Optional[str] = None, # The str of the chat_id
        __session_id__: Optional[str] = None, # The str of the session_id
        __message_id__: Optional[str] = None, # The str of the message_id
        __event_emitter__: Optional[Callable[[dict], Any]] = None, # A Callable used to display event information to the user
        __event_call__: Optional[Callable[[dict], Any]] = None, # A Callable used for Actions
        __files__: Optional[list] = None, # A list of files sent via the chat. Note that images are not considered files and are sent directly to the model as part of the body["messages"] list
        __request__: Optional[Any] = None, # An instance of fastapi.Request
        __task__: Optional[str] = None, # A str for the type of task. Its value is just a shorthand for __metadata__["task"] if present, otherwise None
        __task_body__: Optional[dict] = None, # A dict containing the body needed to accomplish a given __task__. Its value is just a shorthand for __metadata__["task_body"] if present, otherwise None
        __tools__: Optional[list] = None, # A list of ToolUserModel instances
        ) -> dict:

        """Intercept incoming requests"""

        # DEBUG INFO
        if Config.DEBUG_INFO:
            print(f"[DEBUG FILTER DATA] INFO | Inlet start (priority:{self.valves.priority})")

        # Inlet
        try:

            # Status start
            if __event_emitter__ and Config.STATUS_USE:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": Config.STATUS_INFO_START,
                            "done": False,
                            "hidden": False,
                        },
                    }
                )

            # Required data
            current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            user_id = __user__.get("id") if __user__ else "default"
            self.debug_inlet_temp[user_id] = None
            self.debug_stream_temp[user_id] = None

            # Clean chat history from last Debug Filter Data report
            if Config.MESSAGE_CLEAN_CHAT_HISTORY:
                if "messages" in body and body["messages"]:

                    # Report delimiters
                    begin_escaped = re.escape(Config.RESULT_KEYWORD_BEGIN)
                    end_escaped = re.escape(Config.RESULT_KEYWORD_END)
                    pattern = re.compile(f'{begin_escaped}.*?{end_escaped}', flags=re.DOTALL)
                    
                    for message_content in body["messages"]:
                        if "content" in message_content and isinstance(message_content["content"], str):
                            original_content = message_content["content"]
                            
                            # Clean report
                            cleaned_content = pattern.sub('', original_content)
                            
                            # Check for update
                            if cleaned_content != original_content:
                                message_content["content"] = cleaned_content
                                
                                # DEBUG INFO
                                if Config.DEBUG_INFO:
                                    print(f"[DEBUG FILTER DATA] INFO | Report CLEANED from INLET")

            # Log inlet
            if self.valves.log_inlet:

                # Status inlet start
                if __event_emitter__ and Config.STATUS_USE:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {
                                "description": Config.STATUS_INFO_INLET_START,
                                "done": False,
                                "hidden": False,
                            },
                        }
                    )

                # Init
                summary_info = {}

                # Summary
                if self.valves.show_summary:

                    # Generate summary data
                    summary_timestamp = current_timestamp
                    summary_model_id = __model__.get("id") if __model__ else "-"
                    summary_model_name = __model__.get("name") if __model__ else "UNKNOWN"
                    summary_user_id = __user__.get("id") if __user__ else "-"
                    summary_user_name = __user__.get("name") if __user__ else "UNKNOWN"
                    summary_messages_count = len(body.get("messages", []))
                    summary_body_keys_list = list((body or {}).keys())
                    summary_body_keys_txt = '' + ', '.join(summary_body_keys_list or []) + ''
                    summary_user_keys_list = list((__user__ or {}).keys())
                    summary_user_keys_txt = '' + ', '.join(summary_user_keys_list or []) + ''
                    summary_metadata_keys_list = list((__metadata__ or {}).keys())
                    summary_metadata_keys_txt = '' + ', '.join(summary_metadata_keys_list or []) + ''
                    summary_model_keys_list = list((__model__ or {}).keys())
                    summary_model_keys_txt = '' + ', '.join(summary_model_keys_list or []) + ''
                    summary_messages_keys_list = list((__messages__ or {}).keys())
                    summary_messages_keys_txt = '' + ', '.join(summary_messages_keys_list or []) + ''

                    # Summary final info
                    summary_info = {
                        "TYPE": f"INLET (Priority: {self.valves.priority}) [{summary_timestamp}]",
                        "MODEL": f"{summary_model_name} [{summary_model_id}]",
                        "USER": f"{summary_user_name} [{summary_user_id}]",
                        "MESSAGES COUNT": summary_messages_count,
                        "KEYS OF body": summary_body_keys_txt,
                        "KEYS OF __user__": summary_user_keys_txt,
                        "KEYS OF __metadata__": summary_metadata_keys_txt,
                        "KEYS OF __model__": summary_model_keys_txt,
                        "KEYS OF __messages__": summary_messages_keys_txt,
                    }

                # Debug data
                debug_data_dict = {
                    "summary": summary_info,
                    "body": body,
                    "__user__": __user__,
                    "__metadata__": __metadata__,
                    "__model__": __model__,
                    "__messages__": __messages__,
                    "__chat_id__": __chat_id__,
                    "__session_id__": __session_id__,
                    "__message_id__": __message_id__,
                    "__event_emitter__": __event_emitter__,
                    "__event_call__": __event_call__,
                    "__files__": __files__,
                    "__request__": __request__,
                    "__task__": __task__,
                    "__task_body__": __task_body__,
                    "__tools__": __tools__,
                }

                # Select required data
                debug_data = self._select(debug_data_dict)

                # Log inlet
                self._log(f"{Config.TITLE_INLET} [{current_timestamp}]", debug_data, indent=True, delimiters="all")

                # Add data to debug temp
                self.debug_inlet_temp[user_id] = {"inlet_data": debug_data, "inlet_timestamp": current_timestamp}

                # Status inlet OK
                if __event_emitter__ and Config.STATUS_USE:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {
                                "description": Config.STATUS_INFO_INLET_OK,
                                "done": False,
                                "hidden": False,
                            },
                        }
                    )

            # DEBUG INFO
            if Config.DEBUG_INFO:
                print(f"[DEBUG FILTER DATA] INFO | Inlet end")

        # Inlet processing failed
        except Exception as e:

            # DEBUG ERROR
            if Config.DEBUG_ERROR:
                print(f"[DEBUG FILTER DATA] ERROR | Inlet processing failed: {e}")

        return body


    async def outlet(
        self, # self
        body: dict, # A dict usually destined to go almost directly to the model. Although it is not strictly a special argument, it is included here for easier reference and because it contains itself some special arguments
        __user__: Optional[dict] = None, # A dict with user information
        __metadata__: Optional[dict] = None, # A dict with wide ranging information about the chat, model, files, etc...
        __model__: Optional[dict] = None, # A dict with information about the model
        __messages__: Optional[List] = None, # A list of the previous messages
        __chat_id__: Optional[str] = None, # The str of the chat_id
        __session_id__: Optional[str] = None, # The str of the session_id
        __message_id__: Optional[str] = None, # The str of the message_id
        __event_emitter__: Optional[Callable[[dict], Any]] = None, # A Callable used to display event information to the user
        __event_call__: Optional[Callable[[dict], Any]] = None, # A Callable used for Actions
        __files__: Optional[list] = None, # A list of files sent via the chat. Note that images are not considered files and are sent directly to the model as part of the body["messages"] list
        __request__: Optional[Any] = None, # An instance of fastapi.Request
        __task__: Optional[str] = None, # A str for the type of task. Its value is just a shorthand for __metadata__["task"] if present, otherwise None
        __task_body__: Optional[dict] = None, # A dict containing the body needed to accomplish a given __task__. Its value is just a shorthand for __metadata__["task_body"] if present, otherwise None
        __tools__: Optional[list] = None, # A list of ToolUserModel instances
        ) -> dict:

        """Intercept outgoing responses"""

        # DEBUG INFO
        if Config.DEBUG_INFO:
            print(f"[DEBUG FILTER DATA] INFO | Outlet start (priority:{self.valves.priority})")

        # Outlet
        try:

            # Data
            current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            user_id = __user__.get("id") if __user__ else "default"

            # Remove old reports
            if Config.MESSAGE_REMOVE_OLD_REPORT:
                if "messages" in body and body["messages"]:

                    # Report delimiters
                    begin_escaped = re.escape(Config.RESULT_KEYWORD_BEGIN)
                    end_escaped = re.escape(Config.RESULT_KEYWORD_END)
                    pattern = re.compile(f'{begin_escaped}.*?{end_escaped}', flags=re.DOTALL)
                    
                    for message_content in body["messages"]:
                        if "content" in message_content and isinstance(message_content["content"], str):
                            original_content = message_content["content"]
                            
                            # Clean report
                            cleaned_content = pattern.sub('', original_content)
                            
                            # Check for update
                            if cleaned_content != original_content:
                                message_content["content"] = cleaned_content
                                
                                # DEBUG INFO
                                if Config.DEBUG_INFO:
                                    print(f"[DEBUG FILTER DATA] INFO | Report CLEANED from OUTLET")

            # Get data inlet
            if self.valves.log_inlet:
                debug_inlet_temp = self.debug_inlet_temp.get(user_id)
                inlet_data = None if debug_inlet_temp is None else debug_inlet_temp.get("inlet_data")
                inlet_timestamp = None if debug_inlet_temp is None else debug_inlet_temp.get("inlet_timestamp")

            # Get data stream
            if self.valves.log_stream:
                debug_stream_temp = self.debug_stream_temp.get(user_id)
                stream_data = None if debug_stream_temp is None else debug_stream_temp.get("stream_data")

            # Reset
            self.debug_inlet_temp[user_id] = None
            self.debug_stream_temp[user_id] = None

            # Log outlet
            if self.valves.log_outlet:

                # Status outlet start
                if __event_emitter__ and Config.STATUS_USE:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {
                                "description": Config.STATUS_INFO_OUTLET_START,
                                "done": False,
                                "hidden": False,
                            },
                        }
                    )

                # Init
                summary_info = {}

                # Summary
                if self.valves.show_summary:

                    # Generate summary data
                    summary_timestamp = current_timestamp
                    summary_model_id = __model__.get("id") if __model__ else "-"
                    summary_model_name = __model__.get("name") if __model__ else "UNKNOWN"
                    summary_user_id = __user__.get("id") if __user__ else "-"
                    summary_user_name = __user__.get("name") if __user__ else "UNKNOWN"
                    summary_messages_count = len(body.get("messages", []))
                    summary_body_keys_list = list((body or {}).keys())
                    summary_body_keys_txt = '' + ', '.join(summary_body_keys_list or []) + ''
                    summary_user_keys_list = list((__user__ or {}).keys())
                    summary_user_keys_txt = '' + ', '.join(summary_user_keys_list or []) + ''
                    summary_metadata_keys_list = list((__metadata__ or {}).keys())
                    summary_metadata_keys_txt = '' + ', '.join(summary_metadata_keys_list or []) + ''
                    summary_model_keys_list = list((__model__ or {}).keys())
                    summary_model_keys_txt = '' + ', '.join(summary_model_keys_list or []) + ''
                    summary_messages_keys_list = list((__messages__ or {}).keys())
                    summary_messages_keys_txt = '' + ', '.join(summary_messages_keys_list or []) + ''

                    # Summary final info
                    summary_info = {
                        "TYPE": f"OUTLET (Priority: {self.valves.priority}) [{summary_timestamp}]",
                        "MODEL": f"{summary_model_name} [{summary_model_id}]",
                        "USER": f"{summary_user_name} [{summary_user_id}]",
                        "MESSAGES COUNT": summary_messages_count,
                        "KEYS OF body": summary_body_keys_txt,
                        "KEYS OF __user__": summary_user_keys_txt,
                        "KEYS OF __metadata__": summary_metadata_keys_txt,
                        "KEYS OF __model__": summary_model_keys_txt,
                        "KEYS OF __messages__": summary_messages_keys_txt,
                    }

                # Debug data
                debug_data_dict = {
                    "summary": summary_info,
                    "body": body,
                    "__user__": __user__,
                    "__metadata__": __metadata__,
                    "__model__": __model__,
                    "__messages__": __messages__,
                    "__chat_id__": __chat_id__,
                    "__session_id__": __session_id__,
                    "__message_id__": __message_id__,
                    "__event_emitter__": __event_emitter__,
                    "__event_call__": __event_call__,
                    "__files__": __files__,
                    "__request__": __request__,
                    "__task__": __task__,
                    "__task_body__": __task_body__,
                    "__tools__": __tools__,
                }

                # Select required data
                debug_data = self._select(debug_data_dict)

                # Log outlet
                self._log(f"{Config.TITLE_OUTLET} [{current_timestamp}]", debug_data, indent=True, delimiters="all")

                # Status outlet OK
                if __event_emitter__ and Config.STATUS_USE:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {
                                "description": Config.STATUS_INFO_OUTLET_OK,
                                "done": False,
                                "hidden": False,
                            },
                        }
                    )

            # Send to chat
            if self.valves.send_to_chat:
                if "messages" in body and body["messages"]:
                    last_message = body["messages"][-1]
                    if last_message.get("role") == "assistant":

                        # Data
                        original_content = last_message.get("content", "")
                        model_name = __model__.get("name") if __model__ else "UNKNOWN"
                        message_number = len(body["messages"])
                        content_header = ""
                        content_inlet = ""
                        content_outlet = ""
                        content_stream = ""
                        content_footer = ""
                        content_inlet_len = 0
                        content_outlet_len = 0
                        content_stream_len = 0

                        # Interaction
                        interaction_displayed = []
                        if self.valves.log_inlet:
                            interaction_displayed.append("INLET")
                        if self.valves.log_outlet:
                            interaction_displayed.append("OUTLET")
                        if self.valves.log_stream:
                            interaction_displayed.append("STREAM")

                        if len(interaction_displayed) > 0:
                            interaction_displayed_txt = '' + ' | '.join(interaction_displayed or [])
                        else:
                            interaction_displayed_txt = "⚠️ No interaction selected. **You must select at least one interaction in Valves** (inlet|outlet|stream)"

                            # DEBUG WARNING
                            if Config.DEBUG_WARNING:
                                print(f"[DEBUG FILTER DATA] WARNING | No interaction selected in Valves options")

                        # Data 
                        data_displayed = []
                        if self.valves.show_summary:
                            data_displayed.append("summary")
                        if self.valves.show_body:
                            data_displayed.append("body")
                        if self.valves.show_user:
                            data_displayed.append("__user__")
                        if self.valves.show_metadata:
                            data_displayed.append("__metadata__")
                        if self.valves.show_model:
                            data_displayed.append("__model__")
                        if self.valves.show_messages:
                            data_displayed.append("__messages__")
                        if self.valves.show_chat_id:
                            data_displayed.append("__chat_id__")
                        if self.valves.show_session_id:
                            data_displayed.append("__session_id__")
                        if self.valves.show_message_id:
                            data_displayed.append("__message_id__")
                        if self.valves.show_event_emitter:
                            data_displayed.append("__event_emitter__")
                        if self.valves.show_event_call:
                            data_displayed.append("__event_call__")
                        if self.valves.show_files:
                            data_displayed.append("__files__")
                        if self.valves.show_request:
                            data_displayed.append("__request__")
                        if self.valves.show_task:
                            data_displayed.append("__task__")
                        if self.valves.show_task_body:
                            data_displayed.append("__task_body__")
                        if self.valves.show_tools:
                            data_displayed.append("__tools__")

                        # Sent to 
                        sent_to = []
                        if self.valves.send_to_chat:
                            sent_to.append("CHAT")
                        if self.valves.send_to_console:
                            sent_to.append("CONSOLE")
                        if self.valves.send_to_file:
                            sent_to.append("FILE")

                        if len(sent_to) > 0:
                            sent_to_txt = '' + ' | '.join(sent_to or [])
                        else:
                            sent_to_txt = "⚠️ No output selected. **You must select at least one output in Valves** (chat|console|file)"

                            # DEBUG WARNING
                            if Config.DEBUG_WARNING:
                                print(f"[DEBUG FILTER DATA] WARNING | No output selected in Valves options")


                        # Inlet or Outlet
                        if self.valves.log_inlet or self.valves.log_outlet:

                            if len(data_displayed) > 0:
                                data_displayed_txt = '' + ' | '.join(data_displayed or [])
                            else:
                                data_displayed_txt = "⚠️ No data selected. **You must select at least one data in Valves** (e.g.: summary, body, user, ...)"

                                # DEBUG WARNING
                                if Config.DEBUG_WARNING:
                                    print(f"[DEBUG FILTER DATA] WARNING | No data selected in Valves options")

                        # No Inlet and no Outlet
                        else:
                            if self.valves.log_stream:
                                data_displayed_txt = "Stream info only"
                            else:
                                data_displayed_txt = "-"

                        # Stream item nb
                        if self.valves.log_stream:
                            if stream_data is None:
                                stream_item_nb = 0
                            else:
                                stream_item_nb = len(stream_data)
                            if stream_item_nb > 1:
                                stream_item_nb_txt = f"{stream_item_nb} items"
                            else:
                                stream_item_nb_txt = f"{stream_item_nb} item"

                        # Content begin
                        if Config.MESSAGE_CLEAN_CHAT_HISTORY and Config.RESULT_KEYWORD_BEGIN:
                            content_begin = f"\n<br/><br/>{Config.RESULT_KEYWORD_BEGIN}"
                        else:
                            content_begin = f"\n{'_'*80}\n"

                        # Content header
                        if Config.RESULT_HEADER:
                            content_header = (
                                f"## {Config.TITLE_DEBUG}\n"
                                f"- Model: {model_name}\n"
                                f"- Interaction: {interaction_displayed_txt}\n"
                                f"- Data: {data_displayed_txt}\n"
                                f"- Sent to: {sent_to_txt}\n"
                            )

                        # Content inlet
                        if self.valves.log_inlet:
                            inlet_data_formatted = self._format_json(inlet_data)
                            content_inlet_len = self._get_json_size(inlet_data_formatted)
                            content_inlet = (
                                f"#### {Config.TITLE_INLET} [{inlet_timestamp}] Size: {self._format_size(content_inlet_len)}\n"
                                f"```json\n"
                                f"{inlet_data_formatted}\n"
                                f"```\n"
                                f"\n"
                            )

                        # Content outlet
                        if self.valves.log_outlet:
                            debug_data_formatted = self._format_json(debug_data)
                            content_outlet_len = self._get_json_size(debug_data_formatted)
                            content_outlet = (
                                f"#### {Config.TITLE_OUTLET} [{current_timestamp}] Size: {self._format_size(content_outlet_len)}\n"
                                f"```json\n"
                                f"{debug_data_formatted}\n"
                                f"```\n"
                                f"\n"
                            )

                        # Content stream
                        if self.valves.log_stream:
                            stream_data_formatted = self._format_json(stream_data)
                            content_stream_len = self._get_json_size(stream_data_formatted)
                            content_stream = (
                                f"#### {Config.TITLE_STREAM} [{stream_item_nb_txt}] Size: {self._format_size(content_stream_len)}\n"
                                f"```json\n"
                                f"{stream_data_formatted}\n"
                                f"```\n"
                                f"\n"
                            )

                        # Content footer
                        if Config.RESULT_FOOTER:
                            content_len = content_inlet_len + content_outlet_len + content_stream_len
                            content_footer = (
                                f"DEBUG FILTER DATA status OK\n"
                                f"- Report total size: {self._format_size(content_len)}\n"
                                f"- Message number: {message_number}\n"
                            )

                        # Content end
                        if Config.MESSAGE_CLEAN_CHAT_HISTORY and Config.RESULT_KEYWORD_END:
                            content_end = f"\n{Config.RESULT_KEYWORD_END}"
                        else:
                            content_end = f"\n{'_'*80}\n"

                        # Update content
                        debug_content = (
                            f"{content_begin}\n"
                            f"{content_header}\n"
                            f"{content_inlet}\n"
                            f"{content_outlet}\n"
                            f"{content_stream}\n"
                            f"{content_footer}\n"
                            f"{content_end}\n"
                        )

                        # Update content
                        last_message["content"] = (
                            f"{original_content}\n"
                            f"{debug_content}\n"
                        )

        # Outlet processing failed
        except Exception as e:

            # DEBUG ERROR
            if Config.DEBUG_ERROR:
                print(f"[DEBUG FILTER DATA] ERROR | Outlet processing failed: {e}")

        # Status completed
        try:
            if __event_emitter__ and Config.STATUS_USE:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": Config.STATUS_INFO_COMPLETED,
                            "done": True,
                        },
                    }
                )

        # Status warning
        except Exception as e:

            # DEBUG WARNING
            if Config.DEBUG_WARNING:
                print(f"[DEBUG FILTER DATA] WARNING | Status emitter failed: {e}")

        # DEBUG INFO
        if Config.DEBUG_INFO:
            print(f"[DEBUG FILTER DATA] INFO | Outlet end")

        return body


    async def stream(
        self,
        event: Optional[dict] = None, # A dict of the token stream
        __user__: Optional[dict] = None, # A dict with user information
        __event_emitter__: Optional[Callable[[dict], Any]] = None, # A Callable used to display event information to the user
        ) -> dict:
        """Intercept stream responses"""

        # No event data
        if event is None:
            return event

        # Stream
        try:

            # Log stream
            if self.valves.log_stream:

                # Data
                current_timestamp = datetime.now()#.strftime('%Y-%m-%d %H:%M:%S')
                user_id = __user__.get("id") if __user__ else "default"

                debug_stream_temp = self.debug_stream_temp.get(user_id)
                stream_data = None if debug_stream_temp is None else debug_stream_temp.get("stream_data")

                # First stream data
                if stream_data is None:

                    # DEBUG INFO
                    if Config.DEBUG_INFO:
                        print(f"[DEBUG FILTER DATA] INFO | Stream start (priority:{self.valves.priority})")

                    # Start of log
                    self._log(message=f"{Config.TITLE_STREAM} [{current_timestamp}]", data=None, indent=False, delimiters="top")
                    
                    self.debug_stream_temp[user_id] = {"stream_data": [event]}

                    # Status stream start
                    if __event_emitter__ and Config.STATUS_USE:
                        await __event_emitter__(
                            {
                                "type": "status",
                                "data": {
                                    "description": Config.STATUS_INFO_STREAM_START,
                                    "done": False,
                                    "hidden": False,
                                },
                            }
                        )

                # Update stream data
                else:
                    stream_data.append(event)
                    self.debug_stream_temp[user_id] = {"stream_data": stream_data}

                # Log stream
                self._log(message=f"[DEBUG FILTER DATA] STREAM | {current_timestamp}", data=event, indent=True, delimiters=None)

                # Check stream stop
                try:
                    stream_stop = event.get("choices", [{}])[0].get("finish_reason") == "stop"
                except Exception as e:

                    # DEBUG ERROR
                    if Config.DEBUG_ERROR:
                        print(f"[DEBUG FILTER DATA] ERROR | Error checking stream stop: {e}")

                # Stream stop
                if stream_stop:

                    # End of log
                    self._log(message=None, data=None, indent=False, delimiters="bottom")

                    # Status stream OK
                    if __event_emitter__ and Config.STATUS_USE:
                        await __event_emitter__(
                            {
                                "type": "status",
                                "data": {
                                    "description": Config.STATUS_INFO_STREAM_OK,
                                    "done": False,
                                    "hidden": False,
                                },
                            }
                        )

                    # DEBUG INFO
                    if Config.DEBUG_INFO:
                        print(f"[DEBUG FILTER DATA] INFO | Stream end")

            # No log stream
            if not self.valves.log_stream:

                # Get user id
                user_id = __user__.get("id") if __user__ else "default"

                # Check temp
                if not user_id in self.debug_stream_temp or self.debug_stream_temp[user_id] is None:

                    # Status stream OK
                    if __event_emitter__ and Config.STATUS_USE:
                        await __event_emitter__(
                            {
                                "type": "status",
                                "data": {
                                    "description": "🗐 Debug Filter Data - Wait while streaming...",
                                    "done": False,
                                    "hidden": False,
                                },
                            }
                        )

                    # Update temp
                    self.debug_stream_temp[user_id] = True

        # Stream processing failed
        except Exception as e:

            # Cleanup in case of exceptions
            del self.debug_stream_temp[user_id]

            # DEBUG ERROR
            if Config.DEBUG_ERROR:
                print(f"[DEBUG FILTER DATA] ERROR | Stream processing failed: {e}")

        return event

