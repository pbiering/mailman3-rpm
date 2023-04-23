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

#### File_ /etc/postfix/main.cf

 - Check: recipient_delimiter
 - Extend: transport_maps
 - Extend: local_recipient_maps or virtual_alias_maps (depending on local setup)

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
$ mailman lists -n
```

### Grant mailman3 access to mailman2

Note: usually, directory permissions prevent mailman3 reading files of mailman2

```
# usermod -G mailman -a mailman3
```

Note: can be revoked after migration

## Pre-Migration

It would be very helpful to create a new testlist and check e-mail delivery setup before starting migration

```
$ mailman create -o admin@domain.example testlist@domain.example
```

## Migration per list

### Create list

```
$ mailman create -o admin@domain.example list@domain.example
$ echo "member@otherdomain.example" | mailman addmembers - testlist@domain.example
```

### Import settings

``` 
$ %mailman import21 list@domain.example /var/lib/mailman/lists/list/config.pck
mporting members     [####################################]  100%
Importing owners      [####################################]  100%
Importing moderators  [####################################]  100%
Importing defers      [####################################]  100%
Importing holds       [####################################]  100%
Importing rejects     [####################################]  100%
Importing discards    [####################################]  100%

```

### Import archive

```
mailman-web hyperkitty_import -l list@domain.example /var/lib/mailman/archive/public/list.mbox/list.mbox
Importing from mbox file /var/lib/mailman/archive/public/list.mbox/list.mbox to list@domain.example
Computing thread structure
Synchronizing properties with Mailman
25 emails left to refresh, checked 0
Warming up cache
The full-text search index is not updated for this list. It will not be updated by the 'minutely' incremental update job. To update the index for this list, run the Django admin command with arguments 'update_index_one_list list@domain.example'.
```

### Update index on archive

```
$ mailman-web update_index_one_list list@domain.example
Indexing 12345 emails
```
