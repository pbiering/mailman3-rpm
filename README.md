# mailman3-rpm

RPM packaged mailman3 for Fedora and Enterprise Linux

Until updated in Fedora and included by EPEL available via copr:

- https://copr.fedorainfracloud.org/coprs/pbiering/InternetServerExtensions/

## Background

Because of huge Python package dependencies it's impossible to build a native *mailman3* RPM without providing dependencies in USER_SITE directory. Neither EPEL nor Fedora can fulfill depencencies as of 2023-04.

### Drivers

- reproducable
  - identical version can be used in test and production
- no connection to PIP required during build and installation
  - should be anyhow avoided on productive systems
- ready-to-use
- enriched for CAPTCHA support

## Solution

### native build using USER_SITE

Package a native *mailman3* package, storing all dependencies in USER_SITE

### virtualenv build

Package a *virtualenv* setup of *mailman3* as described in https://docs.mailman3.org/en/latest/install/virtualenv.html#virtualenv-install into a RPM.

### Feature of the RPM

- SELinux policy
- CAPTCHA support already prepared (only site+secret key is required to be configured) for
  - reCaptcha
  - hCaptcha
  - FriendlyCaptcha
- database: SQLite
- systemd service & timer files for
  - mailman
  - mailman-web
- reverse proxy config file for Apache
- logrotate config

### Supported OS

| OS  | Method            |
|-----|-------------------|
| EL8 | native+virtualenv |
| EL9 | native+virtualenv |
| F37 | native+virtualenv |
| F38 | native+virtualenv |
| F39 | native+virtualenv |

## Usage

### Build RPM

*Recommended on a dedicated build host*

#### preparation

##### based on upstream/main

```
# clone repo
git clone https://github.com/pbiering/mailman3-rpm.git
# change into directory
cd mailman3-rpm
```

##### based on a published release

```
# fetch release package
wget https://github.com/pbiering/mailman3-rpm/archive/refs/tags/<VERSION>-<RELEASE>.tar.gz
# extract package
tar xzf mailman3-rpm-<VERSION>-<RELEASE>.tar.gz
# change into directory
cd mailman3-rpm-<VERSION>-<RELEASE>
```

#### install dependencies

##### as build user

Extract dependencies

```
rpmbuild -bb mailman3.spec 2>&1 | awk '$0 ~ "is needed" { print $1 }' | xargs echo "dnf install"
```

##### as system user

Install packages listed above

```
dnf install ...
```

#### create source RPM

create Source RPM by downloading external dependencies

```
rpmbuild -bs mailman3.spec --undefine=_disable_source_fetch --define "_topdir ." --define "_sourcedir ." --define "_srcrpmdir ."
```

or use the included Makefile

```
make srpm
```

#### build binary RPM

##### native build using USER_SITE

```
rpmbuild --rebuild ./mailman3-<VERSION>-<RELEASE>.<DIST>.src.rpm
```

or use the included Makefile

```
make rpm
```

### virtualenv build

```
rpmbuild --rebuild -D "mailman3_virtualenv 1" ./mailman3-<VERSION>-<RELEASE>.<DIST>.src.rpm
```

or use the included Makefile

```
make rpm-virtualenv
```


### Install RPM

Transfer RPM to final destination system and install (this will also resolve and install required dependencies)

#### native build

```
dnf localinstall mailman3-<VERSION>-<RELEASE>.<DIST>.<ARCH>.rpm
```

#### virtualenv build

```
dnf localinstall mailman3-virtualenv-<VERSION>-<RELEASE>.<DIST>.<ARCH>.rpm
```

#### via Fedora copr

Until updated in Fedora and included by EPEL available via copr:

- https://copr.fedorainfracloud.org/coprs/pbiering/InternetServerExtensions/


### Configuration

- check output of RPM after installation in general
- check main config file: `/etc/mailman.cfg`
- check additional config files in `/etc/mailman3/`
  - important: settings.py
- check configuration of `postfix`

General: read provided documentation on https://docs.mailman3.org/

## Features

### CAPTCHA support

CAPTCHA is injected into

| Package   | File                |
|-----------|---------------------|
| postorius | forms/list_forms.py |
| allauth   | account/forms.py    |

## Notes

- based on https://kojipkgs.fedoraproject.org//packages/mailman3/3.3.4/6.fc36/src/mailman3-3.3.4-6.fc36.src.rpm (last native one available)
- the SPEC file includes also toggles for
  - using cron files instead of systemd timers (-D "mailman3_cron 1")
  - use same user as mailman major version 2 (-D "mailman3_like_mailman2 1") THIS BREAKS COEXISTENT installation e.g. required for smooth transitions on same system hosting mailman major version 2 and 3 in parallel

## References

- https://koji.fedoraproject.org/koji/packageinfo?packageID=27808
- https://bugzilla.redhat.com/show_bug.cgi?id=2001801
- https://bugzilla.redhat.com/show_bug.cgi?id=2113503
- https://docs.mailman3.org/en/latest/install/virtualenv.html#virtualenv-install
