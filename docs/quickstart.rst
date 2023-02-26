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

    I'm an :icon:`fa-solid fa-folder` icon.
    I'm an :icon:`fa-regular fa-user` icon.
    I'm an :icon:`fa-brands fa-500px` icon.

I'm an :icon:`fa-solid fa-folder` icon.

I'm an :icon:`fa-regular fa-user` icon.

I'm an :icon:`fa-brands fa-500px` icon.

.. note::

    Support is provided for older version of Fontawesome. Documentation using ``fas|far|fab`` or ``fa`` will continue working. Be aware that the icon you want to use may changed name since then.

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

For the latex output, the **sphinx-icon** extention need to use the webfonts provided by fontawesome. It will thus force the use of the XeLaTex builder to allow use of the `fontspec package <https://ctan.org/pkg/fontspec?lang=en>`__. Then 3 new font will be added to the preamble of the tex file:

.. code-block:: latex

    \newfontfamily{\solid}{fa-solid-900.ttf}
    \newfontfamily{\regular}{fa-regular-400.ttf}
    \newfontfamily{\brands}{fa-brands-400.ttf}

Then for each icon role occurence the following command will be used:

.. code-block:: latex

    {\solid\symbol{"F007}}

where ``solid`` is the font style selected in the role and ``F007`` being the unicode of the selected icon.
