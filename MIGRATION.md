# Migration Mailman 2->3

## RampUp

### Mailman 3 basic setup

*Fast Track after installation of RPM*

#### Basic configuration

##### File: /etc/mailman.cfg

 - Check: site_owner


##### File: /etc/mailman3/settings.py

 - Check: CSRF_TRUSTED_ORIGINS
 - Check: DEFAULT_FROM_EMAIL
 - Check: SERVER_EMAIL
 - Check: CAPTCHA_SERVICE
 - Check: CAPTCHA_SITE_KEY
 - Check: CAPTCHA_SECRET

### Start mailman3

```
# systemctl start mailman3
```

If successful, enable autostart

```
# systemctl enable mailman3
```

### Start mailman3-web

```
# systemctl start mailman3-web
```

If successful, enable autostart

```
# systemctl enable mailman3-web
```

#### Super usercreation

- Become "mailman3" user

```
# su - -s /bin/bash mailman3
```

Example, e-mail address is important for verification, password should be a super-secret one

```
mailman-web createsuperuser
Username (leave blank to use 'mailman3'): listmaster
Email address: listmaster@domain.example
Password: 
Password (again): 
Superuser created successfully.
```

### Postfix (after mailman3 initial start)

#### File: /etc/postfix/main.cf

 - Check: recipient_delimiter
 - Extend: transport_maps: `hash:/var/lib/mailman3/data/postfix_lmtp`
 - Extend: local_recipient_maps or virtual_alias_maps (depending on local setup)
   - local: <TODO>
   - virtual: `hash:/var/lib/mailman3/data/postfix_vmap`

Reload postfix
```
systemctl reload postfix
```

## Status

### Show lists of mailman2

```
# su - -s /bin/bash mailman
$ /usr/lib/mailman/bin/list_lists
```

### Show lists of mailman3
```
# su -s -s /bin/bash mailman3
$ mailman3 lists -n
```

### Grant mailman3 access to mailman2

Notes:
  - only required in case of migration on same system
  - usually, directory permissions prevent mailman3 reading files of mailman2

```
# usermod -G mailman -a mailman3
```

Note: can be revoked after migration

## Pre-Migration

### For migration on same system as "mailman" is running, special alias subdomain is required to be configured

See also: https://docs.mailman3.org/projects/mailman/en/latest/src/mailman/docs/mta.html

*ATTENTION, THIS WILL DELETE ALREADY CONFIGURED LISTS*

```
# su - -s /bin/bash mailman3
$ mailman3 shell

from mailman.interfaces.domain import IDomainManager
from zope.component import getUtility
manager = getUtility(IDomainManager)
from operator import attrgetter

def show_domains(*, with_owners=False):
     if len(manager) == 0:
         print('no domains')
         return
     for domain in sorted(manager, key=attrgetter('mail_host')):
        print(domain)
     owners = sorted(owner.addresses[0].email
                     for owner in domain.owners)
     for owner in owners:
         print('- owner:', owner)


show_domains()
<Domain <DOMAIN>>

manager.remove('<DOMAIN>')
manager.add('<DOMAIN>', alias_domain='x.<DOMAIN>')

show_domains()
<Domain <DOMAIN>, alias: x.<DOMAIN>

## end session with CTRL-D

$ mailman3 aliases
```

### Test with a "testlist"

It would be very helpful to create a new testlist and check e-mail delivery setup before starting migration

```
$ mailman3 create -o admin@domain.example testlist@domain.example
$ echo "member@otherdomain.example" | mailman3 addmembers - testlist@domain.example
```

## Migration per list

Note: this works only for low-volume lists. For high-volume lists explicit temporary rejects must be configured in postfix during switchover otherwise there is a gap between creation of list (which turns active receiving on) and import of members.

### Retrieve owner of current list

```
# su - -s /bin/bash mailman
$ /usr/lib/mailman/bin/list_owners <LISTNAME>
<OWNER-EMAIL>
```

### Stopping delivery to mailman2 lists

 - enforce postfix to return only temporary errors
   - enable option `soft_bounce = yes` in `/etc/postfix/main.cf`
   - reload postfix `systemctl reload postfix`
 - disable catch of to-be-migrated list by
   - commenting related lines in
     - `/etc/mailman/aliases`
     - `/etc/mailman/virtual-mailman`
   - recreate databases
```
# postalias /etc/mailman/aliases
# postmap /etc/mailman/virtual-mailman
```

### Create list

```
# su - -s /bin/bash mailman3
$ mailman3 create --language <LANG> -n -o <OWNER-EMAIL> <LISTNAME>@<DOMAIN>
```

New list appears now
```
$ mailman3 lists -n
...
<LISTNAME>@<DOMAIN>
...
```

Note: short description can be set via WebUI now or later.

Following file should reflect new <LISTNAME>: /var/lib/mailman3/data/postfix_lmtp


### Add a test member to check delivery

```
$ echo "<TESTUSER>@<TESTDOMAIN>" | mailman3 addmembers - <LISTNAME>@<DOMAIN>
```

New member is listed now

```
$ mailman3 members <LISTNAME>@<DOMAIN>
<TESTUSER>@<TESTDOMAIN>
```

*Assure that delivery via "mailman2" is disabled, otherwise this test is distributed accross*

Send now e-mail to new list and check whether test will be distributed
 - `From: <TESTUSER>@<TESTDOMAIN>`
 - `To: <LISTNAME>@<DOMAIN>`

Send now e-mail to new list and check whether test will be held
 - `From: <OTHERUSER>@<TESTDOMAIN>`
 - `To: <LISTNAME>@<DOMAIN>`

In case all is working fine, remove test user

```
$ mailman3 delmembers -l <LISTNAME>@<DOMAIN> -m <TESTUSER>@<TESTDOMAIN>
```

List has no members anymore

```
$ mailman3 members <LISTNAME>@<DOMAIN>
<TESTUSER>@<TESTDOMAIN> has no members
```


### Import settings

Import settings from "mailman2"

``` 
$ mailman3 import21 <LISTNAME>@<DOMAIN> /var/lib/mailman/lists/<LISTNAME>/config.pck
importing members     [####################################]  100%
Importing owners      [####################################]  100%
Importing moderators  [####################################]  100%
Importing defers      [####################################]  100%
Importing holds       [####################################]  100%
Importing rejects     [####################################]  100%
Importing discards    [####################################]  100%
```

List members

```
$ mailman3 members <LISTNAME>@<DOMAIN>
...
```

### Import archive

#### Import archive from "mailman"

Example for *private* archive (otherwise use "public" instead of "private"

Attention: the passed tests from above will block import of older messages unless option `--since ...` is used, best is to delete the test message via WebUI in advance of mass import.

```
$ mailman3-web hyperkitty_import -l <LISTNAME>@<DOMAIN> /var/lib/mailman/archives/private/<LISTNAME>.mbox/<LISTNAME>.mbox
Importing from mbox file /var/lib/mailman/archive/private/<LISTNAME>.mbox/<LISTNAME>.mbox to <LISTNAME>@<DOMAIN>
Computing thread structure
Synchronizing properties with Mailman
25 emails left to refresh, checked 0
Warming up cache
The full-text search index is not updated for this list. It will not be updated by the 'minutely' incremental update job. To update the index for this list, run the Django admin command with arguments 'update_index_one_list list@domain.example'.
```

#### Update index on archive

```
$ mailman3-web update_index_one_list <LISTNAME>@<DOMAIN>
Indexing 12345 emails
```

### Disable list in "mailman2"

To disable but not trash a list instantly in "mailman2" best way is to move the related config directory away

```
# su - -s /bin/bash mailman
$ mkdir /var/lib/mailman/migrated3
$ mv /var/lib/mailman/lists/<LISTNAME> /var/lib/mailman/migrated3
```

### Disable postfix returining only temporary errors
 - disable of enforce postfix to return only temporary errors
   - disable option `soft_bounce = no` in `/etc/postfix/main.cf`

Reload postfix
```
systemctl reload postfix
```
