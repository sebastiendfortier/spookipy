# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
TOOLS       = ../doctools

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

insert_version:
	echo 'hello'
	# @$(TOOLS)/insert_version.sh

rst:
	@$(TOOLS)/convert_and_send_to_doc.sh

readme:
	../make_readme.sh

replace:
	echo 'hello'
	# @$(TOOLS)/replace_modified_files.sh

doc: insert_version rst readme replace
	make --no-print-directory html

remove_gen_files:
	rm `ls -I contributing.rst -I ssm.rst -I index.rst -I install.rst -I intro.rst -I LICENSE.rst -I requirements.rst -I tutorial.rst -I usage.rst -I _build -I _static -I auto_examples -I conf.py -I spookipy_logo.jpg -I Makefile`

clean: remove_gen_files

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
