PIXI_CHECK := $(shell command -v pixi 2> /dev/null)
PIXI_CMD := $(if $(PIXI_CHECK),pixi,. ssmuse-sh -p /fs/ssm/eccc/cmd/cmds/apps/pixi/202504/00/pixi_0.44.0_all && pixi)

# Define variables for source command generation
GITLAB_CI_SOURCES := $(shell awk '/^\s*-\s*\.\s*(r\.load\.dot|ssmuse-sh)/ {gsub(/^\s*-\s*\./, ""); gsub(/^\s+|\s+$$/, ""); printf ". %s && ", $$0}' .gitlab-ci.yml)

.PHONY: test lint lint-fix format build doc conda-build conda-upload test-both clean help

# Development targets
test:
	@echo "********* Running test target *********"
	$(PIXI_CMD) run -e dev test 

test-ssm:
	@echo "********* Running test-ssm target *********"
	$(GITLAB_CI_SOURCES) \
	cd test && python -m pytest -vrf

lint:
	@echo "********* Running lint target *********"
	$(PIXI_CMD) run -e dev lint

lint-fix:
	@echo "********* Running lint-fix target *********"
	$(PIXI_CMD) run -e dev lint-fix

format:
	@echo "********* Running format target *********"
	$(PIXI_CMD) run -e dev format

build:
	@echo "********* Running build target *********"
	$(PIXI_CMD) run -e dev build

doc:
	@echo "********* Running doc target *********"
	$(PIXI_CMD) run -e dev doc

# Conda package management
conda-build: clean
	@echo "********* Running conda-build target *********"
	$(PIXI_CMD) run -e dev conda-build

conda-upload: 
	@echo "********* Running conda-upload target *********"
	$(PIXI_CMD) run -e dev conda-upload

test-py38: clean
	@echo "********* Testing package with python 3.8 *********"
	cd package_tests/environments && $(PIXI_CMD) run -e py38 tests

test-py39: clean
	@echo "********* Testing package with python 3.9 *********"
	cd package_tests/environments && $(PIXI_CMD) run -e py39 tests

test-py310: clean
	@echo "********* Testing package with python 3.10 *********"
	cd package_tests/environments && $(PIXI_CMD) run -e py310 tests

test-py311: clean
	@echo "********* Testing package with python 3.11 *********"
	cd package_tests/environments && $(PIXI_CMD) run -e py311 tests

test-py312: clean
	@echo "********* Testing package with python 3.12 *********"
	cd package_tests/environments && $(PIXI_CMD) run -e py312 tests

test-py313: clean
	@echo "********* Testing package with python 3.13 *********"
	cd package_tests/environments && $(PIXI_CMD) run -e py313 tests

test-all: test-py38 test-py39 test-py310 test-py311 test-py312 test-py313


# Default target
all: lint test doc
	@echo "********* Running default target (lint test doc) *********"

# Clean target
clean:
	@echo "********* Running clean target *********"
	scripts/clean.sh
	

help:
	@echo "Available targets:"
	@echo "  test: Run tests"
	@echo "  lint: Run linting"
	@echo "  lint-fix: Run linting and fix issues"
	@echo "  format: Run code formatting"
	@echo "  build: Build the package"
	@echo "  doc: Build documentation"
	@echo "  conda-build: Build conda package"
	@echo "  conda-upload: Upload conda package"
	@echo "  test-py38: Test with Python 3.8"
	@echo "  test-py313: Test with Python 3.13"
	@echo "  test-both: Test with Python 3.8 and 3.13"
	@echo "  all: Run lint, test, and doc targets"
	@echo "  clean: Clean up build artifacts"
	@echo "  help: Show this help message"
