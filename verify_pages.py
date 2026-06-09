import sys
sys.path.insert(0, 'backend')
import app as a

c = a.app.test_client()
paths = ['/', '/index.html', '/signup.html', '/forget.html', '/recovery.html', '/static/index.css', '/static/signup.css', '/static/forget.css']
for path in paths:
    r = c.get(path)
    print(path, '->', r.status_code, 'content_type=', r.content_type, 'len=', len(r.data))
