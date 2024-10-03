
all:
	cd sipgen
	$(MAKE)
	@cd ..
	cd siplib
	$(MAKE)
	@cd ..

install:
	cd sipgen
	$(MAKE) install
	@cd ..
	cd siplib
	$(MAKE) install
	@cd ..
	@if not exist C:\Users\USER\AppData\Local\Programs\Python\Python312\Lib\site-packages mkdir C:\Users\USER\AppData\Local\Programs\Python\Python312\Lib\site-packages
	copy /y sipconfig.py C:\Users\USER\AppData\Local\Programs\Python\Python312\Lib\site-packages\sipconfig.py
	copy /y "C:\Users\USER\Documents\network app\sip-4.19.2\sipdistutils.py" C:\Users\USER\AppData\Local\Programs\Python\Python312\Lib\site-packages\sipdistutils.py

clean:
	cd sipgen
	$(MAKE) clean
	@cd ..
	cd siplib
	$(MAKE) clean
	@cd ..
