from django.test import TestCase
from django.http import JsonResponse, HttpRequest
from chatgpt.views import ensure_conversation_history, DivContent, update_conversation_history, get_total_tokens_in_history, chat
from unittest.mock import patch


class ChatGPTViewsTest(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.session = patch(
            'django.contrib.sessions.backends.db.SessionBase')

    # Test to ensure that a 'conversation_history' session variable is initialized

    def test_ensure_conversation_history(self):
        ensure_conversation_history(self.request)
        self.assertTrue('conversation_history' in self.request.session)

    # Test to check if the DivContent function correctly receives and stores 'content' in session
    def test_DivContent(self):
        self.request.GET = {'content': 'hello'}
        response = DivContent(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.request.session.get('content'), 'hello')

    # Test to validate that 'update_conversation_history' updates the session's conversation history correctly
    def test_update_conversation_history(self):
        self.request.session['conversation_history'] = []
        with patch('builtins.open', read_data='prompt_text'):
            update_conversation_history(self.request, 'test_content')
        self.assertTrue(len(self.request.session['conversation_history']) > 0)

    # Test to validate that 'get_total_tokens_in_history' returns the correct number of tokens for a given conversation history
    def test_get_total_tokens_in_history(self):
        history = [{'role': 'user', 'content': 'hello'},
                   {'role': 'system', 'content': 'hi'}]
        tokens = get_total_tokens_in_history(history)
        self.assertIsInstance(tokens, int)

    # Test to validate that the 'chat' function behaves as expected, including interacting with the OpenAI API
    @patch('openai.ChatCompletion.create')
    def test_chat(self, mock_create):
        # Mocking OpenAI API response
        mock_create.return_value = {'choices': [
            {'message': {'content': 'Hello!'}}], 'usage': {'total_tokens': 10}}
        self.request.GET = {'message': 'hi'}
        response = chat(self.request)
        self.assertEqual(response.status_code, 200)
        # Validate that the assistant's response is stored in the session's conversation history
        self.assertTrue(
            'assistant' in self.request.session['conversation_history'][-1]['role'])
