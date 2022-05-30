.PHONY: clean
binaries=dist build

dist:
	python3 setup.py sdist

build:
	python3 setup.py build

upload: clean dist
	twine upload dist/*

clean:
	rm -rf $(binaries)

