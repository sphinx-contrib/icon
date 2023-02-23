Quickstart
==========

This section contains basic information about **sphinx-icon** to get you started.

Installation
------------

Use ``pip`` to install **sphinx-icon** in your environment:

.. code-block:: console

    pip install sphinx-icon

Extension setup
---------------


After installing **sphinx-icon**, add ``sphinxcontrib.icon`` to the list of extensions
in your ``conf.py`` file:

.. code-block:: python

    extensions = [
        #[...]
        "sphinxcontrib.icon",
    ]

Icon directive
--------------

You can now add icons directly in your documentation:

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