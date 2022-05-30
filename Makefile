.PHONY: clean
binaries=dist build

install:
	python3 setup.py install

dist:
	python3 setup.py sdist

build:
	python3 setup.py build

upload: clean dist
	twine upload dist/*

clean:
	rm -rf $(binaries)

