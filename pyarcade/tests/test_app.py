import json
from itertools import count
from unittest import TestCase
from pyarcade.app import create_app
from pyarcade.game_ids import *
from pyarcade.session_manager import SessionManager, Session, CheckerSession, MastermindSession, MinesweeperSession


class ApplicationHomeTestCase(TestCase):
    def test_get_active_sessions_empty(self):
        flask_app = create_app()
        client = flask_app.test_client()

        response = client.get("/")

        self.assertTrue(response is not None)
        self.assertTrue("menu" in response.json)


class ApplicationMastermindTestCase(TestCase):
    def test_get_mastermind_null_session(self):
        flask_app = create_app()
        client = flask_app.test_client()

        response = client.get("/game/mastermind", json={"session_id": MASTERMIND_ID})

        self.assertTrue(response is not None)

    def test_create_mastermind_null_session(self):
        flask_app = create_app()
        client = flask_app.test_client()

        response = client.post("/create/mastermind", json={"game_id": MASTERMIND_ID})

        self.assertTrue(response is not None)

    def test_update_mastermind_null_session(self):
        flask_app = create_app()
        client = flask_app.test_client()

        response = client.put("/update/mastermind", json={"session_id": 0})

        self.assertTrue(response is not None)

    def test_delete_mastermind_null_session(self):
        flask_app = create_app()
        client = flask_app.test_client()

        response = client.delete("/delete/mastermind", json={"session_id": 0})

        self.assertTrue(response is not None)


class ApplicationMastermindActiveSessionTestCase(TestCase):
    def setUp(self):
        self.session_manager = SessionManager()
        SessionManager.active_sessions = {}
        Session._session_id = count(1)

    def test_create_active_mastermind_sessions(self):
        flask_app = create_app()
        client = flask_app.test_client()

        for idx in range(100):
            reply = client.post("/create/mastermind", json={"game_id": MASTERMIND_ID})
            self.assertTrue(reply is not None)

        self.assertEqual(100, len(self.session_manager.get_sessions_by_type(MastermindSession)))

    def test_read_mastermind_returns_read_active_session(self):
        flask_app = create_app()
        client = flask_app.test_client()

        session_id = client.post("/create/mastermind", json={"game_id": MASTERMIND_ID}).json["session_id"]
        response = client.get("/play/mastermind", json={"session_id": session_id})

        self.assertTrue(response is not None)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json['session_id'], session_id)

    def test_update_mastermind_active_session(self):
        flask_app = create_app()
        client = flask_app.test_client()

        session_id = client.post("/create/mastermind", json={"game_id": MASTERMIND_ID}).json["session_id"]
        response = client.post("/update/mastermind", json={"session_id": session_id, "guess": (3, 4, 2, 1)})

        self.assertTrue(response is not None)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json['session_id'], session_id)

    def test_delete_mastermind_active_session(self):
        flask_app = create_app()
        client = flask_app.test_client()

        session_id = client.post("/create/mastermind", json={"game_id": MASTERMIND_ID}).json["session_id"]
        response = client.post("/delete/mastermind", json={"session_id": session_id})

        self.assertTrue(response is not None)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json['session_id'], session_id)


class ApplicationCheckersNullSessionTestCase(TestCase):
    def setUp(self):
        self.session_manager = SessionManager()
        SessionManager.active_sessions = {}
        Session._session_id = count(1)

    def test_get_checkers_no_sessions(self):
        flask_app = create_app()
        client = flask_app.test_client()

        response = client.get("/game/checkers", json={"game_id": CHECKERS_ID})

        self.assertTrue(response is not None)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.json["active_sessions"]))

    def test_create_checkers_wrong_game_id(self):
        flask_app = create_app()
        client = flask_app.test_client()

        response = client.post("/create/checkers", json={"game_id": -99})

        self.assertTrue(response is not None)
        self.assertEqual(0, response.json["session_id"])

    def test_update_checkers_no_sessions(self):
        flask_app = create_app()
        client = flask_app.test_client()

        response = client.post("/update/checkers", json={"session_id": -99})

        self.assertTrue(response is not None)
        self.assertEqual(0, response.json["session_id"])

    def test_delete_checkers_no_sessions(self):
        flask_app = create_app()
        client = flask_app.test_client()

        response = client.post("/delete/checkers", json={"session_id": -99})

        self.assertTrue(response is not None)
        self.assertEqual(0, response.json["session_id"])


class ApplicationCheckersActiveSessionTestCase(TestCase):
    def setUp(self):
        self.session_manager = SessionManager()
        SessionManager.active_sessions = {}
        Session._session_id = count(1)

    def test_create_active_checker_sessions(self):
        flask_app = create_app()
        client = flask_app.test_client()

        for idx in range(100):
            reply = client.post("/create/checkers", json={"game_id": CHECKERS_ID})
            self.assertTrue(reply is not None)

        self.assertEqual(100, len(self.session_manager.get_sessions_by_type(CheckerSession)))

    def test_read_checkers_returns_read_active_session(self):
        flask_app = create_app()
        client = flask_app.test_client()

        session_id = client.post("/create/checkers", json={"game_id": CHECKERS_ID}).json["session_id"]
        response = client.get("/play/checkers", json={"session_id": session_id})

        self.assertTrue(response is not None)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json['session_id'], session_id)

    def test_update_checkers_active_session(self):
        flask_app = create_app()
        client = flask_app.test_client()

        session_id = client.post("/create/checkers", json={"game_id": CHECKERS_ID}).json["session_id"]
        response = client.post("/update/checkers", json={"session_id": session_id, "move": ((3, 4), (4, 5))})

        self.assertTrue(response is not None)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json['session_id'], session_id)

    def test_delete_checkers_active_session(self):
        flask_app = create_app()
        client = flask_app.test_client()

        session_id = client.post("/create/checkers", json={"game_id": CHECKERS_ID}).json["session_id"]
        response = client.post("/delete/checkers", json={"session_id": session_id})

        self.assertTrue(response is not None)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json['session_id'], session_id)


class ApplicationMinesweeperActiveSessionTestCase(TestCase):
    def setUp(self):
        self.session_manager = SessionManager()
        SessionManager.active_sessions = {}
        Session._session_id = count(1)

    def test_create_active_minesweeper_sessions(self):
        flask_app = create_app()
        client = flask_app.test_client()

        for idx in range(100):
            reply = client.post("/create/minesweeper", json={"game_id": MINESWEEPER_ID})
            self.assertTrue(reply is not None)

        self.assertEqual(100, len(self.session_manager.get_sessions_by_type(MinesweeperSession)))

    def test_read_minesweeper_returns_read_active_session(self):
        flask_app = create_app()
        client = flask_app.test_client()

        session_id = client.post("/create/minesweeper", json={"game_id": MINESWEEPER_ID}).json["session_id"]
        response = client.get("/play/minesweeper", json={"session_id": session_id})

        self.assertTrue(response is not None)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json['session_id'], session_id)

    def test_update_minesweeper_active_session(self):
        flask_app = create_app()
        client = flask_app.test_client()

        session_id = client.post("/create/minesweeper", json={"game_id": MINESWEEPER_ID}).json["session_id"]
        response = client.post("/update/minesweeper", json={"session_id": session_id, "flag_cell": (1, 1)})

        self.assertTrue(response is not None)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json['session_id'], session_id)

    def test_delete_minesweeper_active_session(self):
        flask_app = create_app()
        client = flask_app.test_client()

        session_id = client.post("/create/minesweeper", json={"game_id": MINESWEEPER_ID}).json["session_id"]
        response = client.post("/delete/minesweeper", json={"session_id": session_id})

        self.assertTrue(response is not None)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json['session_id'], session_id)


class ApplicationUserMenuInteractionsTestCase(TestCase):
    def test_main_menu_delete_create_read_update_home(self):
        flask_app = create_app()
        client = flask_app.test_client()

        main_menu = client.get("/").json["menu"]

        reply = client.get(main_menu["mastermind"])
        menu = reply.json["menu"]

        reply = client.post(menu["create"], json={"game_id": MASTERMIND_ID})
        session_id = reply.json["session_id"]
        self.assertTrue(reply is not None)
        self.assertEqual(200, reply.status_code)

        reply = client.get(menu["play"], json={"session_id": session_id})
        self.assertTrue(reply is not None)
        self.assertEqual(200, reply.status_code)
        self.assertEqual(reply.json['session_id'], session_id)

        reply = client.post(menu["update"], json={"session_id": session_id, "guess": (3, 4, 2, 1)})
        self.assertTrue(reply is not None)
        self.assertEqual(200, reply.status_code)
        self.assertEqual(reply.json['session_id'], session_id)

        reply = client.post(menu["delete"], json={"session_id": session_id})
        self.assertTrue(reply is not None)
        self.assertEqual(200, reply.status_code)
        self.assertEqual(reply.json['session_id'], session_id)

        reply = client.get(menu["home"])
        self.assertTrue(reply is not None)
        self.assertTrue("menu" in reply.json)

    def test_main_menu_checkers_create_read_update_delete_home(self):
        flask_app = create_app()
        client = flask_app.test_client()

        main_menu = client.get("/").json["menu"]

        reply = client.get(main_menu["checkers"])
        menu = reply.json["menu"]

        reply = client.post(menu["create"], json={"game_id": CHECKERS_ID})
        session_id = reply.json["session_id"]
        self.assertTrue(reply is not None)
        self.assertEqual(200, reply.status_code)

        reply = client.get(menu["play"], json={"session_id": session_id})
        self.assertTrue(reply is not None)
        self.assertEqual(200, reply.status_code)
        self.assertEqual(reply.json['session_id'], session_id)

        reply = client.post(menu["update"], json={"session_id": session_id, "move": ((3, 4), (4, 5))})
        self.assertTrue(reply is not None)
        self.assertEqual(200, reply.status_code)
        self.assertEqual(reply.json['session_id'], session_id)

        reply = client.post(menu["delete"], json={"session_id": session_id})
        self.assertTrue(reply is not None)
        self.assertEqual(200, reply.status_code)
        self.assertEqual(reply.json['session_id'], session_id)

        reply = client.get(menu["home"])
        self.assertTrue(reply is not None)
        self.assertTrue("menu" in reply.json)

    def test_main_menu_minesweeper_create_read_update_delete_home(self):
        flask_app = create_app()
        client = flask_app.test_client()

        main_menu = client.get("/").json["menu"]

        reply = client.get(main_menu["minesweeper"])
        menu = reply.json["menu"]

        reply = client.post(menu["create"], json={"game_id": MINESWEEPER_ID})
        session_id = reply.json["session_id"]
        self.assertTrue(reply is not None)
        self.assertEqual(200, reply.status_code)

        reply = client.get(menu["play"], json={"session_id": session_id})
        self.assertTrue(reply is not None)
        self.assertEqual(200, reply.status_code)
        self.assertEqual(reply.json['session_id'], session_id)

        reply = client.post(menu["update"], json={"session_id": session_id, "flag_cell": (1, 1)})
        self.assertTrue(reply is not None)
        self.assertEqual(200, reply.status_code)
        self.assertEqual(reply.json['session_id'], session_id)

        reply = client.post(menu["delete"], json={"session_id": session_id})
        self.assertTrue(reply is not None)
        self.assertEqual(200, reply.status_code)
        self.assertEqual(reply.json['session_id'], session_id)

        reply = client.get(menu["home"])
        self.assertTrue(reply is not None)
        self.assertTrue("menu" in reply.json)

    def test_can_navigate_to_minesweeper_and_back(self):
        flask_app = create_app()
        client = flask_app.test_client()

        main_menu = client.get("/").json["menu"]

        reply = client.get(main_menu["minesweeper"])
        menu = reply.json["menu"]

        reply = client.get(menu["home"])
        self.assertTrue(reply is not None)
        self.assertTrue("menu" in reply.json)

    def test_can_navigate_to_checkers_and_back(self):
        flask_app = create_app()
        client = flask_app.test_client()

        main_menu = client.get("/").json["menu"]

        reply = client.get(main_menu["checkers"])
        menu = reply.json["menu"]

        reply = client.get(menu["home"])
        self.assertTrue(reply is not None)
        self.assertTrue("menu" in reply.json)

    def test_can_navigate_to_mastermind_and_back(self):
        flask_app = create_app()
        client = flask_app.test_client()

        main_menu = client.get("/").json["menu"]

        reply = client.get(main_menu["mastermind"])
        menu = reply.json["menu"]

        reply = client.get(menu["home"])
        self.assertTrue(reply is not None)
        self.assertTrue("menu" in reply.json)

    def test_can_navigate_to_all(self):
        flask_app = create_app()
        client = flask_app.test_client()

        main_menu = client.get("/").json["menu"]

        reply = client.get(main_menu["mastermind"])
        menu = reply.json["menu"]

        reply = client.get(menu["home"])
        self.assertTrue(reply is not None)
        self.assertTrue("menu" in reply.json)

        reply = client.get(main_menu["checkers"])
        menu = reply.json["menu"]

        reply = client.get(menu["home"])
        self.assertTrue(reply is not None)
        self.assertTrue("menu" in reply.json)

        reply = client.get(main_menu["minesweeper"])
        menu = reply.json["menu"]

        reply = client.get(menu["home"])
        self.assertTrue(reply is not None)
        self.assertTrue("menu" in reply.json)
