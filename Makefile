# vim: set fileencoding=utf-8:


SHELL=/bin/bash

API_DOC_DIR="./docs"
BUILD=./build
# DEVPI_HOST=$(shell cat devpi-hostname.txt)
# DEVPI_PASSWORD=$(shell cat ./devpi-password.txt)
# DEVPI_USER=$(shell cat ./devpi-user.txt)
DIST=./dist
MANPAGES=./manpages
MAN_SECTION=5
PACKAGE=$(shell cat package.txt)
REQUIREMENTS=requirements.txt
TWINEPASSWD_FILE_NAME="$(HOME)/.twinepasswd"
TWINE_CREDENTIALS_DEFINED=$(shell test -e $(TWINEPASSWD_FILE_NAME) ; echo "$$?")
TWINE_USER=$(shell [[ -e $(TWINEPASSWD_FILE_NAME) ]] && jq -r ".user" "$(TWINEPASSWD_FILE_NAME)")
TWINE_PASSWORD=$(shell [[ -e $(TWINEPASSWD_FILE_NAME) ]] && jq -r ".password" "$(TWINEPASSWD_FILE_NAME)")
VERSION=$(shell echo "from $(PACKAGE) import __VERSION__; print(__VERSION__)" | python)


# Targets:

all: ALWAYS
	make test
	make package
	make docs


# TODO: Use rm -Rfv $$(find $(PACKAGE) | awk '/__pycache__$$/') after the $(PACKAGE)
#       package is claimed to this project by PyPI.
clean:
	rm -Rf $(API_DOC_DIR)/*
	rm -Rf $(BUILD)/*
	rm -Rf $(DIST)/*
	rm -Rf $(MANPAGES)/*
	rm -Rfv $$(find $(PACKAGE)/ | awk '/__pycache__$$/')
	rm -Rfv $$(find tests | awk '/__pycache__$$/')
	rm -Rfv $$(find . | awk '/.ipynb_checkpoints/')
	pushd ./dist ; pip uninstall -y $(PACKAGE)==$(VERSION) || true ; popd


devpi:
	devpi use $(DEVPI_HOST)
	@devpi login $(DEVPI_USER) --password="$(DEVPI_PASSWORD)"
	devpi use $(DEVPI_USER)/dev
	devpi -v use --set-cfg $(DEVPI_USER)/dev
	@[[ -e "pip.conf-bak" ]] && rm -f "pip.conf-bak"


docs: ALWAYS
	pip install -U pdoc pylint
	mkdir -p $(MANPAGES)
	t=$$(mktemp) && awk -v "v=$(VERSION)" '/^%/ { $$4 = v; print; next; } { print; }' README.md > "$$t" && cat "$$t" > README.md && rm -f "$$t"
	pandoc --standalone --to man README.md -o $(MANPAGES)/$(PACKAGE).$(MAN_SECTION)
	mkdir -p $(API_DOC_DIR)
	VERSION="$(VERSION)" pdoc --logo="https://assets.website-files.com/6287e9b993a42a7dcb001b99/6287eb0b156c574ac578dab3_Triple-Logo-Full-Color.svg" --favicon="https://assets.website-files.com/6287e9b993a42a7dcb001b99/628bc3aee64e1c6c0f5e3863_Triple%20favicon.png" -n -o $(API_DOC_DIR) -t ./resources $(PACKAGE) 
	pyreverse --max-color-depth=6 --colorized --output-directory ./resources -o png coronado


install:
	pip install -U $(PACKAGE)==$(VERSION)
	pip list | awk 'NR < 3 { print; } /$(PACKAGE)/'


libupdate:
	pip install -U pip
	pip install -Ur $(REQUIREMENTS)


local:
	pip install -e .


nuke: ALWAYS
	make clean


package:
	pip install -r $(REQUIREMENTS)
	python setup.py bdist_wheel


# The publish: target is for PyPI, not for the devpi server.
# https://www.python.org/dev/peps/pep-0541/#how-to-request-a-name-transfer
#
# PyPI user name:  ciurana; pypi AT cime_net
publish:
ifeq ($(TWINE_CREDENTIALS_DEFINED), 1)   # shell exit code! 1 == false, 0 == true
	@echo "Unable to build - please ensure $(TWINEPASSWD_FILE_NAME) exists"
	@exit 1
endif
	pip install -U twine
	twine --no-color check $(DIST)/*
	@twine --no-color upload -u $(TWINE_USER) -p $(TWINE_PASSWORD) --verbose $(DIST)/*


refresh: ALWAYS


# Delete the Python virtual environment - necessary when updating the
# host's actual Python, e.g. upgrade from 3.7.5 to 3.7.6.
resetpy: ALWAYS
	rm -Rfv ./.Python ./bin ./build ./dist ./include ./lib


targets:
	@printf "Makefile targets:\n\n"
	@cat Makefile| awk '/:/ && !/^#/ && !/targets/ && !/Makefile/ { gsub("ALWAYS", ""); gsub(":", ""); print; } /^ALWAYS/ { next; }'


# TODO: Use rm -Rfv $$(find $(PACKAGE) | awk '/__pycache__$$/') after the $(PACKAGE)
#       package is claimed to this project by PyPI.
test: ALWAYS
	@echo "Version = $(VERSION)"
	pip install -r requirements.txt
	pip install -e .
	pytest -v ./tests/test_$(PACKAGE).py
	pytest -v ./tests/test_address.py
	pytest -v ./tests/test_auth.py
	pytest -v ./tests/test_cardaccount.py
	pytest -v ./tests/test_cardprog.py
	pytest -v ./tests/test_display.py
	pytest -v ./tests/test_exceptions.py
	pytest -v ./tests/test_health.py
	pytest -v ./tests/test_merchant.py
	pytest -v ./tests/test_merchantcodes.py
	pytest -v ./tests/test_offer.py
	pytest -v ./tests/test_publisher.py
	pytest -v ./tests/test_reward.py
	pytest -v ./tests/test_tools.py
	pytest -v ./tests/test_transaction.py
	pip uninstall -y $(PACKAGE)==$(VERSION) || true
	rm -Rfv $$(find $(PACKAGE)/ | awk '/__pycache__$$/')
	rm -Rfv $$(find tests | awk '/__pycache__$$/')


tools:
	pip install -U devpi-client pip ptpython pudb pytest


upload:
	devpi upload dist/*whl


ALWAYS:

