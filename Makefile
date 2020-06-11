define \n


endef

PYTHON = python
PIP = pip

BENCHMARK_FILES = ed_performance.py KG_performance.py pack_performance.py encode_decode_performance.py

.PHONY = help build clean test generate-tests benchmark test-legacy generate-tests-legacy

help:
	@echo "  help             this message"
	@echo "  build            install requirements and build GE25519 arithmetic library"	
	@echo "  clean            remove floodberry/build, __pycache__, testing *.p files"
	@echo "  benchmark LEN=   performance tests, use LEN to specify byte size of message"
	@echo "  test             run unit test using unittest package"
	@echo "  gen-test         generate new TDF structures for unit testing"
	@echo "  test-legacy      run unit tests for legacy implementations"
	@echo "  gen-test-legacy  generate new TDF structures for legacy testing"

build:
	pipenv install || $(PIP) install -r requirements.txt || $(PYTHON) -m pip install -r requirements.txt
	cd floodberry; \
		$(PYTHON) setup.py build_ext -i
	@echo "Finished setting up without issue."

clean:
	rm -fr floodberry/build
	
	rm -fr __pycache__
	rm -fr floodberry/__pycache__
	rm -fr performance/__pycache__
	rm -fr tests/__pycache__
	rm -fr legacy/tests/__pycache__
	rm -fr legacy/reedsolomon/__pycache__
	rm -fr legacy/__pycache__
	rm -fr *.pyc
	rm -fr floodberry/*.pyc
	rm -fr performance/*.pyc
	rm -fr tests/*.pyc
	rm -fr legacy/tests/*.pyc
	rm -fr legacy/reedsolomon/*.pyc
	rm -fr legacy/*.pyc
	
	rm -fr performance/*.p
	rm -fr tests/*.p
	rm -fr legacy/tests/*.p

benchmark: 
ifneq (,$(LEN))
	cd performance; \
		$(PYTHON) generate_performance_files.py $(LEN) 
endif
ifeq (0, $(words $(wildcard performance/*.p)))
	cd performance; \
		$(PYTHON) generate_performance_files.py 32
endif
	cd performance; \
		$(foreach f, $(BENCHMARK_FILES), $(PYTHON) $(f); \${\n})

test:
ifeq (0, $(words $(wildcard performance/*.p)))
	@echo "No testing data found, generating...\n"
	make gen-test
	@echo "Continuing with unit testing...\n"
endif
	$(PYTHON) -m unittest discover tests

gen-test:
	@echo "\nGenerating new test files\n"
	cd tests; \
		$(PYTHON) generate_test_ddh_tdf.py
	@echo "\nFinished generating new test files\n"

test-legacy:
ifeq (0, $(words $(wildcard performance/*.p)))
	@echo "No test files found, generating...\n"
	make gen-test-legacy
	@echo "Continuing with unit testing...\n"
endif
	PYTHONPATH=legacy $(PYTHON) -m unittest discover legacy/tests

gen-test-legacy:
	@echo "  Generating new test files for LEGACY implementation\n"
	cd legacy/tests; \
		$(PYTHON) generate_test_ctdf.py ;\
		$(PYTHON) generate_test_ltdf.py
	@echo "\n  Finished generating new test files"
	
	
