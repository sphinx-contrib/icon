:hide-toc:

.. include:: ../../README.rst

Installation
============

first install the `pipy package <https://pypi.org/project/sphinx-icon/>`__ by runinng:

.. code-block:: console

    pip install sphinx-icon

Then add the extention to your :code:`conf.py` file:

.. code-block:: python

    # docs/conf.py

    # [...]

    # -- General configuration -----------------------------------------------------

    # Add any Sphinx extension module names here, as strings. They can be
    # extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
    # ones.
    extensions = [
        "sphinxcontrib.icon",
    ]

Usage
=====

This module provides support for including inlined fontawesome icons in Sphinx rst documents.

This module defines an :code:`:icon:` role which insert the requested icon. It take a single reuired arguments: the icon name. You'll find the complete list of available icons on the `fontawesome website <https://fontawesome.com/v5.15/icons?d=gallery&p=2>`__:

.. code-block:: rst 

    I'm a folder icon: :icon:`fa fa-folder`.

I'm a folder icon: :icon:`fa fa-folder`.

HTML output
-----------

In the HTML output, the CSS and JS from Fontawesome 5.15.4 are added to the output in the :code:`<head>` tag.

.. code-block:: html 

    <link rel="stylesheet" type="text/css" href="<webpath>/build/html/_font/fontawesome/css/all.min.css">
    <!-- -->
    <script src="<webpath>/build/html/_font/fontawesome/css/all.min.js">

Then for each icon role occurence an :code:`<i>` tag will be used: 

.. code-block:: html

    <i class="fa fa-folder"></i>

Latex output
------------

In the latex outut the `fontawesome5 package <https://www.ctan.org/pkg/fontawesome5>`__ is added to the :code:`preamble`:

.. code-block:: Latex

    \usepackage{fontawesome5}

Then for each icon role occurence the following command will be used: 

.. code-block:: latex

    \faIcon[style]{the-icon-name}

with :code:`style` being one of "regular", "solid" or "brand" and :code:`the-icon-name` being everything after :code:`fa-`.