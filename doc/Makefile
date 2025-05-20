# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
TOOLS         = ../doctools

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

dyn_doc:
	@$(TOOLS)/create_dyn_doc.sh

rst:
	@$(TOOLS)/convert_and_send_to_doc.sh

readme:
	../make_readme.sh

doc: dyn_doc rst readme
	make --no-print-directory html

remove_gen_files:
	rm -f `ls -I anatomy_of_a_plugin.jpg -I ssm.rst -I index.rst -I plugin_anatomy.rst -I readme_no_edit.rst -I intro.rst -I livraison.rst -I LICENSE.rst -I tutorial.rst -I _build -I _static -I auto_examples -I conf.py -I spookipy_logo.jpg -I Makefile -I Tutorial.ipynb`
	rm -f ../spookipy_env.txt

clean: remove_gen_files

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
