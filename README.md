# mailman3-rpm

RPM packaged mailman3 "enhanced" for Fedora and Enterprise Linux

Until included by EPEL and potentially adjustments are overtaken in Fedora available via copr:

- https://copr.fedorainfracloud.org/coprs/pbiering/InternetServerExtensions/

## Background

Because of huge Python package dependencies it's impossible to build a native *mailman3* RPM without providing dependencies in USER_SITE directory.
EPEL cannot fulfill dependencies as of 2023-06
Fedora has only a standard version packaged as of 2023-06 missing some important enhancements.

### Drivers

- reproducable
  - identical version can be used in test and production
- no connection to PIP required during build and installation
  - should be anyhow avoided on productive systems
- ready-to-use
- enriched for CAPTCHA support

## Solution

Package *mailman3* by storing all not fulfillable dependencies in USER_SITE.

### Feature of this RPM

- SELinux policy
- CAPTCHA support already prepared
  - Google's reCaptcha
  - hCaptcha
  - FriendlyCaptcha
- database: SQLite
- systemd service & timer files for
  - mailman
  - mailman-web
- reverse proxy config file for Apache
- logrotate config

### Supported OS

| OS  | Status |
|-----|--------|
| EL8 | ok     |
| EL9 | ok     |
| F37 | ok     |
| F38 | ok     |
| F39 | ok     |

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

```
rpmbuild --rebuild ./mailman3-<VERSION>-<RELEASE>.<DIST>.src.rpm
```

or use the included Makefile

```
make rpm
```


### Install RPM

Transfer RPM to final destination system and install (this will also resolve and install required dependencies)

```
dnf localinstall mailman3-enhanced-<VERSION>-<RELEASE>.<DIST>.<ARCH>.rpm
```

#### via Fedora copr

Until updated in Fedora and included by EPEL available via copr:

- https://copr.fedorainfracloud.org/coprs/pbiering/InternetServerExtensions/

```
dnf install mailman3-enhanced
```

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

| Package   | File(s)             |
|-----------|---------------------|
| postorius | forms/list_forms.py |
| allauth   | account/forms.py    |
| django    | contrib/admin/forms.py<br/>contrib/admin/templates/admin/login.html |

#### CAPTCHA configuration per service
CAPTCHA can be configured by editing options in  file `/etc/mailman3/settings.py`

 - Google's recaptcha: `RECAPTCHA_PUBLIC_KEY` + `RECAPTCHA_PRIVATE_KEY`
 - hCaptcha: `HCAPTCHA_SITEKEY` + `HCAPTCHA_SECRET`
 - FriendlyCaptcha: `FRC_CAPTCHA_SITE_KEY` + `FRC_CAPTCHA_SECRET`

Selection of configured service:

`CAPTCHA_SERVICE=recaptcha|hcaptcha|friendlycaptcha`

## Notes

- based on https://src.fedoraproject.org/rpms/mailman3/tree/rawhide

## References

- https://koji.fedoraproject.org/koji/packageinfo?packageID=27808
- https://bugzilla.redhat.com/show_bug.cgi?id=2001801
- https://bugzilla.redhat.com/show_bug.cgi?id=2113503
- https://src.fedoraproject.org/rpms/mailman3/tree/rawhide
- https://src.fedoraproject.org/rpms/mailman3
