import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
	'Babel==0.9.6',
	'chameleon==2.11',
	'D2LValence==0.1.14',	
	'fanstatic==0.16',
	'fa.jquery==0.9.5',
	'FormAlchemy==1.4.3',
	'html5lib==0.95',
	'js.jqgrid==4.4.4',
	'js.jquery==1.9.1',
	'js.jquery_form==3.09',
	'js.jquery_jgrowl==1.2.5',
	'js.jquery_markitup==1.1.10_1',
	'js.jqueryui==1.8.24',
	'js.jqueryui_selectmenu==0.1',
	'js.tinymce==3.5.2_1',
	'mako==0.7.3',
	'markdown==2.2.1',
	'markupsafe==0.15',
	'pisa==3.0.33',
	'postmarkup==1.2.0',
	'Pygments==1.6',
	'pymysql==0.5',
	'pyPDF==1.11',
	'pyramid_fanstatic==0.4',
	'pyramid_formalchemy==0.4.3',
	'pyramid_mailer==0.11',
	'pyramid_rewrite==0.2',
	'pyramid_tm==0.7',
	'reportlab==2.7',
	'repoze.lru==0.6',
	'repoze.sendmail==4.0',
	'requests==1.2.0',
	'simplejson==3.1.0',
	'tempita==0.5.1',
	'textile==2.1.5',
	'transaction==1.4.1',
	'translationstring==1.1',
	'venusian==1.0a7',
	'waitress==0.8.2',
	'weberror==0.10.3',
	'webhelpers==1.3',
	'webob==1.2.3',
	'webtest==2.0.6',
	'zope.component==4.1.0',
	'zope.deprecation==4.0.2',
	'zope.event==4.0.2',
	'zope.interface==4.0.5',
	'zope.sqlalchemy==0.7.2',
	'pyramid==1.3.3',
	'SQLAlchemy==0.7.8',
    ]

	
setup(name='QuizSmith',
      version='1.0.1',
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

