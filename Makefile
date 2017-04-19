run: runDmx

patch:
	@python3 mapping/patch.py

runFile:
	@python3 -i src/Cherry.py -o "/tmp/cherrylog"

runSerial:
	@python3 -i src/Cherry.py -o "/dev/ttyUSB0"

runDmx:
	@python3 -i src/Cherry.py -o "/dev/ttyUSB0"

testPB:
	@python3 test/PatternBuilderTest.py
