# mailman3-rpm

RPM packaged mailman3 for Fedora and Enterprise Linux

## Background

Because of huge Python package dependencies it's in 2023-04 impossible to build a native *mailman3* RPM without creating conflicts with already existing packages in OS like Fedora and Enterprise Linux.

### Drivers

- reproducable
  - identical version can be used in test and production
- no connection to PIP required
  - should be anyhow avoided on productive systems
- ready-to-use
- enriched for CAPTCHA support

## Solution

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

| OS  | Method     |
|-----|------------|
| EL8 | virtualenv |
| EL9 | virtualenv |
| F37 | virtualenv |
| F38 | virtualenv |

## Known issues with native builds

### All

- unable to inject CAPTCHA support into existing packages

| Package   | File                |
|-----------|---------------------|
| postorius | forms/list_forms.py |
| allauth   | account/forms.py    |

### Enterprise Linux

- missing a lot of of dependency packages in EPEL
- conflicts with base repo for
  - building required cmarkgfm >= 0.7.0 with existing python3-cffi == 1.14.5-5.el9@appstream

### Fedora

- missing some dependency packages in EPEL
- conflicts with base repo for

| Package      | Has                              |Requires|
|--------------|----------------------------------|--------|
| flufl-bounce | 3.0-17.fc37 <br/>3.0-18.fc38     | >= 4.0 |
| flufl-i18n   | 2.0.2-10.fc37 <br/>2.0.2-11.fc38 | >= 3.2 |

## Notes

- based on https://kojipkgs.fedoraproject.org//packages/mailman3/3.3.4/6.fc36/src/mailman3-3.3.4-6.fc36.src.rpm (last native one available)
- the SPEC file includes a toggle for activation of a native build by bundling missing packages but as described above it's impossible for EL and Fedora as of today because of final conflicts.

## References

- https://koji.fedoraproject.org/koji/packageinfo?packageID=27808
- https://bugzilla.redhat.com/show_bug.cgi?id=2001801
- https://bugzilla.redhat.com/show_bug.cgi?id=2113503