from pyarcade.session_manager import SessionManager, CheckerSession, MastermindSession
from pyarcade.checkers_board import CheckerBoard
import unittest
import sys


class SessionManagerInitSessionTestCase(unittest.TestCase):
    def setUp(self):
        SessionManager.active_sessions = {}

    def test_init_checkers_session_gives_unique_id(self):
        sessions = []
        session_manager = SessionManager()

        for idx in range(100):
            sessions.append(session_manager.init_checkers_session(CheckerBoard())["session_id"])

        self.assertTrue(len(set(sessions)) == 100)

    def test_init_mastermind_session_gives_unique_id(self):
        sessions = []
        session_manager = SessionManager()

        for idx in range(100):
            sessions.append(session_manager.init_mastermind_session([])["session_id"])

        self.assertTrue(len(set(sessions)) == 100)

    def test_init_mastermind_checkers_sessions_gives_unique_id(self):
        sessions = []
        session_manager = SessionManager()

        for idx in range(100):
            sessions.append(session_manager.init_mastermind_session([])["session_id"])
            sessions.append(session_manager.init_checkers_session(CheckerBoard())["session_id"])

        # Each game session instance has it's own set of sessions
        self.assertEqual(len(set(sessions)), 200)


class SessionManagerSessionExistsTestCase(unittest.TestCase):
    def test_checkers_session_exists_after_init(self):
        sessions = []
        session_manager = SessionManager()

        for idx in range(100):
            sessions.append(session_manager.init_checkers_session(CheckerBoard())["session_id"])

        for idx in range(100):
            self.assertTrue(session_manager.session_exists(sessions[idx]))

    def test_mastermind_session_exists_after_init(self):
        sessions = []
        session_manager = SessionManager()

        for idx in range(100):
            sessions.append(session_manager.init_mastermind_session([])["session_id"])

        for idx in range(100):
            self.assertTrue(session_manager.session_exists(sessions[idx]))

    def test_checkers_session_does_not_exist_after_delete(self):
        sessions = []
        session_manager = SessionManager()

        for idx in range(100):
            sessions.append(session_manager.init_checkers_session(CheckerBoard())["session_id"])

        for idx in range(100):
            session_manager.delete_session(sessions[idx])

        for idx in range(100):
            self.assertFalse(session_manager.session_exists(sessions[idx]))

    def test_mastermind_session_does_not_exist_after_delete(self):
        sessions = []
        session_manager = SessionManager()

        for idx in range(100):
            sessions.append(session_manager.init_mastermind_session([])["session_id"])

        for idx in range(100):
            session_manager.delete_session(sessions[idx])

        for idx in range(100):
            self.assertFalse(session_manager.session_exists(sessions[idx]))


class SessionManagerDeleteSessionTestCase(unittest.TestCase):
    def test_delete_checkers_session_removes_from_active(self):
        sessions = []
        session_manager = SessionManager()

        for idx in range(100):
            sessions.append(session_manager.init_checkers_session(CheckerBoard())["session_id"])

        for idx in range(100):
            session_manager.delete_session(sessions[idx])

        for idx in range(100):
            self.assertFalse(session_manager.session_exists(sessions[idx]))

    def test_delete_mastermind_session_removes_from_active(self):
        sessions = []
        session_manager = SessionManager()

        for idx in range(100):
            sessions.append(session_manager.init_mastermind_session([])["session_id"])

        for idx in range(100):
            session_manager.delete_session(sessions[idx])

        for idx in range(100):
            self.assertFalse(session_manager.session_exists(sessions[idx]))

    def test_delete_mastermind_and_checkers_sessions_removes_from_active(self):
        sessions = []
        session_manager = SessionManager()

        for idx in range(100):
            sessions.append(session_manager.init_mastermind_session([])["session_id"])
            sessions.append(session_manager.init_checkers_session(CheckerBoard())["session_id"])

        for idx in range(200):
            session_manager.delete_session(sessions[idx])

        for idx in range(200):
            self.assertFalse(session_manager.session_exists(sessions[idx]))

    def test_delete_checkers_session_returns_correct_id(self):
        sessions = []
        session_manager = SessionManager()

        for idx in range(100):
            sessions.append(session_manager.init_checkers_session(CheckerBoard())["session_id"])

        for idx in range(100):
            reply = session_manager.delete_session(sessions[idx])
            self.assertEqual(reply["session_id"], sessions[idx])

    def test_delete_mastermind_session_returns_correct_id(self):
        sessions = []
        session_manager = SessionManager()

        for idx in range(100):
            sessions.append(session_manager.init_mastermind_session([])["session_id"])

        for idx in range(100):
            reply = session_manager.delete_session(sessions[idx])
            self.assertEqual(reply["session_id"], sessions[idx])


class SessionManagerInsertActiveSessionTestCase(unittest.TestCase):
    def test_insert_session_is_in_active_sessions(self):
        sessions = []
        session_manager = SessionManager()

        for idx in range(100):
            sessions.append(session_manager.insert_active_session(CheckerSession(CheckerBoard()))["session_id"])
            sessions.append(session_manager.insert_active_session(MastermindSession([]))["session_id"])

        for idx in range(200):
            self.assertTrue(sessions[idx] in session_manager.active_sessions)


class SessionManagerGetSessionByIDTestCase(unittest.TestCase):
    def test_get_session_by_id(self):
        session_manager = SessionManager()

        checkers_session = CheckerSession(CheckerBoard())
        mastermind_session = MastermindSession([])

        check_id = session_manager.insert_active_session(checkers_session)["session_id"]
        mast_id = session_manager.insert_active_session(mastermind_session)["session_id"]

        self.assertEqual(session_manager.get_session_by_id(check_id), checkers_session)
        self.assertEqual(session_manager.get_session_by_id(mast_id), mastermind_session)


class SessionManagerIsCheckersSessionTestCase(unittest.TestCase):
    def test_is_checkers_session_is_true_for_checkers_id(self):
        session_manager = SessionManager()
        sesh_id = session_manager.init_checkers_session(CheckerBoard())["session_id"]
        self.assertTrue(session_manager.is_checkers_session(sesh_id))

    def test_is_checkers_session_is_false_for_mastermind_id(self):
        session_manager = SessionManager()
        sesh_id = session_manager.init_mastermind_session([])["session_id"]
        self.assertFalse(session_manager.is_checkers_session(sesh_id))


class SessionManagerIsMastermindSessionTestCase(unittest.TestCase):
    def test_is_mastermind_session_is_true_for_mastermind_id(self):
        session_manager = SessionManager()
        sesh_id = session_manager.init_mastermind_session([])["session_id"]
        self.assertTrue(session_manager.is_mastermind_session(sesh_id))

    def test_is_checkers_session_is_false_for_mastermind_id(self):
        session_manager = SessionManager()
        sesh_id = session_manager.init_checkers_session(CheckerBoard())["session_id"]
        self.assertFalse(session_manager.is_mastermind_session(sesh_id))


class SessionManagerSessionIsDoneTestCase(unittest.TestCase):
    def test_session_is_done_returns_true_when_done(self):
        session_manager = SessionManager()
        sesh_id = session_manager.init_checkers_session(CheckerBoard())["session_id"]
        session_manager.active_sessions[sesh_id].done = True
        self.assertTrue(session_manager.session_is_done(sesh_id))

    def test_session_id_done_returns_false_when_not_done(self):
        session_manager = SessionManager()
        sesh_id = session_manager.init_checkers_session(CheckerBoard())["session_id"]
        session_manager.active_sessions[sesh_id].done = False
        self.assertFalse(session_manager.session_is_done(sesh_id))
