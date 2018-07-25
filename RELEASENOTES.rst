===========
oslo.policy
===========

.. _oslo.policy_1.38.1:

1.38.1
======

.. _oslo.policy_1.38.1_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/policy-check-performance-fbad83c7a4afd7d7.yaml @ b'909a1ea3a7aceb6e0637058b9c6a53d14043d6d1'

- As reported in launchpad bug 1723030, under some circumstances policy
  checks caused a significant performance degradation. This release includes
  improved logic around rule validation to prevent that.


.. _oslo.policy_1.38.0:

1.38.0
======

.. _oslo.policy_1.38.0_New Features:

New Features
------------

.. releasenotes/notes/bug-1779172-c1323c0f647bc44c.yaml @ b'775641a5fc549c20be37cf862deca394bf7f2d21'

- [`bug 1779172 <https://bugs.launchpad.net/keystone/+bug/1779172>`_]
  The ``enforce()`` method now supports the ability to parse ``oslo.context``
  objects if passed into ``enforce()`` as ``creds``. This provides more
  consistent policy enforcement for service developers by ensuring the
  attributes provided in policy enforcement are standardized. In this case
  they are being standardized through the
  ``oslo_context.context.RequestContext.to_policy_values()`` method.


.. _oslo.policy_1.38.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/bug-1779172-c1323c0f647bc44c.yaml @ b'775641a5fc549c20be37cf862deca394bf7f2d21'

- [`bug 1779172 <https://bugs.launchpad.net/keystone/+bug/1779172>`_]
  The ``enforce()`` method now supports the ability to parse ``oslo.context``
  objects if passed into ``enforce()`` as ``creds``. This provides more
  consistent policy enforcement for service developers by ensuring the
  attributes provided in policy enforcement are standardized. In this case
  they are being standardized through the
  ``oslo_context.context.RequestContext.to_policy_values()`` method.

.. releasenotes/notes/expand-cli-docs-02c2f13adbe251c0.yaml @ b'3fe95b2aebde226bab0d710885f60a1862499b16'

- [`bug 1741073 <https://bugs.launchpad.net/oslo.policy/+bug/1741073>`_]
  Documentation has been improved to include ``oslopolicy-sample-generator``
  and ``oslopolicy-list-redundant`` usage.


.. _oslo.policy_1.37.0:

1.37.0
======

.. _oslo.policy_1.37.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/add-scope-types-to-sphinxext-cacd845c4575e965.yaml @ b'eb1546fdfc157ebce0d52cbee54e2898d13de245'

- [`bug 1773473 <https://bugs.launchpad.net/oslo.policy/+bug/1773473>`_]
  The ``sphinxext`` extension for rendering policy documentation now supports
  ``scope_types`` attributes.

.. releasenotes/notes/fix-rendering-for-deprecated-rules-d465292e4155f483.yaml @ b'0f31938dd720015444e03f0056c0cfc0e4b8e932'

- [`bug 1771442 <https://bugs.launchpad.net/oslo.policy/+bug/1771442>`_]
  Policy rules that are deprecated for removal are now properly formatted
  when rendering sample policy files for documentation.

