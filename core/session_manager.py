import threading
import uuid
from typing import Dict, Optional
import os
class SessionManager:
    """
    Manages user sessions using a thread-safe approach.
    - Supports session creation, validation, and termination.
    """

    def __init__(self):
        """
        Initializes a thread-safe session manager.
        """
        self.sessions: Dict[str, str] = {}
        self.lock = threading.Lock()  # Ensures thread-safe operations.

    def create_session(self, user_id: str) -> str:
        """
        Creates a new session for the given user ID.

        Args:
            user_id (str): The ID of the user for whom the session is created.

        Returns:
            str: A unique session ID for the user.
        """
        session_id = str(uuid.uuid4())  # Generates a secure, unique session ID.

        with self.lock:  # Ensures thread-safe write operation.
            self.sessions[session_id] = user_id

        return session_id

    def validate_session(self, session_id: str) -> bool:
        """
        Validates if a session ID exists.

        Args:
            session_id (str): The session ID to validate.

        Returns:
            bool: True if the session ID is valid, False otherwise.
        """
        with self.lock:  # Ensures thread-safe read operation.
            return session_id in self.sessions

    def get_user_from_session(self, session_id: str) -> Optional[str]:
        """
        Retrieves the user ID associated with a session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            Optional[str]: The user ID if the session exists, None otherwise.
        """
        with self.lock:
            return self.sessions.get(session_id)

    def end_session(self, session_id: str) -> bool:
        """
        Terminates a session by its session ID.

        Args:
            session_id (str): The session ID to end.

        Returns:
            bool: True if the session was successfully ended, False if it didn't exist.
        """
        with self.lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
                return True
            return False

    def clear_all_sessions(self):
        """
        Clears all active sessions.
        """
        with self.lock:
            self.sessions.clear()
