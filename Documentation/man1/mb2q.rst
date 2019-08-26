.. SPDX-License-Identifier: GPL-2.0

mb2q manual page
================

Synopsis
--------

**mb2q** [*options*] inbox

Description
-----------

:program:`mb2q`, A program to create a quilt patch series from a mailbox

mb2q analyses the complete mailbox and collects various tags (Reviewed-by,
Acked-by, Tested-by) from replies to individual patches and to the cover
letter. If a tag is in a reply to the cover letter it is applied to all
patches which reference the cover letter.

Optionally the output can be redirected into a mailbox which can be applied
with git-am.

Options
-------

positional arguments:
  inbox                 Input mailbox file

optional arguments:

  -h, --help            show this help message and exit

  -c CONFIG, --config CONFIG
                        Config file. Default: ~/.mb2q.yaml

  -F, --fromnodup       Do not duplicate From into the body
  			By default the From: header is copied
			into the mail body (changelog) which is
			is convenient if patches which have been
			collected from a mailing list are resent.

			A From: tag which is already in the mail
			body is preserved and not replaced.

  -m MBOXOUT, --mboxout MBOXOUT
			Do not store the result in a quilt series. Generate
			a mailbox instead which can be applied with git-am

  -n, --nolink          Do not add Link:// tags to patches
  
  
  -N, --noid            Do not require Message ID. Implies --nolink.
			For testing and in really bad cases.
  
  -p PATCHESDIR, --patchesdir PATCHESDIR
                        Use given directory and do not automatically create
                        patches-$inbox/
			
  -a ACKEDBY, --ackedby ACKEDBY
                        Add Acked-by to all patches. Comma separated list.
                        "Joe Devel <joe@dev.el>, Dev Joe <dev@joe.org>"
			
  -r REVIEWEDBY, --reviewedby REVIEWEDBY
                        Add Reviewed-by to all patches. Comma separated list.
			
  -t TESTEDBY, --testedby TESTEDBY
                        Add Tested-by to all patches. Comma separated list

  -C, --CollectCC       Collect all CCs from mail header


Configuration file
------------------

The program has a default configuration built in which can be reconfigured
with a configuration file. The default location is ~/.mb2q.yaml. This can
be overridden by the '-c' command line argument.

Configuration options
---------------------

  .. code-block:: yaml

     committer: Surname Name <name@email.addr>

     nocc_addrs:
      - nocc@email.addr
      - another.nocc@email.addr

     list_addrs:
      - linux-kernel@vger.kernel.org
      - another-list@listserver.org

     drop_from:
      - '<MAILER-DAEMON@'

     link_base: https://lkml.kernel.org/r/

     dropcc: True

     sob_before_cc: True

committer:
^^^^^^^^^^

  Set the committer name/email for the Signed-off-by tag. If the entry is
  not in the configuration file mb2q tries to find the committer via git or
  the relevant git enviroment variables.

nocc_addrs:
^^^^^^^^^^^

  Mail addresses which are always dropped from the Cc list of a mail
  independent of the dropcc config option and the '-C' command line
  parameter

list_addrs:
^^^^^^^^^^^

  A list of mailing list mail addresses which if matches are:

    - a indicator to append a Link tag based on the link_base configuration
      entry and the message id of the patch mail

    - removed from the cc list independent of the dropcc config option and
      the '-C' command line parameter

drop_from:
^^^^^^^^^^

  A list of email addresses which cause a mail in the mailbox to be ignored.
  That's useful if the email client which is used to store the mailbox inserts
  an administrative email at the beginning of the mailbox. The above example
  catches that mail inserted by alpine.

link_base:
^^^^^^^^^^

  The base URL for creating Link: tags in the changelog. The Message-ID of
  the patch mail is appended to the base URL.

dropccs:
^^^^^^^^

  If True which is also the built-in default all Cc's are stripped from the
  changelog. If False the Cc's in the changelog of the patch mail are
  preserved. The default is True because having all that Cc noise in the
  change log is pointless when the original mail can be retrieved via the
  Link tag.

sob_before_cc:
^^^^^^^^^^^^^^

 It true mb2q emits the committer SOB before Cc and Link tags. Otherwise at
 after all tags.

Examples
--------

Analyze a mailbox named 'mbox' and store the resulting quilt series in the
directory 'patches-mbox'. If the directory does not exit, it is created. If
a series file exists in a already existing directory the patches are
appended to the existing series. The file names for the patch files are
generated from the subject line. If name conflicts occur, then a increasing
version number is appended to the file name::

  $ mb2q mbox
  $ ls patches-mbox

When the directory name is chosen, then leading path components are
stripped off::

  $ mb2q ~/mail/mbox
  $ ls patches-mbox

Same as above, but forces mb2q to use the directory 'patches' and not
create one based on the name of the mailbox::

  $ mb2q -p patches mbox
  $ quilt series

Analyze 'mbox' and store the result as a mailbox in 'obox'. The resulting
mailbox has all the same tag collection and formatting features as the
quilt version and can be directly applied with 'git-am'::

  $ mb2q -o obox mbox
  $ git-am obox

Analyze mbox and add command line supplied acks and tested by to all
patches in 'mbox'::

  $ mb2q -a "Joe Hacker <jh@ack.er>, Acker Jon <ack@er.jon>' -t 'Mary Tester <mary@test.er>' mbox


See also
--------

License
-------
Gnu Public License version 2

    
