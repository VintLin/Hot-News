# import sys
# sys.path.append('..')
# ^server have

from App import create_app


def Exec():
    app = create_app()
    app.run(debug=True)


Exec()