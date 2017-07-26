from application import application

if __name__ == '__main__':
	application.config.from_object('config.Config')
	application.config.from_pyfile('amazonRDS.py')
	application.run()
