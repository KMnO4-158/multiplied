.. change_log:

=========
Changelog
=========

v0.10
=====

`v0.10.0 <https://github.com/KMnO4-158/multiplied/releases/tag/v0.10.0>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Major Updates

    - Move hybrid logic to Algorithm class (`844fca2`_)
    - Algorithms now handle sparse Wallace templates (`40c9d18`_)
    - Algorithms now handle sparse Dadda templates (`235662a`_)

Updates

    - Use [Map] unified bounds efficiently (`b5d92dd`_) (`6d21f7a`_)
    - Add raw_dadda_matrix (`bd4056e`_)
    - Rename to_int_matrix -> to_int_array (`158d969`_)

Fixes

    - ``Map`` initialisation (`52c3be8`_)
    - ``isppm`` flagging Map as false (`c851ca5`_)
    - Improve and add sanity checks (`0fe894e`_) (`bdd4368`_) (`b01775f`_) (`9a8bf4d`_)


See full changelog `here <https://github.com/KMnO4-158/multiplied/pull/139>`_

.. _844fca2: https://github.com/KMnO4-158/multiplied/commit/844fca2
.. _40c9d18: https://github.com/KMnO4-158/multiplied/commit/40c9d18
.. _235662a: https://github.com/KMnO4-158/multiplied/commit/235662a
.. _b5d92dd: https://github.com/KMnO4-158/multiplied/commit/b5d92dd
.. _bd4056e: https://github.com/KMnO4-158/multiplied/commit/bd4056e
.. _158d969: https://github.com/KMnO4-158/multiplied/commit/158d969
.. _52c3be8: https://github.com/KMnO4-158/multiplied/commit/52c3be8
.. _c851ca5: https://github.com/KMnO4-158/multiplied/commit/c851ca5
.. _0fe894e: https://github.com/KMnO4-158/multiplied/commit/0fe894e
.. _bdd4368: https://github.com/KMnO4-158/multiplied/commit/bdd4368
.. _b01775f: https://github.com/KMnO4-158/multiplied/commit/b01775f
.. _9a8bf4d: https://github.com/KMnO4-158/multiplied/commit/9a8bf4d

v0.9
=====

`v0.9.0 <https://github.com/KMnO4-158/multiplied/releases/tag/v0.9.0>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Updates

    - Added Conflict Detection (`22fbed1`_)
    - Improved Default Merge Logic (`7bd696e`_)
    - Merge Conflict Resolution (`3a93569`_) (`e7e73cb`_)

Testing

    - Add WALLACE_TREE, DADDA_TREE reference data (`297130d`_)
    - Validate "Official" Wallace and Dadda Tree (`5ac6984`_)

Fixes

    - ``mprint`` Duplicating Prints (`ca51819`_)
    - Algorithm ``dadda=True`` Option Inconsistency (`f1baf08`_)

See full changelog `here <https://github.com/KMnO4-158/multiplied/pull/133>`_

.. _22fbed1: https://github.com/KMnO4-158/multiplied/commit/22fbed1
.. _7bd696e: https://github.com/KMnO4-158/multiplied/commit/7bd696e
.. _3a93569: https://github.com/KMnO4-158/multiplied/commit/3a93569
.. _e7e73cb: https://github.com/KMnO4-158/multiplied/commit/e7e73cb
.. _297130d: https://github.com/KMnO4-158/multiplied/commit/297130d
.. _5ac6984: https://github.com/KMnO4-158/multiplied/commit/5ac6984
.. _ca51819: https://github.com/KMnO4-158/multiplied/commit/ca51819
.. _f1baf08: https://github.com/KMnO4-158/multiplied/commit/f1baf08


v0.8
=====

`v0.8.2 <https://github.com/KMnO4-158/multiplied/releases/tag/v0.8.2>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This patch focused on fully integrating complex Template objects and improving performance.

Updates

    - Batched truth table generation now balanced (`c566789`_)
    - Bounding box based mapping (`fece553`_)
    - Simplified Partial Product Matrix(PPM) sanity check (`6e9104b`_)
    - Finalised complex Template support (`fdf515b`_)
    - Typing and import structure (`8bc35c0`_)

See full changelog `here <https://github.com/KMnO4-158/multiplied/pull/125>`_

.. _c566789: https://github.com/KMnO4-158/multiplied/commit/c566789
.. _fece553: https://github.com/KMnO4-158/multiplied/commit/fece553
.. _6e9104b: https://github.com/KMnO4-158/multiplied/commit/6e9104b
.. _fdf515b: https://github.com/KMnO4-158/multiplied/commit/fdf515b
.. _8bc35c0: https://github.com/KMnO4-158/multiplied/commit/8bc35c0

`v0.8.1 <https://github.com/KMnO4-158/multiplied/releases/tag/v0.8.1>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Updates

    - Complex Templates Now Usable (`42c1a99`_)
    - Automatic Template Result Generation (`fdae851`_)
    - Refactor Reduction via Bounding Boxes (`aa15fb3`_)
    - Ensure Empty Chars Force NOOPs (`18bf6cb`_)
    - Implement Truth Scope Batching (`2b434c7`_)

See full changelog `here <https://github.com/KMnO4-158/multiplied/pull/124>`_

.. _42c1a99: https://github.com/KMnO4-158/multiplied/commit/42c1a99
.. _fdae851: https://github.com/KMnO4-158/multiplied/commit/fdae851
.. _aa15fb3: https://github.com/KMnO4-158/multiplied/commit/aa15fb3
.. _18bf6cb: https://github.com/KMnO4-158/multiplied/commit/18bf6cb
.. _2b434c7: https://github.com/KMnO4-158/multiplied/commit/2b434c7

`v0.8.0 <https://github.com/KMnO4-158/multiplied/releases/tag/v0.8.0>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Updates

    - Added raw_zero_map, raw_dadda_map (`c28e2ef`_)
    - Added raw_zero_matrix(), renamed empty_matrix() to raw_empty_matrix() (`c7f6d80`_)


Tests:

    Initial implementation of Core tests via Pytest:

    - Algorithm (`60c57a7`_)
    - Template and Pattern (`6e74340`_)
    - Truth (`5cea472`_)
    - Matrix (`ba35cee`_)
    - Map (`bcc9c89`_)

Looking forward:

    [Main Focus]

    - Complete Remaining User Guides
    - Bit Tracking / Waveform Analysis

    [ Ongoing ]

    - Map Object Coordinate Refactor
    - Data Structure Optimisation
    - DataFrame Generation Optimisation
    - 16-bit Algorithm Support

See full changelog `here <https://github.com/KMnO4-158/multiplied/pull/120>`_

.. _c28e2ef: https://github.com/KMnO4-158/multiplied/commit/c28e2ef
.. _c7f6d80: https://github.com/KMnO4-158/multiplied/commit/c7f6d80
.. _60c57a7: https://github.com/KMnO4-158/multiplied/commit/60c57a7
.. _6e74340: https://github.com/KMnO4-158/multiplied/commit/6e74340
.. _5cea472: https://github.com/KMnO4-158/multiplied/commit/5cea472
.. _ba35cee: https://github.com/KMnO4-158/multiplied/commit/ba35cee
.. _bcc9c89: https://github.com/KMnO4-158/multiplied/commit/bcc9c89

v0.7
=====

`v0.7.3 <https://github.com/KMnO4-158/multiplied/releases/tag/v0.7.3>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Updates:

    - Expand core.utils unit tests (`0a4e9ea`_)

Documentation:

    - Improve quickstart and structure pages (`f96d975`_)
    - Updated and added theme specific elements to intro page (`bafc7ff`_)
    - Update README project to mirror intro page (`8eff9d1`_)

Bug Fixes:

    - fixed inconsistent `DataFrame` column index usage (`ab53fb4`_)


See full changelog `here <https://github.com/KMnO4-158/multiplied/pull/111>`_

.. _f96d975: https://github.com/KMnO4-158/multiplied/commit/f96d975
.. _bafc7ff: https://github.com/KMnO4-158/multiplied/commit/bafc7ff
.. _8eff9d1: https://github.com/KMnO4-158/multiplied/commit/8eff9d1
.. _0a4e9ea: https://github.com/KMnO4-158/multiplied/commit/0a4e9ea
.. _ab53fb4: https://github.com/KMnO4-158/multiplied/commit/ab53fb4

`v0.7.2 <https://github.com/KMnO4-158/multiplied/releases/tag/v0.7.2>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added:

    - hoist() for Dadda tree mapping (`7a775b4`_)

Documentation:

    - Get Started Page complete (`e5e7527`_)
    - User guide landing page + data structure guide (`3888354`_)

Bug Fixes:

    - Harmonised dataframe column index scheme (`9a9ac50`_)
    - Inconsistent state updates (`46f885b`_)

See full changelog `here <https://github.com/KMnO4-158/multiplied/pull/105>`_

.. _7a775b4: https://github.com/KMnO4-158/multiplied/commit/7a775b4
.. _e5e7527: https://github.com/KMnO4-158/multiplied/commit/e5e7527
.. _3888354: https://github.com/KMnO4-158/multiplied/commit/3888354
.. _9a9ac50: https://github.com/KMnO4-158/multiplied/commit/9a9ac50
.. _46f885b: https://github.com/KMnO4-158/multiplied/commit/46f885b



`v0.7.1 <https://github.com/KMnO4-158/multiplied/releases/tag/v0.7.1>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Updates:

    - Setup "ACT" For Local Github Actions Testing (`5fa50b0`_)
    - Run Tests Before Merge / Publish (`bb9a7cf`_)
    - Update Docstrings to Numpy Style (`84c113d`_)
    - Adopt PyTest (`3e02e1f`_)
    - Add .md Sphinx Support (`5f5916d`_)

Looking forward:

    [ Main Focus ]

    - Expand Analysis
    - Documentation:

      - User Guide
      - Improve Get Started Page

    [ Ongoing ]

    - Refactor tests
    - Map Object Coordinate Refactor
    - Data Structure Optimisation
    - 16-bit Algorithm Support

See full changelog `here <https://github.com/KMnO4-158/multiplied/pull/104>`_

.. _5fa50b0: https://github.com/KMnO4-158/multiplied/commit/5fa50b0eebb9b0aeef20611905786e4a901c70d0
.. _bb9a7cf: https://github.com/KMnO4-158/multiplied/commit/bb9a7cf7a47eaf4b73827e9515ee2e6364ab5acd
.. _84c113d: https://github.com/KMnO4-158/multiplied/commit/84c113dfd2a473ca0f8ad84e0e429fee2c2016be
.. _3e02e1f: https://github.com/KMnO4-158/multiplied/commit/3e02e1f9b33ad1ca50e86c25cd6d7d0aa0d9c71d
.. _5f5916d: https://github.com/KMnO4-158/multiplied/commit/5f5916d75f05abfa942938fdc8c2add4f55b7e5b



v0.6
=====

`v0.6.2 <https://github.com/KMnO4-158/multiplied/releases/tag/v0.6.2>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bug Fixes:

    - Moved pyproject.toml metadata extraction into conf.py (`09d2544`_)
    - Refactored / Harmonised Dataframe, Parquet Access (`ffc8963`_)
    - Dark plot background inconsistencies (`d95bbda`_)

See full changelog `here <https://github.com/KMnO4-158/multiplied/pull/96>`_.

.. _09d2544: https://github.com/KMnO4-158/multiplied/commit/09d254432cf6cd3ace877c493676986d5308b28b
.. _ffc8963: https://github.com/KMnO4-158/multiplied/commit/ffc8963919f54d1934031b0b64354a9838dfd707
.. _d95bbda: https://github.com/KMnO4-158/multiplied/commit/d95bbda239ef04ee959091dd7fe0339777ab003d

`v0.6.0 <https://github.com/KMnO4-158/multiplied/releases/tag/v0.6.0>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Updates:

    - Implement 3D Heatmap (`f7a9a62`_)
    - Implement Dadda-Tree (`6e2b8c8`_)
    - Implement Saturation (`00242fb`_)
    - Streamline Algorithm instantiation (`c420f07`_)

Looking forward:

    [Main Focus]

    - Adopt Numpy Docstring Style
    - Automation / CI/CD
    - Simple User Guide


    [ Ongoing ]

    - Continued development of the API reference site
    - Map Object Coordinate Refactor
    - Adopt Pytest
    - Data Structure Optimisation
    - 16-bit Algorithm Support

See full changelog `here <https://github.com/KMnO4-158/multiplied/pull/91>`_.

.. _f7a9a62: https://github.com/KMnO4-158/multiplied/commit/f7a9a629815d0a668461bb514a566bbb191c097f
.. _6e2b8c8: https://github.com/KMnO4-158/multiplied/commit/6e2b8c85edc5605550b53aa5c39609d31401e736
.. _00242fb: https://github.com/KMnO4-158/multiplied/commit/00242fb7ba9a7c7d12f8d9631620580026851491
.. _c420f07: https://github.com/KMnO4-158/multiplied/commit/c420f07f6a1f3b022ee527fe470f6c2c1007548a

v0.5
=====

`v0.5.0 <https://github.com/KMnO4-158/multiplied/releases/tag/v0.5.0>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Updates:

    - Generated Complete 8-bit Wallace-Tree truth table (`19953dd`_)
    - Export Algorithm to .json (`32d2e90`_)
    - Import and Export to .parquet (`b449ab3`_)
    - Simple Frequency Analysis (`28b088d`_)
    - Export Analysis Results As Heatmap (`28b088d`_)


Looking forward:

    [Main Focus]

    - Saturation
    - Expand Analysis Tools
    - Adopt Numpy Docstring Style
    - Simple User Guide


    [ Ongoing ]

    - Continued development of the API reference site
    - Map Object Coordinate Refactor
    - Adopt Pytest
    - Data Structure Optimisation
    - 16-bit Algorithm Support


See full changelog `here <https://github.com/KMnO4-158/multiplied/pull/69>`_.

.. _19953dd: https://github.com/KMnO4-158/multiplied/pull/69/commits/19953dd1b88f85e44110b273012cfb5f4778ccbc
.. _32d2e90: https://github.com/KMnO4-158/multiplied/pull/69/commits/32d2e90b16500cc2fcecdd5eb47cabb070fa80db
.. _b449ab3: https://github.com/KMnO4-158/multiplied/commit/b449ab35b2720d14e39fc1b9402cd6d3028abee6
.. _28b088d: https://github.com/KMnO4-158/multiplied/pull/69/commits/28b088d891647bb9dedd52d38cbdb9dd4b49ed75

v0.4
=====

`v0.4.0 <https://github.com/KMnO4-158/multiplied/releases/tag/v0.4.0>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Updates:

    - Applying Algorithms to operands (`f728829`_)
    - Expanded Map class to complex maps (`77b2b7e`_)
    - Added complex map generation (`923e85d`_)
    - Added bounding box for efficient arithmetic unit isolation (`3a0a0f6`_)
    - Initial implementaton of checksums (`d0ea73e`_)


Looking forward:

    [Main Focus]

    - Truth table generation via algorithm(s)
    - Export to .parquet files

    [ Ongoing ]

    - Simple Analysis
    - Continued development of the API reference site
    - Simple User Guide
    - Adopt Pytest

See full changelog `here <https://github.com/KMnO4-158/multiplied/commits/v0.4.0>`_.

.. _f728829: https://github.com/KMnO4-158/multiplied/commit/f728829ecdbab0a96fdd6e191595bdfd8f521e98
.. _77b2b7e: https://github.com/KMnO4-158/multiplied/commit/77b2b7e564c1791559dc605b9b02d2a58263dec0
.. _923e85d: https://github.com/KMnO4-158/multiplied/commit/923e85d90c3fff55ac168dc6f95d813cd656c2ce
.. _3a0a0f6: https://github.com/KMnO4-158/multiplied/commit/3a0a0f62d0e70a18d1694f7ae9f6c99923603a58
.. _d0ea73e: https://github.com/KMnO4-158/multiplied/commit/d0ea73e11a55db8308dbe594ef0b067390d8c3ae

v0.3
=====

`v0.3.3 <https://github.com/KMnO4-158/multiplied/releases/tag/v0.3.3>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Updates:

    - Automatic algorithm generation via patterns
    - Implemented reduction via arithmetic units. Work continues for merging results
    - Added groundwork for complex template isolation and sanity checks
    - Added checksums to Template class, allowing for faster traversal
    - Improved and expanded utility functions
    - Bug fixes and improved sanity checks in most classes

Looking forward:

    [Main Focus]

    - Truth table generation via algorithm(s)
    - Applying algorithms to operands
    - Complex mapping
    - Complex templates

    [ Ongoing ]

    - Prepare for complex, custom, templates
    - Export to .parquet files
    - Continued development of the API reference site
    - Adopt Pytest

See full changelog `here <https://github.com/KMnO4-158/multiplied/commits/v0.3.3>`_.

`v0.3.0 <https://github.com/KMnO4-158/multiplied/releases/tag/v0.3.0>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Updates:

    - Secured multiplied on PyPi, test.PyPi and github
    - Assisted algorithm generation via patterns (not true automation)
    - Finalised structure and populated an Algorithm stage `#18 <https://github.com/KMnO4-158/multiplied/issues/18>`_
    - Expanded mp.pretty formatting to all Multiplied types
    - Added to utils.char.py to clean up template generation
    - Generate templates from patterns using existing matrix

    Plus smaller bug fixes and improvements

Looking forward:

    [Main Focus]

    - Automatic algorithm generation via patterns
    - Applying algorithms to operands
    - Truth table generation via algorithm(s)

    [ Ongoing ]

    - Prepare for complex, custom, templates
    - Export to .parquet files
    - Continued development of the API reference site

See full changelog `here <https://github.com/KMnO4-158/multiplied/commits/v0.3.0>`_.

v0.2
====


`v0.2.0 <https://github.com/KMnO4-158/multiplied/releases/tag/v0.2.0>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Updates:

    - API reference site complete and ready for population
    - Changed API ref theme to `breeze <https://github.com/aksiome/breeze>`_
    - Initial implementation for all algorithm related classes
    - Improved interoperability between classes
    - Resolve and produce rmaps for basic templates/matrices

Looking forward:

    [Main Focus]

    - Implement algorithms via built-in templates
    - Prepare for complex, custom, templates
    - Design ways to assist algorithm creation

    [ Ongoing ]

    - Implement exporting to parquet files
    - Continued development of the API reference site


v0.1
====

`v0.1.1 <https://github.com/KMnO4-158/multiplied/releases/tag/v0.1.1>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This patch is focused on documentation and testing the api reference site locally

Updates:

    - progress towards an online api reference site
    - Improved landing page and overall site layout
    - Scripts apidoc.sh and build.sh to automate syncing and creating the sphinx site
    - Added sphinx-rtd-theme
    - minimal additions to codebase, mostly outlining future functionality



`v0.1.0 <https://github.com/KMnO4-158/multiplied/releases/tag/v0.1.0>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This release is a complete refactor of the original script, widening it's scope and turning it into a library.

Added:

    - Classes and a general focus on code reuse
    - Reduction templates for CSA and Adders
    - Initial Documentation

TODO:

    - Documentation and template implementation

For more info on future goals, check out the `roadmap <https://github.com/KMnO4-158/multiplied/blob/master/ROADMAP.md>`_.
