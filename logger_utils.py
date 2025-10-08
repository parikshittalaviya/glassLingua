# logger_utils.py
import sys
import os

def suppress_pygame_logs():
    """Suppresses pygame's default stdout/stderr logging."""
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")

def restore_logs():
    """Restores stdout and stderr after suppressing logs."""
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


# # Save original stdout and stderr so we can restore them later
# _original_stdout = sys.stdout
# _original_stderr = sys.stderr

# def suppress_pygame_logs():
#     """
#     Suppresses unnecessary logs by redirecting stdout and stderr to os.devnull.
#     This is useful when Pygame (or other libraries) produce a lot of console output.
#     """
#     sys.stdout = open(os.devnull, 'w')
#     sys.stderr = open(os.devnull, 'w')
#     # Optionally, you can also adjust pygame's internal logger if needed.
#     # For example, if using the logging module:
#     # import logging
#     # logging.getLogger('pygame').setLevel(logging.WARNING)

# def restore_logs():
#     """
#     Restores the original stdout and stderr.
#     """
#     # Close the devnull streams to free resources
#     if sys.stdout and sys.stdout is not _original_stdout:
#         sys.stdout.close()
#     if sys.stderr and sys.stderr is not _original_stderr:
#         sys.stderr.close()
#     sys.stdout = _original_stdout
#     sys.stderr = _original_stderr
