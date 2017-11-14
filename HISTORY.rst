.. :changelog:

History
=======

0.5.0 (2017-11-14)
------------------

* Now jsail searches fields dict not only in key ``@fields``, but also
  in ``fields``.
* Fixed precendence of fields searched for item's timestamp. Previously,
  item found in ``@timestamp`` can be overwritten by value from
  ``time``. Now these fields are searched in this order and first found
  value is used:

  - ``@timestamp``
  - ``timestamp``
  - ``time``
  - ``(@fields | fields).timestamp``
  - ``(@fields | fields).time``


0.4.0 (2017-05-18)
------------------

* Unbuffered stdin usage was fixed and now program
  exists correctly if it encounter EOF.

0.3.0 (2016-10-03)
------------------

* Now jsail recognizes as timestamp keys ``timestamp``,
  ``time``, ``@fields.timestamp``, ``@fields.time``.
  And similarly, for message these keys are checked:
  ``message``, ``msg``, ``@fields.message``, ``@fields.msg``.
* Now jsail quietly skips lines which can't be parsed
  as single JSON document.

0.2.1 (2016-03-13)
------------------

* Fixed issue with STDIN bufering. Previously,
  input given from STDIN was buffered and sometimes
  ``jsail`` didn't show content until buffer fills up.
  Now this behaviour is fixed.

0.2.0 (2015-07-06)
------------------

* 'anyjson' was added into the requrements list.
* Now jsail will process STDIN if filename wasn't given as a command line argument. This makes possible to use it in unix pipelines.

0.1.0 (2015-04-16)
---------------------

* First release on PyPI.
