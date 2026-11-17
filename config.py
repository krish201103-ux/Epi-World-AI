"""
config.py -- Centralized configuration for Epiworld.

Addresses mentor review Comment 9 (Configuration Management): values that
were previously hardcoded inside server.py (host, port, and the Groq API
key) now live here and are read from environment variables, with safe
defaults for local development.

Setup:
  1. Copy .env.example to .env
  2. Put your real Groq API key in .env
  3. .env is in .gitignore -- it will never be committed

server.py reads everything through this module; nothing downstream should
read os.environ directly.

NOTE: this reads .env with a small built-in parser (_load_env_file below)
instead of the third-party python-dotenv package. That's a deliberate choice,
not a simplification for its own sake -- some environments (locked-down
Windows machines with an Application Control policy, for example) block
`pip install` entirely, so any dependency beyond what already runs the app
successfully is a real risk of breaking the whole project on that machine.
This file now needs nothing that isn't already required by server.py itself.
"""
import os
from pathlib import Path


def _read_env_text(path):
    """Read a .env file's text content, tolerant of the encodings Windows tools
       commonly produce -- this is not a hypothetical concern: PowerShell's `>`
       redirect (an alias for Out-File) defaults to UTF-16LE with a byte-order
       mark, and Notepad's "UTF-8" save option adds a UTF-8 BOM. A strict
       encoding='utf-8' read can silently fail to find any KEY=VALUE lines in
       either case -- not by raising an error, but by producing mangled text
       that never matches the parsing logic below, which looks like "the key
       just isn't loading" with no obvious cause. Tries UTF-8 (with or without
       BOM) first since that's the recommended/common case, then falls back to
       UTF-16 variants before giving up."""
    raw = path.read_bytes()
    for encoding in ('utf-8-sig', 'utf-8', 'utf-16', 'utf-16-le', 'utf-16-be'):
        try:
            return raw.decode(encoding)
        except (UnicodeDecodeError, UnicodeError):
            continue
    # Last resort: decode UTF-8 anyway, replacing anything that doesn't fit --
    # better to load the lines that DO parse than to silently load nothing.
    return raw.decode('utf-8', errors='replace')


def _load_env_file(path):
    """Minimal stand-in for python-dotenv's load_dotenv(): reads KEY=VALUE
       lines from a .env file into os.environ, without adding a dependency.
       Skips blank lines and lines starting with #. Strips one layer of
       matching quotes around the value, same as python-dotenv does. Never
       overwrites a variable that's already set in the real environment
       (e.g. one set by the OS or a hosting platform) -- .env is only a
       local-development fallback."""
    if not path.exists():
        return
    for line in _read_env_text(path).splitlines():
        line = line.strip().lstrip('\ufeff')  # strip a leading BOM if one slipped through as a character
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, _, value = line.partition('=')
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        if key:
            os.environ.setdefault(key, value)


_load_env_file(Path(__file__).parent / '.env')


def _get_bool(name: str, default: bool) -> bool:
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


# -- Flask server -----------------------------------------------------
HOST = os.environ.get("EPIWORLD_HOST", "127.0.0.1")
PORT = int(os.environ.get("EPIWORLD_PORT", "5000"))
DEBUG = _get_bool("EPIWORLD_DEBUG", False)

# -- Forecasting defaults ----------------------------------------------
DEFAULT_HORIZON = int(os.environ.get("EPIWORLD_DEFAULT_HORIZON", "5"))
MAX_HORIZON = int(os.environ.get("EPIWORLD_MAX_HORIZON", "20"))

# -- EpiGem AI chatbot (Groq) -------------------------------------------
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_URL = os.environ.get("GROQ_URL", "https://api.groq.com/openai/v1/chat/completions")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")

GROQ_ENABLED = bool(GROQ_API_KEY)
if not GROQ_ENABLED:
    # Do not crash the whole app if the key is missing -- the dashboard,
    # forecasting, and every other feature work fine without EpiGem.
    # server.py checks GROQ_ENABLED before calling the chatbot endpoints
    # and returns a clear "chatbot not configured" message instead.
    print(
        "[config] WARNING: GROQ_API_KEY is not set. EpiGem AI chat will be "
        "disabled until it is configured in your .env file. All other "
        "features (forecasting, dashboard, upload) are unaffected."
    )
