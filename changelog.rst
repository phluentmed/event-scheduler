.. _changelog:

================
 Change History
================

This document contains change notes for bugfix & new features
in the 0.x.x series,

.. _version-0.1.0:

0.1.0
=====
:release-date: 2021-03-07 5.46 P.M UTC-5:00
:release-by: Dil Mchaina

- Add scheduling of recurring events
- Add testutil to aid in testing application code with an event scheduler
- Some naming changes in the tests

0.1.1
=====
:release-date: 2021-04-24 12.22 A.M UTC-5:00
:release-by: Dil Mchaina

- Fix bug involving field naming in Event namedtuple
- Fix relative link in README.md in pypi

0.1.2
=====
:release-date: 2021-05-02 9.09 P.M UTC-5:00
:release-by: Dil Mchaina

- Fix bug when cancelling an already executed event when the queue is empty
- Bump version on urllib3 due to security issues

0.1.3
=====
:release-date: 2022-01-06 1.20 A.M UTC-5:00
:release-by: Dil Mchaina

- Bump urllib3 from 1.26.4 to 1.26.5 in /docs
- Bump babel from 2.9.0 to 2.9.1 in /docs
- Minor optimization