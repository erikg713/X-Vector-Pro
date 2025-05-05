class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, user_id):
        session_id = generate_session_id()
        self.sessions[session_id] = user_id
        return session_id

    def validate_session(self, session_id):
        return session_id in self.sessions

    def end_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]
