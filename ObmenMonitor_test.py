import os
import server
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()
        #server.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(server.app.config['DATABASE'])

    def test_index_page(self):
        rv = self.app.get('/')
        assert 'localhost:8080' in rv.data

    def test_add_client(self):
        rv = self.app.post('/edit_client', data=dict(
        name='First client',
        clientid='clientid'
    ), follow_redirects=True)

        assert 'First client' in rv.data
        assert 'clientid' in rv.data


if __name__ == '__main__':
    unittest.main()