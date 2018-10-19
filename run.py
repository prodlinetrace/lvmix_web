#!/usr/bin/env python
import sys
from app import create_app
from app import db

app = create_app('default')

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', threaded=True)
    db.create_all()
