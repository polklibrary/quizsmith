import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid==1.3.3',
    'SQLAlchemy==0.7.8',
    'transaction==1.4.1',
    'pyramid_tm==0.7',
    'zope.sqlalchemy==0.7.2',
    'waitress==0.8.2',
    'pymysql==0.5',
    'pyramid_formalchemy==0.4.3',
    'fa.jquery==0.9.5',
    'fanstatic==0.16',
    'pyramid_fanstatic==0.4',
    'pyramid_mailer==0.11',
    'pisa==3.0.33',
    'reportlab==2.7',
    'html5lib==0.95',
    'requests==1.2.0',
    'pyPDF==1.11',
    ]

setup(name='QuizSmith',
      version='1.0.0',
      description='QuizSmith',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='David Hietpas',
      author_email='hietpasd@uwosh.edu',
      url='http://www.uwosh.edu/library/quizsmith',
      keywords='Quiz Education Trivia BarTrivia Bar Assessment Fun',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='quizsmith',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = quizsmith:main
      [console_scripts]
      initialize_Trivia_db = quizsmith.scripts.initializedb:main
      """,
      )

