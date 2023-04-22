### ***THIS IS A SPECIAL PACKAGE for mailman3
###
### see also:
###  - https://github.com/pbiering/mailman3-rpm
###  - description (below)
###
### Step 1: create source package by
###  BUNDLED-AS-REQUIRED PACKAGING (overload existing older versions if required by storing in USER_SITE)
###   download required packages and store to ~/rpmbuild/SOURCES
###   known required overloading see below defined: b_e_* / b_v_* (*b*undle_*e*nabled / *b*undle_*v*ersion))
###   $ rpmbuild -bp --undefine=_disable_source_fetch mailman3.spec
###
###  VIRTUALENV PACKAGING
###   according to https://docs.mailman3.org/en/latest/install/virtualenv.html#virtualenv-install
###   download main packages and dependencies and store to ~/rpmbuild/SOURCES
###   $ rpmbuild -bp --undefine=_disable_source_fetch -D "mailman3_virtualenv 1" mailman3.spec
###
### Step 2: install required build dependencies, get list of required packages
### $ rpmbuild -bb mailman3.spec 2>&1 | awk '$0 ~ "is needed" { print $1 }' | xargs echo "dnf install"
###
### Step 2: install required build dependencies, get list of required packages
### $ sudo dnf install ...
###
### Step 4: rebuild
### $ rpmbuild -bb mailman3.spec
###
### Build toggles
###  mailman3_like_mailman2 (default: 0): create package conflicting with mailman major version 2
###  mailman3_cron          (default: 0): package cron-jobs instead of systemd-timers
###  mailman3_virtualenv    (default: 0): virtualenv instead of native package

# do not create debug packages
%define debug_package %{nil}


## MAIN VERSIONS+RELEASE
%global version_mailman 			3.3.8
%global version_mailman_web			0.0.6
%global version_mailman_hyperkitty		1.2.1

%global release_token 8

## NAMES
%global pypi_name mailman
%global pname     mailman3


# toggle to create a with mailman version 2 non-conflicting package
%if 0%{?mailman3_like_mailman2}
%global mailman3_separated 0
%else
%global mailman3_separated 1
%endif

# toggle to cron files instead of systemd/service+timer
%if 0%{?mailman3_cron}
%global mailman3_cron 1
%else
%global mailman3_cron 0
%endif


### base dependencies

%if (0%{?rhel} == 8)
# hardwire to Python 3.9
%define 	python3_version_num	39
%define		python3_version		3.9
BuildRequires:  python%{python3_version_num}-devel
BuildRequires:  python%{python3_version_num}-setuptools
Requires:       python%{python3_version_num}
%else
# Enforce Python >= 3.9
%define		python3_version_num	3
#do not overwrite python3_version from rpm-macros
BuildRequires:  python3-devel >= 3.9
BuildRequires:  python3-setuptools
Requires:       python3 >= 3.9
%endif


%if 0%{?mailman3_virtualenv}
###  VIRTUALENV PACKAGING 
BuildRequires:  python%{python3_version_num}-pip
%endif


## VIRTUALENV + BUNDLED-AS-REQUIRED by EL+EPEL supported  requirements

# mandatory packages for mailman
%define	b_e_django_mailman3		1
%define	b_e_hyperkitty			1
%define	b_e_postorius			1

# mandatory packages for enabling CAPTCHA
%define	b_e_django_allauth		1
%define	b_e_django_recaptcha		1
%define	b_e_django_hcaptcha		1
%define	b_e_django_friendlycaptcha	1

%define	b_e_whoosh			1

%if (0%{?rhel} == 8)
# not available for EL == 8 -> bundle

%define	b_e_alembic			1
%define	b_e_atpublic			1
%define	b_e_attrs			1
%define	b_e_authres			1
%define	b_e_blessed			1
%define	b_e_cffi			1
%define	b_e_dateutil			1
%define	b_e_defusedxml			1
%define	b_e_flufl_lock			1
%define	b_e_greenlet			1
%define	b_e_isort			1
%define	b_e_jwt				1
%define	b_e_mailmanclient		1
%define	b_e_mako			1
%define	b_e_oauthlib			1
%define	b_e_passlib			1
%define	b_e_pytz			1
%define	b_e_rcssmin			1
%define	b_e_requests_oauthlib		1
%define	b_e_robot_detection		1
%define	b_e_sqlparse			1
%define	b_e_sqlalchemy			1
%define	b_e_tomli			1
%define	b_e_types_cryptography		1
%define	b_e_wcwidth			1
%define	b_e_zope_configuration		1
%define	b_e_zope_schema			1
%define	b_e_zope_i18nmessageid		1
%define	b_e_zope_component		1
%define	b_e_zope_event			1
%define	b_e_zope_hookable		1
%define	b_e_zope_interface		1

# end of rhel==8
%endif


%if 0%{?mailman3_virtualenv}
###  VIRTUALENV PACKAGING

## build dependencies
%define	b_e_cython			1
%define	b_e_packaging			1

# preinstalled will not work with PIP even in case: --system-site-packages
%define	b_e_setuptools			1
%define	b_e_setuptools_scm		1
%define	b_e_wheel			1

%if 0%{?rhel} == 8
%define	b_e_poetry_core			1
%define	b_e_flit_core			1
%endif

%if 0%{?rhel} >= 9
## build dependencies

# EL9 has 2.0.1 but not usable via PIP even in case: --system-site-packages
%define	b_e_tomli			1

%endif

%endif


%if 0%{?rhel} >= 8
# not available for EL >= 8 -> bundle

%define	b_e_arrow			1
%define	b_e_authheaders			1

# >= 3.5.2 required, 3.4.1-3.el9 is too low
%define	b_e_asgiref			1

%define	b_e_bleach			1

# superseed EL9 appstream
%define	b_e_cffi			1

%define	b_e_cmarkgfm			1
%define	b_e_dkimpy			1
%define	b_e_docutils			1
%define	b_e_falcon			1
%define	b_e_gunicorn			1
%define	b_e_lazr_config			1
%define	b_e_lazr_delegates		1
%define	b_e_mistune			1
%define	b_e_openid			1
%define	b_e_publicsuffix2		1
%define	b_e_pycparser			1
%define	b_e_pygments			1
%define	b_e_readme_renderer		1
%define	b_e_rjsmin			1
%define	b_e_typing_extensions		1
%define	b_e_webencodings		1
%define	b_e_zope_configuration		1
%define	b_e_zope_schema			1
%define	b_e_zope_i18nmessageid		1

## django dependencies
%define	b_e_django			1
%define	b_e_django_q			1
%define	b_e_django_compressor		1
%define	b_e_django_extensions		1
%define	b_e_django_gravatar2		1
%define	b_e_django_rest_framework	1
%define	b_e_django_appconf		1
%define	b_e_django_picklefield		1

# end of rhel>=8
%endif

%if (0%{?fedora} >= 37) || (0%{?rhel} >= 8)
## common for Fedora & EL
%define	b_e_importlib_resources		1

# even while available bundle to avoid install of huge dependencies
%define	b_e_networkx			1

%if (0%{?fedora} >= 37)

%if 0%{?mailman3_virtualenv}
# available 4.4.0-2.fc37 causes problems with VIRTUALENV/importlib_resources
%define	b_e_typing_extensions		1
# available 3.7.1-5.fc37 causes problems with VIRTUALENV/importlib_resources
%define	b_e_flit_core			1
%endif

%endif

%if (0%{?fedora} > 40)
# guessing that f40 will have updated versions...
%else
# >= 3.5.2 required, 3.4.1-7.fc37 / 3.4.1-8.fc38 is too low
%define	b_e_asgiref			1
# dependencies
%define	b_e_aiosmtpd			1
%define	b_e_flufl_bounce		1
%define	b_e_flufl_i18n			1

# Fedora provides 3.0 which is too low (see below)
%define	b_e_django_haystack		1
%endif

# end of fedora>=37 && rhel>=8
%endif


### Requirements

## Macros

# requirement conditional build-only without version
%define req_cond_b_o_n_v()  \
%if ! %1 \
BuildRequires:	python%{python3_version_num}-%2 \
%endif

# requirement conditional build+install without version
%define req_cond_b_i_n_v()  \
%if ! %1 \
BuildRequires:	python%{python3_version_num}-%2 \
Requires:	python%{python3_version_num}-%2 \
%endif

# requirement conditional build+install with version
%define req_cond_b_i_w_v()  \
%if ! %1 \
BuildRequires:	python%{python3_version_num}-%2 %3 %4 \
Requires:	python%{python3_version_num}-%2 %3 %4 \
%endif

# requirement conditional build+install with version and conflicts
%define req_cond_b_i_wcv()  \
%if ! %1 \
BuildRequires:	python%{python3_version_num}-%2 %3 %4 \
Requires:	python%{python3_version_num}-%2 %3 %4 \
%else \
BuildConflicts:	python%{python3_version_num}-%2 %5 %6 \
Conflicts:	python%{python3_version_num}-%2 %5 %6 \
%endif


### build-only related
%req_cond_b_o_n_v	1				rpm-macros

%req_cond_b_o_n_v	0%{?b_e_flit_core}		flit-core
%req_cond_b_o_n_v	0%{?b_e_setuptools}		setuptools
%req_cond_b_o_n_v	0%{?b_e_setuptools_scm}		setuptools_scm
%req_cond_b_o_n_v	0%{?b_e_wheel}			wheel

## Build dependencies
%if 0%{?b_e_cffi}
BuildRequires:	libffi-devel
%endif


### build+install related

%req_cond_b_i_w_v	0%{?b_e_aiosmtpd}		aiosmtpd >= 1.4.3
%req_cond_b_i_n_v	0%{?b_e_alembic}		alembic
%req_cond_b_i_w_v	0%{?b_e_asgiref}		asgiref >= 3.5.2
%req_cond_b_i_n_v	0%{?b_e_atpublic}		atpublic
%req_cond_b_i_n_v	0%{?b_e_attrs}			attrs
%req_cond_b_i_n_v	0%{?b_e_authres}		authres
%req_cond_b_i_w_v	0%{?b_e_authheaders}		authheaders >= 0.14.0
%req_cond_b_i_n_v	0%{?b_e_blessed}		blessed
%req_cond_b_i_n_v	0%{?b_e_dateutil}		dateutil
%req_cond_b_i_w_v	0%{?b_e_dkimpy}			dkimpy >= 0.7.1
%req_cond_b_i_w_v	0%{?b_e_django}			django >= 4
%req_cond_b_i_n_v	0%{?b_e_django_compressor}	django-compressor
%req_cond_b_i_w_v	0%{?b_e_django_extensions}	django-extensions >= 1.3.7
%req_cond_b_i_w_v	0%{?b_e_django_gravatar2}	django-gravatar2 >= 1.0.6

# f37/f38/f39: 3.0
# 3.0 has issue with django: cannot import name 'ungettext' from 'django.utils.translation' (BZ#2187604)
%req_cond_b_i_wcv	0%{?b_e_django_haystack}	django-haystack >= 3.2 < 3.2

%req_cond_b_i_n_v	0%{?b_e_django_q}		django-q
%req_cond_b_i_n_v	0%{?b_e_django_rest_framework}	django-rest-framework
%req_cond_b_i_w_v	0%{?b_e_falcon}			falcon >= 3.0.0

# f37/f38/f39: 3.0
%req_cond_b_i_w_v	0%{?b_e_flufl_bounce}		bounce >= 4.0

# f37/f38/f39: 2.0.2
%req_cond_b_i_w_v	0%{?b_e_flufl_i18n}		flufl-i18n >= 3.2

%req_cond_b_i_n_v	0%{?b_e_flufl_lock}		flufl-lock
%req_cond_b_i_n_v	0%{?b_e_gunicorn}		gunicorn
%req_cond_b_i_n_v	0%{?b_e_greenlet}		greenlet
%req_cond_b_i_n_v	0%{?b_e_isort}			isort
%req_cond_b_i_w_v	0%{?b_e_jwt}			jwt >= 1.7
%req_cond_b_i_n_v	0%{?b_e_lazr_config}		lazr-config
%req_cond_b_i_n_v	0%{?b_e_mako}			mako
%req_cond_b_i_n_v	0%{?b_e_mailmanclient}		mailmanclient
%req_cond_b_i_w_v	0%{?b_e_cmarkgfm}		cmarkgfm >= 0.8.0
%req_cond_b_i_n_v	0%{?b_e_mistune}		mistune
%req_cond_b_i_w_v	0%{?b_e_openid}			openid >= 3.0.8
%req_cond_b_i_n_v	0%{?b_e_passlib}		passlib
%req_cond_b_i_n_v	0%{?b_e_publicsuffix2}		publicsuffix2
%req_cond_b_i_n_v	0%{?b_e_pytz}			pytz
%req_cond_b_i_n_v	0%{?b_e_rcssmin}		rcssmin
%req_cond_b_i_n_v	0%{?b_e_readme_renderer}	readme-renderer
%req_cond_b_i_w_v	0%{?b_e_requests_oauthlib}	requests-oauthlib >= 0.3.0
%req_cond_b_i_n_v	0%{?b_e_robot_detection}	robot-detection
%req_cond_b_i_n_v	0%{?b_e_sqlalchemy}		sqlalchemy
%req_cond_b_i_n_v	0%{?b_e_sqlparse}		sqlparse
%req_cond_b_i_n_v	0%{?b_e_tomli}			tomli
%req_cond_b_i_n_v	0%{?b_e_typing_extensions}	typing-extensions
%req_cond_b_i_n_v	0%{?b_e_webencodings}		webencodings
%req_cond_b_i_n_v	0%{?b_e_whoosh}			whoosh
%req_cond_b_i_n_v	0%{?b_e_zope_component}		zope-component
%req_cond_b_i_n_v	0%{?b_e_zope_configuration}	zope-configuration
%req_cond_b_i_n_v	0%{?b_e_zope_event}		zope-event
%req_cond_b_i_n_v	0%{?b_e_zope_interface}		zope-interface
%req_cond_b_i_n_v	0%{?b_e_zope_hookable}		zope-hookable

## ALL supported OS versions
%req_cond_b_i_n_v	1				click
%req_cond_b_i_n_v	1				cryptography
%req_cond_b_i_n_v	1				dns
%req_cond_b_i_n_v	1				idna
%req_cond_b_i_n_v	1				markusafe
%req_cond_b_i_n_v	1				psutil
%req_cond_b_i_n_v	1				requests
%req_cond_b_i_n_v	1				six
%req_cond_b_i_n_v	1				toml
%req_cond_b_i_n_v	1				urllib3

# extra
BuildRequires: 	publicsuffix-list
Requires: 	publicsuffix-list


## VIRTUALENV+BUNDLED-AS-REQUIRED by EL+EPEL destination directories
%global basedir         /usr/lib/%{pname}
%global logdir          %{_localstatedir}/log/%{pname}
%global rundir          %{_rundir}/%{pname}
%global lockdir         %{_rundir}/lock/%{pname}
%global spooldir        %{_localstatedir}/spool/%{pname}
%global vardir          %{_localstatedir}/lib/%{pname}
%global etcdir          %{_sysconfdir}/%{pname}
%global sysconfdir      %{_sysconfdir}

%global builddir	%{_builddir}/%{pypi_name}-%{version_mailman}%{?prerelease}

%if 0%{?mailman3_virtualenv}
### VIRTUALENV PACKAGING 
%global virtualenvsubdir venv
%global bindir		%{basedir}/%{virtualenvsubdir}/bin
%global sitelibdir	%{basedir}/%{virtualenvsubdir}/lib64/python%{python3_version}/site-packages
%else
### BUNDLED-AS-REQUIRED PACKAGING 
%global bindir		   %{_libexecdir}/%{pname}
%global sitelibdir	   %{python3_sitelib}
%global sitearchdir	   %{python3_sitearch}
%define sitedirsub         /.local/lib/python%{python3_version}/site-packages
%global usersitedir	   %{basedir}%{sitedirsub}
%global sharedstatesitedir %{vardir}%{sitedirsub}
%endif

%global lmtpport        8024
# 8025 is default for aiosmtpd
%global webport         8026
%global restapiport     8027

## USER+GROUP
%if (0%{mailman3_separated} == 0)
# The user and group Mailman will run as, same as mailman 2 RPM (this create conflicts in parallel installation)
%global mmuser       mailman
%global mmuserid     41
%global mmgroup      mailman
%global mmgroupid    41
%else
# The user and group Mailman will run as, different values than mailman 2 RPM to enable parallel setup on one system
# user/group system id will be autogenerated by using -r
%global mmuser       mailman3
%global mmuserid     ""
%global mmgroup      mailman3
%global mmgroupid    ""
%endif


## BUNDLED DEPENDENCIES VERSIONS

#define	b_v_alembic			1.10.3 # typing_extensions/TypeGuard problem
%define	b_v_alembic			1.9.4

#define	b_v_atpublic		3.1.1 # >= 3.x has no setup.py
%define	b_v_atpublic		2.3

%define	b_v_attrs			22.2.0
%define	b_v_authres			1.2.0
%define	b_v_blessed			1.20.0
%define	b_v_certifi			2022.12.7
%define	b_v_charset_normalizer		3.1.0
%define	b_v_click			8.1.3
%define	b_v_cython			0.29.34
%define	b_v_cryptography		40.0.1
%define	b_v_dateutil			2.8.2
%define	b_v_defusedxml			0.7.1
%define	b_v_dnspython			2.3.0
%define	b_v_flit_core			3.8.0

#define	b_v_flufl_lock			7.1.1 # >= 7.x has no setup.py
%define	b_v_flufl_lock			6.0

%define	b_v_greenlet			2.0.2
%define	b_v_idna			3.4
%define	b_v_isort			5.12.0
%define	b_v_mako			1.2.4
%define	b_v_MarkupSafe			2.1.2
%define	b_v_networkx			3.0
%define	b_v_oauthlib			3.2.2
%define	b_v_openid			3.2.0
%define	b_v_packaging			23.0
%define	b_v_passlib			1.7.4
%define	b_v_pdm_pep517			1.1.3
%define	b_v_poetry_core			1.5.2
%define	b_v_psutil			5.9.4
%define	b_v_pycparser			2.21

#define	b_v_jwt				2.6.0 # conflicts on EL with python39-cryptography==3.3.1
%define	b_v_jwt				2.5.0

%define	b_v_pytz			2023.3
%define	b_v_rcssmin			1.1.1
%define	b_v_requests_oauthlib		1.3.1
#N2#define	b_v_redis			3.5.3
%define	b_v_robot_detection		0.4
#N2#define	b_v_semantic_version	2.10.0 
%define	b_v_setuptools			67.6.1
%define	b_v_setuptools_scm		7.1.0

#define	b_v_sqlalchemy			2.0.9 # EL8 problem typing_extensions/Concatenate
%define	b_v_sqlalchemy			1.4.47

%define	b_v_sqlparse			0.4.3

#define	b_v_tomli			2.0.1 # >= 2.x has no setup.py
#define	b_v_tomli			1.2.3 # >= 1.2.x has no setup.py
%define	b_v_tomli			1.1.0

#define	b_v_typing_extensions		4.5.0 # >= 4.x has no setup.py / 3.10.0.2 causes dataclass_transform dependency problems
#define	b_v_typing_extensions		3.10.0.2  # causes dataclass_transform dependency problems
%define	b_v_typing_extensions		3.7.4.3

%define	b_v_types_cryptography		3.3.23.2

%define	b_v_wcwidth			0.2.6
%define	b_v_webencodings		0.5.1

# 0.40.0 has issue on EL9 with flit_core
#define	b_v_wheel			0.40.0
%define	b_v_wheel			0.38.4

#N2#define	b_v_zipp			3.15.0

%define	b_v_zope_component		5.1.0
%define	b_v_zope_event			4.6
%define	b_v_zope_hookable		5.4
%define	b_v_zope_interface		6.0

%define	b_v_mailmanclient		3.3.5

## BUNDLED VERSIONS
# base
%define	b_v_postorius			1.3.8
%define	b_v_hyperkitty			1.3.7

# dependencies
%define	b_v_aiosmtpd			1.4.4.post2
%define	b_v_arrow			1.2.3
%define	b_v_asgiref			3.6.0
%define	b_v_authheaders			0.15.2
%define	b_v_bleach			6.0.0
%define	b_v_cffi                	1.15.1
%define	b_v_dkimpy			1.1.1
%define	b_v_docutils			0.19
%define	b_v_falcon			3.1.1
%define	b_v_flufl_bounce		4.0
%define	b_v_gunicorn			20.1.0
%define	b_v_lazr_config			2.2.3
%define	b_v_lazr_delegates		2.1.0
%define	b_v_mistune			2.0.5
%define	b_v_publicsuffix2		2.20191221
%define	b_v_pygments			2.14.0
%define	b_v_rjsmin			1.2.1
%define	b_v_whoosh			2.7.4

%define	b_v_zope_configuration		4.4.1
%define	b_v_zope_schema			7.0.1
%define	b_v_zope_i18nmessageid		6.0.1

%define	b_v_readme_renderer		37.3
%define	b_v_cmarkgfm			0.8.0

#define	b_v_flufl_i18n			4.1.1 # 4.x has no setup.py
%define	b_v_flufl_i18n			3.2

#define	b_v_importlib_resources		5.2.0 # 5.x has no setup.py
%define	b_v_importlib_resources		4.1.1

## django dependencies
%define	b_v_django			4.1.7
%define	b_v_django_allauth		0.54.0
%define	b_v_django_appconf		1.0.5
%define	b_v_django_compressor		4.3.1
%define	b_v_django_extensions		3.2.1
%define	b_v_django_gravatar2		1.4.4
%define	b_v_django_haystack		3.2.1
%define	b_v_django_picklefield		3.1
%define	b_v_django_rest_framework	3.14.0
%define	b_v_django_q			1.3.9

## django mailman related
%define	b_v_django_mailman3		1.3.9
%define	b_v_django_recaptcha		3.0.0
%define	b_v_django_hcaptcha		0.2.0
%define	b_v_django_friendlycaptcha	0.1.7


### HEADER
%if 0%{?mailman3_virtualenv}
###  VIRTUALENV PACKAGING 
Name:           %{pname}-virtualenv
Summary:        The GNU mailing list manager 3 (virtualenv edition)
%else
###  BUNDLED-AS-REQUIRED PACKAGING
Name:           %{pname}
Summary:        The GNU mailing list manager 3
%endif
Version:        %{version_mailman}%{?prerelease:~%{prerelease}}
Release:        %{release_token}%{?dist}

License:        GPLv3
URL:            https://www.mailman3.org/

Source1:        %{pname}.cfg
Source2:        %{pname}-tmpfiles.conf
Source3:        %{pname}.service
Source4:        %{pname}.logrotate
Source7:        %{pname}-gunicorn.conf.py
Source8:        %{pname}-django-settings.py
Source9:        %{pname}-web.service
Source11:       %{pname}-httpd.conf
Source13:       %{pname}-hyperkitty.cfg

# SELinux
Source90:	%{pname}.fc
Source91:	%{pname}.te

Source100:      %{__pypi_url}m/%{pypi_name}/%{pypi_name}-%{version_mailman}%{?prerelease}.tar.gz
Source101:	%{__pypi_url}m/%{pypi_name}-web/%{pypi_name}-web-%{version_mailman_web}.tar.gz
Source102:	%{__pypi_url}m/%{pypi_name}-hyperkitty/%{pypi_name}-hyperkitty-%{version_mailman_hyperkitty}.tar.gz

# cron jobs
Source200:	%{pname}.cron
Source201:	%{pname}-web.cron

# converted from mailman3.cron
Source300:	%{pname}-notify.service
Source301:	%{pname}-digests.service

Source310:	%{pname}-notify.timer
Source311:	%{pname}-digests.timer

# converted from mailman3-web.cron
Source400:	%{pname}-web-minutely.service
Source401:	%{pname}-web-quarter_hourly.service
Source402:	%{pname}-web-hourly.service
Source403:	%{pname}-web-daily.service
Source404:	%{pname}-web-weekly.service
Source405:	%{pname}-web-monthly.service
Source406:	%{pname}-web-yearly.service

Source410:	%{pname}-web-minutely.timer
Source411:	%{pname}-web-quarter_hourly.timer
Source412:	%{pname}-web-hourly.timer
Source413:	%{pname}-web-daily.timer
Source414:	%{pname}-web-weekly.timer
Source415:	%{pname}-web-monthly.timer
Source416:	%{pname}-web-yearly.timer

### COMMON PACKAGING
Source1000:	%{__pypi_url}p/postorius/postorius-%{b_v_postorius}.tar.gz
Source1001:	%{__pypi_url}H/HyperKitty/HyperKitty-%{b_v_hyperkitty}.tar.gz

Source1010:	%{__pypi_url}a/authheaders/authheaders-%{b_v_authheaders}.tar.gz
Source1011:	%{__pypi_url}l/lazr.config/lazr.config-%{b_v_lazr_config}.tar.gz
Source1012:	%{__pypi_url}l/lazr.delegates/lazr.delegates-%{b_v_lazr_delegates}.tar.gz
Source1013:	%{__pypi_url}a/aiosmtpd/aiosmtpd-%{b_v_aiosmtpd}.tar.gz
Source1014:	%{__pypi_url}f/falcon/falcon-%{b_v_falcon}.tar.gz
Source1015:	%{__pypi_url}d/dkimpy/dkimpy-%{b_v_dkimpy}.tar.gz
Source1016:	%{__pypi_url}m/mistune/mistune-%{b_v_mistune}.tar.gz
Source1017:	%{__pypi_url}r/readme_renderer/readme_renderer-%{b_v_readme_renderer}.tar.gz
Source1018:	%{__pypi_url}p/publicsuffix2/publicsuffix2-%{b_v_publicsuffix2}.tar.gz
Source1019:	%{__pypi_url}r/rjsmin/rjsmin-%{b_v_rjsmin}.tar.gz
Source1020:	%{__pypi_url}a/arrow/arrow-%{b_v_arrow}.tar.gz
Source1021:	%{__pypi_url}d/docutils/docutils-%{b_v_docutils}.tar.gz
Source1022:	%{__pypi_url}b/bleach/bleach-%{b_v_bleach}.tar.gz
Source1023:	%{__pypi_url}P/Pygments/Pygments-%{b_v_pygments}.tar.gz
Source1024:	%{__pypi_url}a/asgiref/asgiref-%{b_v_asgiref}.tar.gz
Source1025:	%{__pypi_url}f/flufl.bounce/flufl.bounce-%{b_v_flufl_bounce}.tar.gz
Source1026:	%{__pypi_url}f/flufl.i18n/flufl.i18n-%{b_v_flufl_i18n}.tar.gz
Source1027:	%{__pypi_url}W/Whoosh/Whoosh-%{b_v_whoosh}.tar.gz

Source1028:	%{__pypi_url}c/cmarkgfm/cmarkgfm-%{b_v_cmarkgfm}.tar.gz
Source1029:	%{__pypi_url}c/cffi/cffi-%{b_v_cffi}.tar.gz
Source1030:	%{__pypi_url}i/importlib_resources/importlib_resources-%{b_v_importlib_resources}.tar.gz
Source1031:	%{__pypi_url}g/gunicorn/gunicorn-%{b_v_gunicorn}.tar.gz

Source1040:	%{__pypi_url}z/zope.configuration/zope.configuration-%{b_v_zope_configuration}.tar.gz
Source1041:	%{__pypi_url}z/zope.schema/zope.schema-%{b_v_zope_schema}.tar.gz
Source1042:	%{__pypi_url}z/zope.i18nmessageid/zope.i18nmessageid-%{b_v_zope_i18nmessageid}.tar.gz

## django dependencies
Source1100:	%{__pypi_url}D/Django/Django-%{b_v_django}.tar.gz
Source1101:	%{__pypi_url}d/django-haystack/django-haystack-%{b_v_django_haystack}.tar.gz
Source1102:	%{__pypi_url}d/django-allauth/django-allauth-%{b_v_django_allauth}.tar.gz
Source1104:	%{__pypi_url}d/django-q/django-q-%{b_v_django_q}.tar.gz
Source1105:	%{__pypi_url}d/django_compressor/django_compressor-%{b_v_django_compressor}.tar.gz
Source1106:	%{__pypi_url}d/django-extensions/django-extensions-%{b_v_django_extensions}.tar.gz
Source1107:	%{__pypi_url}d/django-gravatar2/django-gravatar2-%{b_v_django_gravatar2}.tar.gz
Source1108:	%{__pypi_url}d/djangorestframework/djangorestframework-%{b_v_django_rest_framework}.tar.gz
Source1109:	%{__pypi_url}d/django-appconf/django-appconf-%{b_v_django_appconf}.tar.gz
Source1110:	%{__pypi_url}d/django-picklefield/django-picklefield-%{b_v_django_picklefield}.tar.gz

## django mailman related
Source1180:	%{__pypi_url}d/django-mailman3/django-mailman3-%{b_v_django_mailman3}.tar.gz
Source1190:	%{__pypi_url}d/django-recaptcha/django-recaptcha-%{b_v_django_recaptcha}.tar.gz
Source1191:	%{__pypi_url}d/django-hCaptcha/django-hCaptcha-%{b_v_django_hcaptcha}.tar.gz
Source1192:	%{__pypi_url}d/django-friendly-captcha/django-friendly-captcha-%{b_v_django_friendlycaptcha}.tar.gz

### VIRTUALENV PACKAGING
Source2009:	%{__pypi_url}C/Cython/Cython-%{b_v_cython}.tar.gz
Source2012:	%{__pypi_url}f/flit_core/flit_core-%{b_v_flit_core}.tar.gz

# networkx has too many dependencies if installed via RPM -> bundle
Source2019:	%{__pypi_url}n/networkx/networkx-%{b_v_networkx}.tar.gz

Source2021:	%{__pypi_url}p/packaging/packaging-%{b_v_packaging}.tar.gz
Source2024:	%{__pypi_url}p/poetry_core/poetry_core-%{b_v_poetry_core}.tar.gz
Source2026:	%{__pypi_url}p/pycparser/pycparser-%{b_v_pycparser}.tar.gz
Source2030:	%{__pypi_url}P/PyJWT/PyJWT-%{b_v_jwt}.tar.gz
#N2#Source2032:	#{__pypi_url}r/redis/redis-#{b_v_redis}.tar.gz
Source2036:	%{__pypi_url}s/setuptools/setuptools-%{b_v_setuptools}.tar.gz
Source2037:	%{__pypi_url}s/setuptools_scm/setuptools_scm-%{b_v_setuptools_scm}.tar.gz
#N2#Source2039:	#{__pypi_url}s/semantic_version/semantic_version-#{b_v_semantic_version}.tar.gz
Source2041:	%{__pypi_url}s/sqlparse/sqlparse-%{b_v_sqlparse}.tar.gz
Source2043:	%{__pypi_url}t/typing_extensions/typing_extensions-%{b_v_typing_extensions}.tar.gz
Source2046:	%{__pypi_url}w/wcwidth/wcwidth-%{b_v_wcwidth}.tar.gz
Source2047:	%{__pypi_url}w/webencodings/webencodings-%{b_v_webencodings}.tar.gz
Source2048:	%{__pypi_url}w/wheel/wheel-%{b_v_wheel}.tar.gz
#N2#Source2053:	#{__pypi_url}z/zipp/zipp-#{b_v_zipp}.tar.gz

# EL8
Source2000:	%{__pypi_url}a/alembic/alembic-%{b_v_alembic}.tar.gz
Source2001:	%{__pypi_url}a/atpublic/atpublic-%{b_v_atpublic}.tar.gz
Source2002:	%{__pypi_url}a/attrs/attrs-%{b_v_attrs}.tar.gz
Source2003:	%{__pypi_url}a/authres/authres-%{b_v_authres}.tar.gz
Source2004:	%{__pypi_url}b/blessed/blessed-%{b_v_blessed}.tar.gz
Source2005:	%{__pypi_url}c/certifi/certifi-%{b_v_certifi}.tar.gz
Source2006:	%{__pypi_url}c/charset-normalizer/charset-normalizer-%{b_v_charset_normalizer}.tar.gz
Source2010:	%{__pypi_url}d/defusedxml/defusedxml-%{b_v_defusedxml}.tar.gz
Source2013:	%{__pypi_url}f/flufl.lock/flufl.lock-%{b_v_flufl_lock}.tar.gz
Source2014:	%{__pypi_url}g/greenlet/greenlet-%{b_v_greenlet}.tar.gz
Source2016:	%{__pypi_url}i/isort/isort-%{b_v_isort}.tar.gz
Source2017:	%{__pypi_url}M/Mako/Mako-%{b_v_mako}.tar.gz
Source2020:	%{__pypi_url}o/oauthlib/oauthlib-%{b_v_oauthlib}.tar.gz
Source2022:	%{__pypi_url}p/passlib/passlib-%{b_v_passlib}.tar.gz
Source2023:	%{__pypi_url}p/pdm-pep517/pdm-pep517-%{b_v_pdm_pep517}.tar.gz
Source2027:	%{__pypi_url}p/python-dateutil/python-dateutil-%{b_v_dateutil}.tar.gz
Source2028:	%{__pypi_url}p/python3-openid/python3-openid-%{b_v_openid}.tar.gz
Source2029:	%{__pypi_url}p/pytz/pytz-%{b_v_pytz}.tar.gz
Source2031:	%{__pypi_url}r/rcssmin/rcssmin-%{b_v_rcssmin}.tar.gz
Source2034:	%{__pypi_url}r/requests-oauthlib/requests-oauthlib-%{b_v_requests_oauthlib}.tar.gz
Source2035:	%{__pypi_url}r/robot-detection/robot-detection-%{b_v_robot_detection}.tar.gz
Source2042:	%{__pypi_url}S/SQLAlchemy/SQLAlchemy-%{b_v_sqlalchemy}.tar.gz
Source2044:	%{__pypi_url}t/tomli/tomli-%{b_v_tomli}.tar.gz
Source2049:	%{__pypi_url}z/zope.component/zope.component-%{b_v_zope_component}.tar.gz
Source2050:	%{__pypi_url}z/zope.event/zope.event-%{b_v_zope_event}.tar.gz
Source2051:	%{__pypi_url}z/zope.hookable/zope.hookable-%{b_v_zope_hookable}.tar.gz
Source2052:	%{__pypi_url}z/zope.interface/zope.interface-%{b_v_zope_interface}.tar.gz
Source2055:	%{__pypi_url}t/types-cryptography/types-cryptography-%{b_v_types_cryptography}.tar.gz

Source2090:	%{__pypi_url}m/mailmanclient/mailmanclient-%{b_v_mailmanclient}.tar.gz

Patch3000:	mailman3-haystack-whoosh_backend-PR1870.patch
Patch3001:	mailman3-whoosh-whoosh3.patch

# CAPTCHA enabling patches
Patch901:	mailman3-postorius-list_forms.py-CAPTCHA.patch
Patch902:	mailman3-allauth-forms.py-CAPTCHA.patch


%if 0%{?mailman3_virtualenv}
### VIRTUALENV PACKAGING 

# conflict with non-virtualenv mailman3
Conflicts:	mailman3
BuildConflicts:	mailman3

# will be bundled, too many dependencies existing
BuildConflicts:	python%{python3_version_num}-networkx

%else
### BUNDLED-AS-REQUIRED PACKAGING 

## Arch adjustments
%define noarch 1
 
# has binary packages
%{?b_e_cmarkgfm:%define noarch 0}
%{?b_e_cffi:%define noarch 0}
%{?b_e_rjsmin:%define noarch 0}
%{?b_e_zope_hookable:%define noarch 0}
%{?b_e_zope_i18nmessageid:%define noarch 0}
%{?b_e_zope_interface:%define noarch 0}


# conflict with virtualenv mailman3
Conflicts:	mailman3-virtualenv

%endif

# conflict with mailman version 2 as long as sharing the same user
%if (0%{mailman3_separated} == 0)
Conflicts:	mailman
%endif


# SELinux https://fedoraproject.org/wiki/SELinux/IndependentPolicy#Creating_the_Spec_File
Provides:  %{pname}-selinux == %{version}-%{release}
%global selinux_variants mls targeted
Requires: selinux-policy >= %{_selinux_policy_version}
BuildRequires: pkgconfig(systemd)
BuildRequires: selinux-policy
BuildRequires: selinux-policy-devel
Requires(post): selinux-policy-base >= %{_selinux_policy_version}
Requires(post): libselinux-utils
Requires(post): policycoreutils

%if 0%{?fedora} || 0%{?rhel} >= 8
Requires(post): policycoreutils-python-utils
%else
Requires(post): policycoreutils-python
%endif

# SELinux https://fedoraproject.org/wiki/SELinux_Policy_Modules_Packaging_Draft
BuildRequires:  checkpolicy, selinux-policy-devel
BuildRequires:  hardlink

# Scriptlets
%{?systemd_requires}
BuildRequires:  systemd
Requires(pre):  shadow-utils

# httpd config for Web UI
BuildRequires:	httpd-devel
Requires:	httpd

# i18n
BuildRequires:	gettext

# CSS compilation
Requires:       sassc

# Webinterface
Requires:	httpd

# email system
Requires:	postfix

# html to plain text
Requires:	lynx

# password generator (postinstall)
Requires:	/usr/bin/uuidgen
Requires:	/usr/bin/md5sum
Requires:	/usr/bin/cut

# systemd ExecStartPost
Requires:	/usr/sbin/ss
Requires:	/usr/bin/timeout


## MACROS for prepare/build/install
%define get_source(n:) %{lua:
	n = tonumber(rpm.expand("%{-n:%{-n*}}"))
	for i, s in ipairs(source_nums) do
		if (n == s) then
			print(sources[i])
		end
	end
}

%define prep_cond() (\
echo "SETUP_COND: %1 %2"; \
if [ "%1" = "1" ]; then \
%if 0%{?mailman3_virtualenv} \
%{__cp} %{get_source -n %2} %{builddir}/pip \
%else \
%setup -q -T -a %2 -D -n %{builddir} \
%endif \
fi)

%define build_cond() (\
echo "BUILD_COND: %1 %2 %3"; \
if [ "%1" = "1" ]; then \
pushd %3-%2 || exit 1 \
%py3_build \
popd \
fi)

%define install_cond() (\
echo "INSTALL_COND: %1 %2 %3"; \
if [ "%1" = "1" ]; then \
pushd %3-%2 || exit 1 \
%py3_install \
popd \
fi)


%description
This is GNU Mailman, a mailing list management system distributed under the
terms of the GNU General Public License (GPL) version 3 or later.  The name of
this software is spelled 'Mailman' with a leading capital 'M' but with a lower
case second `m'.  Any other spelling is incorrect.
%if 0%{?mailman3_virtualenv}
* THIS IS A ALL-IN-ONE package containing Mailman 3 in Python "virtualenv" *
https://docs.mailman3.org/en/latest/install/virtualenv.html#virtualenv-install
%else
* THIS package contains Mailman 3 and all required but by OS not supported modules
 USER_SITE: %{usersitedir}
%endif
%if 0%{mailman3_separated}
* THIS package can coexist with Mailman 2
%else
* THIS package conflicts with Mailman 2
%endif
%if 0%{?mailman3_cron}
* THIS package contains scheduled tasks using: cron
%else
* THIS package contains scheduled tasks using: systemd.timer
%endif
user/group   : %{mmuser}/%{mmgroup}
directory    : %{basedir}/%{virtualenvsubdir}

it contains also
 mailman-web       : %{version_mailman_web} using 'gunicorn'
 mailman-hyperkitty: %{version_mailman_hyperkitty}

important forms are extended with CAPTCHA protection
 recaptcha hcaptcha friendlycaptcha

default configuration
 database: sqlite3
 indexer : whoosh
 CAPTCHA : NONE (requires custom secret+site key)
 
preconfigured ports (required for SELinux)
LMTP         : %{lmtpport}
REST-API     : %{restapiport}
Web Interface: %{webport}
%if 0%{?mailman3_virtualenv}
%else
%endif

%prep
rm -rf %{pypi_name}-%{version_mailman}
%{__mkdir} %{pypi_name}-%{version_mailman}
cd %{pypi_name}-%{version_mailman}

set +x
echo "*** BUILD INFORMATION ***"
%if 0%{?mailman3_virtualenv}
echo "** Packaging: VIRTUALENV"
%else
echo "** Packaging: BUNDLED-AS-REQUIRED"
%endif
%if 0%{mailman3_separated}
echo "** RPM: separate Mailman 3 from Mailman 2"
%else
echo "** RPM: Mailman 3 conflicts with Mailman 2"
%endif
%if 0%{?mailman3_cron}
echo "** Scheduled tasks: packaged using cron"
%else
echo "** Scheduled tasks: packaged using systemd.timer"
%endif
set -x

%if 0%{?mailman3_virtualenv}
### VIRTUALENV PACKAGING 
%{__mkdir} pip

# extract
%{__cp} %{SOURCE100} pip/
%{__cp} %{SOURCE101} pip/
%{__cp} %{SOURCE102} pip/

%else
### BUNDLED-AS-REQUIRED PACKAGING 

## base
%setup -T -D -a 100 -n %{builddir}
%setup -T -D -a 101 -n %{builddir}
%setup -T -D -a 102 -n %{builddir}

%endif

### ALL

## build/VIRTUALENV dependencies (no need to build/install)
%prep_cond "%{?b_e_cython}"                 2009
%prep_cond "%{?b_e_flit_core}"              2012
%prep_cond "%{?b_e_packaging}"              2021
%prep_cond "%{?b_e_poetry_core}"            2024
%prep_cond "%{?b_e_pycparser}"              2026
%prep_cond "%{?b_e_setuptools}"             2036
%prep_cond "%{?b_e_setuptools_scm}"         2037
%prep_cond "%{?b_e_wheel}"                  2048

## bundled packages
%prep_cond "%{?b_e_postorius}"              1000
%prep_cond "%{?b_e_hyperkitty}"             1001

## dependencies
%prep_cond "%{?b_e_authheaders}"            1010
%prep_cond "%{?b_e_lazr_config}"            1011
%prep_cond "%{?b_e_lazr_delegates}"         1012
%prep_cond "%{?b_e_aiosmtpd}"               1013
%prep_cond "%{?b_e_falcon}"                 1014
%prep_cond "%{?b_e_dkimpy}"                 1015
%prep_cond "%{?b_e_mistune}"                1016
%prep_cond "%{?b_e_readme_renderer}"        1017
%prep_cond "%{?b_e_publicsuffix2}"          1018
%prep_cond "%{?b_e_rjsmin}"                 1019
%prep_cond "%{?b_e_arrow}"                  1020
%prep_cond "%{?b_e_docutils}"               1021
%prep_cond "%{?b_e_bleach}"                 1022
%prep_cond "%{?b_e_pygments}"               1023
%prep_cond "%{?b_e_asgiref}"                1024
%prep_cond "%{?b_e_flufl_bounce}"           1025
%prep_cond "%{?b_e_flufl_i18n}"             1026
%prep_cond "%{?b_e_whoosh}"                 1027

%prep_cond "%{?b_e_cmarkgfm}"               1028
%prep_cond "%{?b_e_cffi}"                   1029
%prep_cond "%{?b_e_importlib_resources}"    1030
%prep_cond "%{?b_e_gunicorn}"               1031

%prep_cond "%{?b_e_zope_configuration}"     1040
%prep_cond "%{?b_e_zope_schema}"            1041
%prep_cond "%{?b_e_zope_i18nmessageid}"     1042

%prep_cond "%{?b_e_alembic}"                2000
%prep_cond "%{?b_e_atpublic}"               2001
%prep_cond "%{?b_e_attrs}"                  2002
%prep_cond "%{?b_e_authres}"                2003
%prep_cond "%{?b_e_blessed}"                2004
%prep_cond "%{?b_e_defusedxml}"             2010
%prep_cond "%{?b_e_flufl_lock}"             2013
%prep_cond "%{?b_e_greenlet}"               2014
%prep_cond "%{?b_e_isort}"                  2016
%prep_cond "%{?b_e_mako}"                   2017
%prep_cond "%{?b_e_networkx}"               2019
%prep_cond "%{?b_e_oauthlib}"               2020
%prep_cond "%{?b_e_passlib}"                2022
%prep_cond "%{?b_e_dateutil}"               2027
%prep_cond "%{?b_e_openid}"                 2028
%prep_cond "%{?b_e_pytz}"                   2029
%prep_cond "%{?b_e_jwt}"                    2030
%prep_cond "%{?b_e_rcssmin}"                2031
%prep_cond "%{?b_e_requests_oauthlib}"      2034
%prep_cond "%{?b_e_robot_detection}"        2035
%prep_cond "%{?b_e_sqlparse}"               2041
%prep_cond "%{?b_e_sqlalchemy}"             2042
%prep_cond "%{?b_e_typing_extensions}"      2043
%prep_cond "%{?b_e_tomli}"                  2044
%prep_cond "%{?b_e_wcwidth}"                2046
%prep_cond "%{?b_e_webencodings}"           2047
%prep_cond "%{?b_e_zope_component}"         2049
%prep_cond "%{?b_e_zope_event}"             2050
%prep_cond "%{?b_e_zope_hookable}"          2051
%prep_cond "%{?b_e_zope_interface}"         2052
%prep_cond "%{?b_e_types_cryptography}"     2055

%prep_cond "%{?b_e_mailmanclient}"          2090

## django dependencies
%prep_cond "%{?b_e_django}"                 1100
%prep_cond "%{?b_e_django_haystack}"        1101
%prep_cond "%{?b_e_django_allauth}"         1102
%prep_cond "%{?b_e_django_q}"               1104
%prep_cond "%{?b_e_django_compressor}"      1105
%prep_cond "%{?b_e_django_extensions}"      1106
%prep_cond "%{?b_e_django_gravatar2}"       1107
%prep_cond "%{?b_e_django_rest_framework}"  1108
%prep_cond "%{?b_e_django_appconf}"         1109
%prep_cond "%{?b_e_django_picklefield}"     1110

## django mailman related
%prep_cond "%{?b_e_django_mailman3}"        1180
%prep_cond "%{?b_e_django_recaptcha}"       1190
%prep_cond "%{?b_e_django_hcaptcha}"        1191
%prep_cond "%{?b_e_django_friendlycaptcha}" 1192


%if 0%{?mailman3_virtualenv}
### VIRTUALENV PACKAGING

%else
### BUNDLED-AS-REQUIRED PACKAGING

%endif

## SELinux
%{__mkdir} SELinux

%{__cp} %{SOURCE90} SELinux/%{pname}.fc
sed -i -e 's,@LOGDIR@,%{logdir},g;s,@BINDIR@,%{bindir},g;s,@BASEDIR@,%{basedir},g;s,@RUNDIR@,%{rundir},g;s,@VARDIR@,%{vardir},g;s,@SPOOLDIR@,%{spooldir},g;s,@ETCDIR@,%{etcdir},g;s,@LOCKDIR@,%{lockdir},g' SELinux/%{pname}.fc

%{__cp} %{SOURCE91} SELinux/%{pname}.te


%build
%if 0%{?mailman3_virtualenv}
### VIRTUALENV PACKAGING 
cd %{builddir}

%else
### BUNDLED-AS-REQUIRED PACKAGING

# will be all done in install section because of dependencies
%endif

cd SELinux
for selinuxvariant in %{selinux_variants}; do
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
  %{__mv} %{pname}.pp %{pname}.pp.${selinuxvariant}
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
done


%install
## directories
install -d -p %{buildroot}%{vardir}
install -d -p %{buildroot}%{spooldir}
install -d -p %{buildroot}%{logdir}
install -d -p %{buildroot}%{rundir}
install -d -p %{buildroot}%{lockdir}
install -d -p %{buildroot}%{basedir}
# Mailman will auto-create the following dir, but not with the correct group
# owner (MTAs such as Postfix must read and write to it). Set it here in RPM's
# file listing.
install -d -p %{buildroot}%{vardir}/data

# database directory (sqlite)
install -d -p %{buildroot}%{vardir}/db


%if 0%{?mailman3_virtualenv}
### VIRTUALENV PACKAGING 
## according to https://docs.mailman3.org/en/latest/install/virtualenv.html#virtualenv-install
cd %{builddir}

# create virtual environment
python%{python3_version} -m venv --system-site-packages %{buildroot}%{basedir}/%{virtualenvsubdir}

# activate virtual environment
source %{buildroot}%{bindir}/activate

PYTHONPATH=$PYTHONPATH:%{_buildroot}%{sitelibdir}/Django-%{?b_v_django}/build/lib
PYTHONPATH=$PYTHONPATH:%{_buildroot}%{sitelibdir}/asgiref-%{?b_v_asgiref}/build/lib
export PYTHONPATH

# install from local files basic support tools
%if 0%{?b_e_setuptools_scm}
pip%{python3_version} install --no-index --no-cache-dir --disable-pip-version-check --find-links %{builddir}/pip setuptools_scm
%endif

%if 0%{?b_e_wheel}
pip%{python3_version} install --no-index --no-cache-dir --disable-pip-version-check --find-links %{builddir}/pip wheel
%endif

%if 0%{?b_e_tomli}
pip%{python3_version} install --no-index --no-cache-dir --disable-pip-version-check --find-links %{builddir}/pip tomli
%endif

%if 0%{?b_e_isort}
pip%{python3_version} install --no-index --no-cache-dir --disable-pip-version-check --find-links %{builddir}/pip isort
%endif

# install from local files "base"
pip%{python3_version} install --no-index --no-cache-dir --disable-pip-version-check --find-links %{builddir}/pip %{pypi_name}

# install from local files "webinterface"
pip%{python3_version} install --no-index --no-cache-dir --disable-pip-version-check --find-links %{builddir}/pip %{pypi_name}-hyperkitty

# prerequisite (to avoid depencency issue during build of django-picklefield)
pip%{python3_version} install --no-index --no-cache-dir --disable-pip-version-check --find-links %{builddir}/pip django

pip%{python3_version} install --no-index --no-cache-dir --disable-pip-version-check --find-links %{builddir}/pip gunicorn
pip%{python3_version} install --no-index --no-cache-dir --disable-pip-version-check --find-links %{builddir}/pip sqlparse
pip%{python3_version} install --no-index --no-cache-dir --disable-pip-version-check --find-links %{builddir}/pip networkx

pip%{python3_version} install --no-index --no-cache-dir --disable-pip-version-check --find-links %{builddir}/pip %{pypi_name}-web

# search engine
pip%{python3_version} install --no-index --no-cache-dir --disable-pip-version-check --find-links %{builddir}/pip django-haystack

pip%{python3_version} install --no-index --no-cache-dir --disable-pip-version-check --find-links %{builddir}/pip Whoosh

# install from local files "CAPTCHA"
pip%{python3_version} install --no-index --no-cache-dir --disable-pip-version-check --find-links %{builddir}/pip django-recaptcha
pip%{python3_version} install --no-index --no-cache-dir --disable-pip-version-check --find-links %{builddir}/pip django-hcaptcha
pip%{python3_version} install --no-index --no-cache-dir --disable-pip-version-check --find-links %{builddir}/pip django-friendly-captcha

## remove all python cache files
find %{buildroot} -name '*.pyc' | xargs rm -rf
find %{buildroot} -name '__pycache__' | xargs rm -rf

# remove all exe files
find %{buildroot} -iname '*.exe' | xargs rm -f

# disable RemovedInDjango30Warning
grep --include='*.py' -l -r "^from django.utils.deprecation import RemovedInDjango30Warning" %{buildroot}%{basedir}/%{virtualenvsubdir} | while read file; do
	sed -i -e 's,^\(from django.utils.deprecation import RemovedInDjango30Warning\),#DISABLED-BY-RPMBUILD# \1,g' $file
done

# remove all buildroot references
grep '%{buildroot}' %{buildroot}/* -r -l 2>/dev/null | while read file; do
	sed -i -e 's,%{buildroot},,g' $file
done

# compile all python modules
%if (%{python3_pkgversion} >= 30) && (%{python3_pkgversion} < 39)
# < 3.9 is not supporting -s)
%else
python%{python3_version} -m compileall -q -s %{buildroot} %{buildroot}%{basedir}/%{virtualenvsubdir}
%endif

# "mailman-web compilemessages" is prevented to run later because of read-only file/dir in package
set +x
echo "BEGIN: msgfmt/po->mo"
find %{buildroot}%{basedir} -type f -name '*.po' | while read pofile; do
	mofile="${pofile/.po/.mo}"
	if [ ! -f $mofile -o $pofile -nt $mofile ]; then
		msgfmt $pofile -o $mofile
	fi
done
echo "END  : msgfmt/po->mo"
set -x

# enable virtualenv by default for user
echo 'source %{bindir}/activate' >> %{buildroot}%{vardir}/.bash_profile

%else
### BUNDLED-AS-REQUIRED PACKAGING

## precondition (build+install)
%build_cond   "%{?b_e_wheel}"          "%{?b_v_wheel}"          wheel
%install_cond "%{?b_e_wheel}"          "%{?b_v_wheel}"          wheel

%build_cond   "%{?b_e_setuptools_scm}" "%{?b_v_setuptools_scm}" setuptools_scm
%install_cond "%{?b_e_setuptools_scm}" "%{?b_v_setuptools_scm}" setuptools_scm

%build_cond   "%{?b_e_tomli}"          "%{?b_v_tomli}"          tomli
%install_cond "%{?b_e_tomli}"          "%{?b_v_tomli}"          tomli

%build_cond   "%{?b_e_cffi}"           "%{?b_v_cffi}"           cffi
%install_cond "%{?b_e_cffi}"           "%{?b_v_cffi}"           cffi

%build_cond   "%{?b_e_isort}"          "%{?b_v_isort}"          isort
%install_cond "%{?b_e_isort}"          "%{?b_v_isort}"          isort

PYTHONPATH=$PYTHONPATH:%{buildroot}%{sitelibdir}:%{buildroot}%{sitearchdir}
export PYTHONPATH
echo "PYTHONPATH=$PYTHONPATH"

## base
pushd %{pypi_name}-%{version_mailman}%{?prerelease}
%py3_build
popd

pushd %{pypi_name}-web-%{version_mailman_web}
%py3_build
popd

pushd %{pypi_name}-hyperkitty-%{version_mailman_hyperkitty}
%py3_build
popd

## bundled packages
%build_cond "%{?b_e_postorius}"              "%{?b_v_postorius}"              postorius
%build_cond "%{?b_e_hyperkitty}"             "%{?b_v_hyperkitty}"             HyperKitty

## dependencies
%build_cond "%{?b_e_aiosmtpd}"               "%{?b_v_aiosmtpd}"               aiosmtpd
%build_cond "%{?b_e_alembic}"                "%{?b_v_alembic}"                alembic
%build_cond "%{?b_e_arrow}"                  "%{?b_v_arrow}"                  arrow
%build_cond "%{?b_e_atpublic}"               "%{?b_v_atpublic}"               atpublic
%build_cond "%{?b_e_attrs}"                  "%{?b_v_attrs}"                  attrs
%build_cond "%{?b_e_asgiref}"                "%{?b_v_asgiref}"                asgiref
%build_cond "%{?b_e_authheaders}"            "%{?b_v_authheaders}"            authheaders
%build_cond "%{?b_e_authres}"                "%{?b_v_authres}"                authres
%build_cond "%{?b_e_bleach}"                 "%{?b_v_bleach}"                 bleach
%build_cond "%{?b_e_blessed}"                "%{?b_v_blessed}"                blessed
%build_cond "%{?b_e_dateutil}"               "%{?b_v_dateutil}"               python-dateutil
%build_cond "%{?b_e_defusedxml}"             "%{?b_v_defusedxml}"             defusedxml
%build_cond "%{?b_e_cmarkgfm}"               "%{?b_v_cmarkgfm}"               cmarkgfm
%build_cond "%{?b_e_dkimpy}"                 "%{?b_v_dkimpy}"                 dkimpy
%build_cond "%{?b_e_docutils}"               "%{?b_v_docutils}"               docutils
%build_cond "%{?b_e_falcon}"                 "%{?b_v_falcon}"                 falcon
%build_cond "%{?b_e_flufl_i18n}"             "%{?b_v_flufl_i18n}"             flufl.i18n
%build_cond "%{?b_e_flufl_bounce}"           "%{?b_v_flufl_bounce}"           flufl.bounce
%build_cond "%{?b_e_flufl_lock}"             "%{?b_v_flufl_lock}"             flufl.lock
%build_cond "%{?b_e_greenlet}"               "%{?b_v_greenlet}"               greenlet
%build_cond "%{?b_e_gunicorn}"               "%{?b_v_gunicorn}"               gunicorn
%build_cond "%{?b_e_importlib_resources}"    "%{?b_v_importlib_resources}"    importlib_resources
%build_cond "%{?b_e_jwt}"                    "%{?b_v_jwt}"                    PyJWT
%build_cond "%{?b_e_lazr_config}"            "%{?b_v_lazr_config}"            lazr.config
%build_cond "%{?b_e_lazr_delegates}"         "%{?b_v_lazr_delegates}"         lazr.delegates
%build_cond "%{?b_e_mako}"                   "%{?b_v_mako}"                   Mako
%build_cond "%{?b_e_mailmanclient}"          "%{?b_v_mailmanclient}"          mailmanclient
%build_cond "%{?b_e_mistune}"                "%{?b_v_mistune}"                mistune
%build_cond "%{?b_e_networkx}"               "%{?b_v_networkx}"               networkx
%build_cond "%{?b_e_oauthlib}"               "%{?b_v_oauthlib}"               oauthlib
%build_cond "%{?b_e_openid}"                 "%{?b_v_openid}"                 python3-openid
%build_cond "%{?b_e_passlib}"                "%{?b_v_passlib}"                passlib
%build_cond "%{?b_e_publicsuffix2}"          "%{?b_v_publicsuffix2}"          publicsuffix2
%build_cond "%{?b_e_pytz}"                   "%{?b_v_pytz}"                   pytz
%build_cond "%{?b_e_rcssmin}"                "%{?b_v_rcssmin}"                rcssmin
%build_cond "%{?b_e_readme_renderer}"        "%{?b_v_readme_renderer}"        readme_renderer
%build_cond "%{?b_e_requests_oauthlib}"      "%{?b_v_requests_oauthlib}"      requests-oauthlib
%build_cond "%{?b_e_rjsmin}"                 "%{?b_v_rjsmin}"                 rjsmin
%build_cond "%{?b_e_robot_detection}"        "%{?b_v_robot_detection}"        robot-detection
%build_cond "%{?b_e_pygments}"               "%{?b_v_pygments}"               Pygments
%build_cond "%{?b_e_sqlparse}"               "%{?b_v_sqlparse}"               sqlparse
%build_cond "%{?b_e_sqlalchemy}"             "%{?b_v_sqlalchemy}"             SQLAlchemy
%build_cond "%{?b_e_types_cryptography}"     "%{?b_v_types_cryptography}"     types-cryptography
%build_cond "%{?b_e_typing_extensions}"      "%{?b_v_typing_extensions}"      typing_extensions
%build_cond "%{?b_e_wcwidth}"                "%{?b_v_wcwidth}"                wcwidth
%build_cond "%{?b_e_webencodings}"           "%{?b_v_webencodings}"           webencodings
%build_cond "%{?b_e_whoosh}"                 "%{?b_v_whoosh}"                 Whoosh

%build_cond "%{?b_e_zope_configuration}"     "%{?b_v_zope_configuration}"     zope.configuration
%build_cond "%{?b_e_zope_schema}"            "%{?b_v_zope_schema}"            zope.schema
%build_cond "%{?b_e_zope_i18nmessageid}"     "%{?b_v_zope_i18nmessageid}"     zope.i18nmessageid
%build_cond "%{?b_e_zope_component}"         "%{?b_v_zope_component}"         zope.component
%build_cond "%{?b_e_zope_event}"             "%{?b_v_zope_event}"             zope.event
%build_cond "%{?b_e_zope_hookable}"          "%{?b_v_zope_hookable}"          zope.hookable
%build_cond "%{?b_e_zope_interface}"         "%{?b_v_zope_interface}"         zope.interface

## django dependencies
%build_cond "%{?b_e_django}"                 "%{?b_v_django}"                 Django
%build_cond "%{?b_e_django_allauth}"         "%{?b_v_django_allauth}"         django-allauth
%build_cond "%{?b_e_django_appconf}"         "%{?b_v_django_appconf}"         django-appconf
%build_cond "%{?b_e_django_compressor}"      "%{?b_v_django_compressor}"      django_compressor
%build_cond "%{?b_e_django_extensions}"      "%{?b_v_django_extensions}"      django-extensions
%build_cond "%{?b_e_django_gravatar2}"       "%{?b_v_django_gravatar2}"       django-gravatar2
%build_cond "%{?b_e_django_haystack}"        "%{?b_v_django_haystack}"        django-haystack
%build_cond "%{?b_e_django_q}"               "%{?b_v_django_q}"               django-q
%build_cond "%{?b_e_django_rest_framework}"  "%{?b_v_django_rest_framework}"  djangorestframework

# django-picklefield depends on django
PYTHONPATH=$PYTHONPATH:%{_builddir}/%{pypi_name}-%{version_mailman}%{?prerelease}/Django-%{?b_v_django}/build/lib
PYTHONPATH=$PYTHONPATH:%{_builddir}/%{pypi_name}-%{version_mailman}%{?prerelease}/asgiref-%{?b_v_asgiref}/build/lib
export PYTHONPATH
%build_cond "%{?b_e_django_picklefield}"     "%{?b_v_django_picklefield}"     django-picklefield

## django mailman related
%build_cond "%{?b_e_django_mailman3}"        "%{?b_v_django_mailman3}"        django-mailman3
%build_cond "%{?b_e_django_recaptcha}"       "%{?b_v_django_recaptcha}"       django-recaptcha
%build_cond "%{?b_e_django_hcaptcha}"        "%{?b_v_django_hcaptcha}"        django-hCaptcha
%build_cond "%{?b_e_django_friendlycaptcha}" "%{?b_v_django_friendlycaptcha}" django-friendly-captcha


PYTHONPATH=$PYTHONPATH:%{buildroot}%{sitelibdir}:%{buildroot}%{sitearchdir}
export PYTHONPATH
echo "PYTHONPATH=$PYTHONPATH"

pushd %{pypi_name}-%{version_mailman}%{?prerelease}
%py3_install
popd

pushd %{pypi_name}-web-%{version_mailman_web}
%py3_install
popd

pushd %{pypi_name}-hyperkitty-%{version_mailman_hyperkitty}
%py3_install
popd

## bundled packages
%install_cond "%{?b_e_postorius}"              "%{?b_v_postorius}"              postorius
%install_cond "%{?b_e_hyperkitty}"             "%{?b_v_hyperkitty}"             HyperKitty

## dependencies
%install_cond "%{?b_e_aiosmtpd}"               "%{?b_v_aiosmtpd}"               aiosmtpd
%install_cond "%{?b_e_alembic}"                "%{?b_v_alembic}"                alembic
%install_cond "%{?b_e_arrow}"                  "%{?b_v_arrow}"                  arrow
%install_cond "%{?b_e_asgiref}"                "%{?b_v_asgiref}"                asgiref
%install_cond "%{?b_e_atpublic}"               "%{?b_v_atpublic}"               atpublic
%install_cond "%{?b_e_attrs}"                  "%{?b_v_attrs}"                  attrs
%install_cond "%{?b_e_authheaders}"            "%{?b_v_authheaders}"            authheaders
%install_cond "%{?b_e_authres}"                "%{?b_v_authres}"                authres
%install_cond "%{?b_e_bleach}"                 "%{?b_v_bleach}"                 bleach
%install_cond "%{?b_e_blessed}"                "%{?b_v_blessed}"                blessed
%install_cond "%{?b_e_cffi}"                   "%{?b_v_cffi}"                   cffi
%install_cond "%{?b_e_cmarkgfm}"               "%{?b_v_cmarkgfm}"               cmarkgfm
%install_cond "%{?b_e_dateutil}"               "%{?b_v_dateutil}"               python-dateutil
%install_cond "%{?b_e_defusedxml}"             "%{?b_v_defusedxml}"             defusedxml
%install_cond "%{?b_e_dkimpy}"                 "%{?b_v_dkimpy}"                 dkimpy
%install_cond "%{?b_e_docutils}"               "%{?b_v_docutils}"               docutils
%install_cond "%{?b_e_falcon}"                 "%{?b_v_falcon}"                 falcon
%install_cond "%{?b_e_flufl_bounce}"           "%{?b_v_flufl_bounce}"           flufl.bounce
%install_cond "%{?b_e_flufl_i18n}"             "%{?b_v_flufl_i18n}"             flufl.i18n
%install_cond "%{?b_e_flufl_lock}"             "%{?b_v_flufl_lock}"             flufl.lock
%install_cond "%{?b_e_gunicorn}"               "%{?b_v_gunicorn}"               gunicorn
%install_cond "%{?b_e_greenlet}"               "%{?b_v_greenlet}"               greenlet
%install_cond "%{?b_e_importlib_resources}"    "%{?b_v_importlib_resources}"    importlib_resources
%install_cond "%{?b_e_jwt}"                    "%{?b_v_jwt}"                    PyJWT
%install_cond "%{?b_e_lazr_config}"            "%{?b_v_lazr_config}"            lazr.config
%install_cond "%{?b_e_lazr_delegates}"         "%{?b_v_lazr_delegates}"         lazr.delegates
%install_cond "%{?b_e_mako}"                   "%{?b_v_mako}"                   Mako
%install_cond "%{?b_e_mailmanclient}"          "%{?b_v_mailmanclient}"          mailmanclient
%install_cond "%{?b_e_mistune}"                "%{?b_v_mistune}"                mistune
%install_cond "%{?b_e_networkx}"               "%{?b_v_networkx}"               networkx
%install_cond "%{?b_e_oauthlib}"               "%{?b_v_oauthlib}"               oauthlib
%install_cond "%{?b_e_openid}"                 "%{?b_v_openid}"                 python3-openid
%install_cond "%{?b_e_passlib}"                "%{?b_v_passlib}"                passlib
%install_cond "%{?b_e_publicsuffix2}"          "%{?b_v_publicsuffix2}"          publicsuffix2
%install_cond "%{?b_e_pygments}"               "%{?b_v_pygments}"               Pygments
%install_cond "%{?b_e_pytz}"                   "%{?b_v_pytz}"                   pytz
%install_cond "%{?b_e_readme_renderer}"        "%{?b_v_readme_renderer}"        readme_renderer
%install_cond "%{?b_e_requests_oauthlib}"      "%{?b_v_requests_oauthlib}"      requests-oauthlib
%install_cond "%{?b_e_rcssmin}"                "%{?b_v_rcssmin}"                rcssmin
%install_cond "%{?b_e_rjsmin}"                 "%{?b_v_rjsmin}"                 rjsmin
%install_cond "%{?b_e_robot_detection}"        "%{?b_v_robot_detection}"        robot-detection
%install_cond "%{?b_e_sqlparse}"               "%{?b_v_sqlparse}"               sqlparse
%install_cond "%{?b_e_sqlalchemy}"             "%{?b_v_sqlalchemy}"             SQLAlchemy
%install_cond "%{?b_e_types_cryptography}"     "%{?b_v_types_cryptography}"     types-cryptography
%install_cond "%{?b_e_typing_extensions}"      "%{?b_v_typing_extensions}"      typing_extensions
%install_cond "%{?b_e_wcwidth}"                "%{?b_v_wcwidth}"                wcwidth
%install_cond "%{?b_e_webencodings}"           "%{?b_v_webencodings}"           webencodings
%install_cond "%{?b_e_whoosh}"                 "%{?b_v_whoosh}"                 Whoosh

%install_cond "%{?b_e_zope_component}"         "%{?b_v_zope_component}"         zope.component
%install_cond "%{?b_e_zope_configuration}"     "%{?b_v_zope_configuration}"     zope.configuration
%install_cond "%{?b_e_zope_event}"             "%{?b_v_zope_event}"             zope.event
%install_cond "%{?b_e_zope_i18nmessageid}"     "%{?b_v_zope_i18nmessageid}"     zope.i18nmessageid
%install_cond "%{?b_e_zope_interface}"         "%{?b_v_zope_interface}"         zope.interface
%install_cond "%{?b_e_zope_hookable}"          "%{?b_v_zope_hookable}"          zope.hookable
%install_cond "%{?b_e_zope_schema}"            "%{?b_v_zope_schema}"            zope.schema

## django* dependencies
%install_cond "%{?b_e_django}"                 "%{?b_v_django}"                 Django
%install_cond "%{?b_e_django_allauth}"         "%{?b_v_django_allauth}"         django-allauth
%install_cond "%{?b_e_django_appconf}"         "%{?b_v_django_appconf}"         django-appconf
%install_cond "%{?b_e_django_compressor}"      "%{?b_v_django_compressor}"      django_compressor
%install_cond "%{?b_e_django_extensions}"      "%{?b_v_django_extensions}"      django-extensions
%install_cond "%{?b_e_django_gravatar2}"       "%{?b_v_django_gravatar2}"       django-gravatar2
%install_cond "%{?b_e_django_haystack}"        "%{?b_v_django_haystack}"        django-haystack
%install_cond "%{?b_e_django_q}"               "%{?b_v_django_q}"               django-q
%install_cond "%{?b_e_django_rest_framework}"  "%{?b_v_django_rest_framework}"  djangorestframework

# django-picklefield depends on django
PYTHONPATH=$PYTHONPATH:%{_builddir}/%{pypi_name}-%{version_mailman}%{?prerelease}/Django-%{?b_v_django}/build/lib
PYTHONPATH=$PYTHONPATH:%{_builddir}/%{pypi_name}-%{version_mailman}%{?prerelease}/asgiref-%{?b_v_asgiref}/build/lib
export PYTHONPATH
%install_cond "%{?b_e_django_picklefield}"     "%{?b_v_django_picklefield}"     django-picklefield

## django mailman related
%install_cond "%{?b_e_django_mailman3}"        "%{?b_v_django_mailman3}"        django-mailman3
%install_cond "%{?b_e_django_recaptcha}"       "%{?b_v_django_recaptcha}"       django-recaptcha
%install_cond "%{?b_e_django_hcaptcha}"        "%{?b_v_django_hcaptcha}"        django-hCaptcha
%install_cond "%{?b_e_django_friendlycaptcha}" "%{?b_v_django_friendlycaptcha}" django-friendly-captcha

# cleanup doc files of bundled packages
%{__rm} -rf %{buildroot}%{_docdir}/*

# move scripts away from _bindir to avoid conflicts and create a wrapper scripts
install -d -p %{buildroot}%{bindir}
%{__mv} %{buildroot}%{_bindir}/* %{buildroot}%{bindir}

for wrapper in mailman mailman-web; do
	cat > %{buildroot}%{_bindir}/$wrapper << EOF
#!/bin/sh
if [ "\$(whoami)" != "%{mmuser}" ]; then
    echo "This command must be run under the mailman user (%{mmuser})."
    exit 1
fi
%{bindir}/$wrapper \$@
EOF

done

%endif

# apply comsetic patches
%if 0%{?b_e_django_haystack}
if [ -f %{buildroot}%{sitelibdir}/haystack/backends/whoosh_backend.py ]; then
cat %{PATCH3000} | patch %{buildroot}%{sitelibdir}/haystack/backends/whoosh_backend.py
fi
%endif

%if 0%{?b_e_whoosh}
if [ -f %{buildroot}%{sitelibdir}/whoosh/codec/whoosh3.py ]; then
cat %{PATCH3001} | patch %{buildroot}%{sitelibdir}/whoosh/codec/whoosh3.py
fi
%endif

# CAPTCHA extension patches
cat %{PATCH901} | patch %{buildroot}%{sitelibdir}/postorius/forms/list_forms.py
cat %{PATCH902} | patch %{buildroot}%{sitelibdir}/allauth/account/forms.py

# enforce "python" to "python3"
grep --include='*.py' --include='*.py-tpl' -l -r "env python$" %{buildroot}%{sitelibdir} | while read file; do
	sed -i -e 's,env python$,env python3,g' $file
done

# replace dedicated installed file with softlink to publicsuffix-list (see also python-publicsuffix2.spec)
find %{buildroot}%{sitelibdir} -type f -name public_suffix_list.dat | while read f; do
	echo "replace dedicated installed files with softlink: $f"
	rm $f
	ln -s %{_datarootdir}/publicsuffix/public_suffix_list.dat $f
done


%if 0%{?mailman3_virtualenv}
### VIRTUALENV PACKAGING 

%else
### BUNDLED-AS-REQUIRED PACKAGING

## move installed site-package to USER_SITE

# create USER_SITE directory
install -d -p  %{buildroot}%{dirname:%{sharedstatesitedir}}

# create destination for USER_SITE
install -d -p %{buildroot}%{usersitedir}

# create softlink to bundled modules
ln -s %{usersitedir} %{buildroot}%{sharedstatesitedir}

# move noarch
for f in %{buildroot}%{sitelibdir}/*; do
	%{__mv} $f %{buildroot}%{usersitedir}/
done

# move arch dependent
for f in %{buildroot}%{sitearchdir}/*; do
	entry=$(basename "$f")
	if [ ! -d %{buildroot}%{usersitedir}/$entry ]; then
		# directory not exiting
		%{__mv} $f %{buildroot}%{usersitedir}/
	else
		if [ -d $f ]; then
			# directory exiting, move subdirectories only
			for s in $f/*; do
				%{__mv} $s %{buildroot}%{usersitedir}/$entry/
			done
			rmdir $f
		else
			echo "Cannot move into %{buildroot}%{usersitedir}: $f"
		fi
	fi
done

# remove any header files installed by bundles
rm -rf %{buildroot}%{_includedir}

%endif


# basic config files
install -D -m 0640 %{SOURCE1} %{buildroot}%{_sysconfdir}/mailman.cfg

# systemd files
install -D -m 0644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/%{pname}.conf
install -D -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/%{pname}.service

install -d -p %{buildroot}%{_sysconfdir}/logrotate.d/
install -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/%{pname}

# periodic task
#install -D -m 0644 %{SOURCE5} %{buildroot}%{_unitdir}/%{pname}-digests.service
#install -D -m 0644 %{SOURCE6} %{buildroot}%{_unitdir}/%{pname}-digests.timer

## SELinux
for selinuxvariant in %{selinux_variants}; do
  install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
  install -p -m 644 SELinux/%{pname}.pp.${selinuxvariant} \
    %{buildroot}%{_datadir}/selinux/${selinuxvariant}/%{pname}.pp
done
hardlink -cv %{buildroot}%{_datadir}/selinux

#### gunicorn
install -d -p %{buildroot}%{_sysconfdir}/%{pname}
install -D -m 0644 %{SOURCE7} %{buildroot}%{etcdir}/gunicorn.conf.py
install -D -m 0644 %{SOURCE7} %{buildroot}%{etcdir}/gunicorn.conf.py.dist
install -D -m 0644 %{SOURCE8} %{buildroot}%{etcdir}/settings.py
install -D -m 0644 %{SOURCE8} %{buildroot}%{etcdir}/settings.py.dist

install -D -m 0644 %{SOURCE9} %{buildroot}%{_unitdir}/%{pname}-web.service

install -d -p %{buildroot}%{vardir}/web/static

# Webserver
install -D -m 0644 %{SOURCE11} %{buildroot}%{_httpd_confdir}/%{pname}.conf
install -D -m 0644 %{SOURCE11} %{buildroot}%{_httpd_confdir}/%{pname}.conf.dist

# Hyperkitty archiver
install -D -m 0644 %{SOURCE13} %{buildroot}%{etcdir}/hyperkitty.cfg
install -D -m 0644 %{SOURCE13} %{buildroot}%{etcdir}/hyperkitty.cfg.dist

%if 0%{?mailman3_cron}
## crontab
install -d %{buildroot}%{_sysconfdir}/cron.d
install -D -m 0644 %{SOURCE200} %{buildroot}%{_sysconfdir}/cron.d/%{basename:%{SOURCE200}}
install -D -m 0644 %{SOURCE201} %{buildroot}%{_sysconfdir}/cron.d/%{basename:%{SOURCE201}}
%else
## systemd/service+timer
# mailman
install -D -m 0644 %{SOURCE300} %{buildroot}%{_unitdir}/%{basename:%{SOURCE300}}
install -D -m 0644 %{SOURCE301} %{buildroot}%{_unitdir}/%{basename:%{SOURCE301}}

install -D -m 0644 %{SOURCE310} %{buildroot}%{_unitdir}/%{basename:%{SOURCE310}}
install -D -m 0644 %{SOURCE311} %{buildroot}%{_unitdir}/%{basename:%{SOURCE311}}

# mailman-web
install -D -m 0644 %{SOURCE400} %{buildroot}%{_unitdir}/%{basename:%{SOURCE400}}
install -D -m 0644 %{SOURCE401} %{buildroot}%{_unitdir}/%{basename:%{SOURCE401}}
install -D -m 0644 %{SOURCE402} %{buildroot}%{_unitdir}/%{basename:%{SOURCE402}}
install -D -m 0644 %{SOURCE403} %{buildroot}%{_unitdir}/%{basename:%{SOURCE403}}
install -D -m 0644 %{SOURCE404} %{buildroot}%{_unitdir}/%{basename:%{SOURCE404}}
install -D -m 0644 %{SOURCE405} %{buildroot}%{_unitdir}/%{basename:%{SOURCE405}}
install -D -m 0644 %{SOURCE406} %{buildroot}%{_unitdir}/%{basename:%{SOURCE406}}

install -D -m 0644 %{SOURCE410} %{buildroot}%{_unitdir}/%{basename:%{SOURCE410}}
install -D -m 0644 %{SOURCE411} %{buildroot}%{_unitdir}/%{basename:%{SOURCE411}}
install -D -m 0644 %{SOURCE412} %{buildroot}%{_unitdir}/%{basename:%{SOURCE412}}
install -D -m 0644 %{SOURCE413} %{buildroot}%{_unitdir}/%{basename:%{SOURCE413}}
install -D -m 0644 %{SOURCE414} %{buildroot}%{_unitdir}/%{basename:%{SOURCE414}}
install -D -m 0644 %{SOURCE415} %{buildroot}%{_unitdir}/%{basename:%{SOURCE415}}
install -D -m 0644 %{SOURCE416} %{buildroot}%{_unitdir}/%{basename:%{SOURCE416}}
%endif


## substitute all placeholders
%define bindir_gunicorn %{bindir}

%if 0%{?mailman3_virtualenv}
### VIRTUALENV PACKAGING

%define pythonpath %{sitelibdir}

%else
### BUNDLED-AS-REQUIRED PACKAGING

%define pythonpath %{usersitedir}

%if 0%{?b_e_gunicorn}
%else
%define bindir_gunicorn %{_bindir}
%endif

%endif

find %{buildroot}%{_sysconfdir} %{buildroot}%{_unitdir} %{buildroot}%{_tmpfilesdir} -type f | while read file; do
	# replace directories
	sed -i -e 's,@LOGDIR@,%{logdir},g;s,@BINDIR@,%{bindir},g;s,@BASEDIR@,%{basedir},g;s,@RUNDIR@,%{rundir},g;s,@VARDIR@,%{vardir},g;s,@SPOOLDIR@,%{spooldir},g;s,@ETCDIR@,%{etcdir},g;s,@LOCKDIR@,%{lockdir},g;s,@SYSCONFDIR@,%{sysconfdir},g;s,@MMUSER@,%{mmuser},g;s,@MMGROUP@,%{mmgroup},g' $file
	# replace ports
	sed -i -e 's,@WEBPORT@,%{webport},g;s,@LMTPPORT@,%{lmtpport},g;s,@RESTAPIPORT@,%{restapiport},g' $file

	sed -i -e 's,@BINDIR_GUNICORN@,%{bindir_gunicorn},g;s,@PYTHONPATH@,%{pythonpath},g' $file
done


#TODO#final#check
# check whether it's bascially working
PYTHONPATH=%{buildroot}%{sitelibdir}

%if 0%{?mailman3_virtualenv}
### VIRTUALENV PACKAGING
%else
### BUNDLED-AS-REQUIRED PACKAGING
PYTHONPATH=$PYTHONPATH:%{buildroot}%{usersitedir}
%endif

export PYTHONPATH

## mailman
# prepare "check" config file
install -D -m 0640 %{SOURCE1} %{buildroot}%{_sysconfdir}/mailman.cfg.check
sed -i -e 's,@LOGDIR@,%{buildroot}%{logdir},g;s,@BINDIR@,%{buildroot}%{bindir},g;s,@BASEDIR@,%{buildroot}%{basedir},g;s,@RUNDIR@,%{buildroot}%{rundir},g;s,@VARDIR@,%{buildroot}%{vardir},g;s,@SPOOLDIR@,%{buildroot}%{spooldir},g;s,@ETCDIR@,%{buildroot}%{etcdir},g;s,@LOCKDIR@,%{buildroot}%{lockdir},g;s,@SYSCONFDIR@,%{buildroot}%{sysconfdir},g;s,@MMUSER@,%{mmuser},g;s,@MMGROUP@,%{mmgroup},g' %{buildroot}%{_sysconfdir}/mailman.cfg.check

# check whether online help is working
echo "Check whether 'mailman' is at least able to display online help"
python%{python3_version} %{buildroot}%{bindir}/mailman --config %{buildroot}%{_sysconfdir}/mailman.cfg.check --help >/dev/null
if [ $? -eq 0 ]; then
  echo "Check whether 'mailman' is at least able to display online help - SUCCESSFUL"
else
  exit 1
fi

## mailman-web
# prepare "check" config file
install -d %{buildroot}%{etcdir}/check/
install -D -m 0644 %{SOURCE8} %{buildroot}%{etcdir}/check/settings.py
sed -i -e 's,@LOGDIR@,%{buildroot}%{logdir},g;s,@BINDIR@,%{buildroot}%{bindir},g;s,@BASEDIR@,%{buildroot}%{basedir},g;s,@RUNDIR@,%{buildroot}%{rundir},g;s,@VARDIR@,%{buildroot}%{vardir},g;s,@SPOOLDIR@,%{buildroot}%{spooldir},g;s,@ETCDIR@,%{buildroot}%{etcdir},g;s,@LOCKDIR@,%{buildroot}%{lockdir},g;s,@SYSCONFDIR@,%{buildroot}%{sysconfdir},g;s,@MMUSER@,%{mmuser},g;s,@MMGROUP@,%{mmgroup},g' %{buildroot}%{etcdir}/check/settings.py

# check whether online help is working
echo "Check whether 'mailman-web' is at least able to display online help"
MAILMAN_WEB_CONFIG=%{buildroot}%{etcdir}/check/settings.py
export MAILMAN_WEB_CONFIG
set +x
output=$(python%{python3_version} %{buildroot}%{bindir}/mailman-web --help)
if [ $? -eq 0 ]; then
  echo "Check whether 'mailman-web' is at least able to display online help - SUCCESSFUL"

  for module in postorius hyperkitty staticfiles sessions rest_framework haystack django_q django_extensions contenttypes compressor auth account; do
    echo -n "Check for module in 'mailman-web --help': $module"
    if echo "$output" | %{__grep} -F -q "[$module]"; then
      echo " OK"
    else
      echo " NOT FOUND"
      exit 1
    fi
  done
else
  exit 1
fi
set -x

# remove "check" config file
rm -f %{buildroot}%{_sysconfdir}/mailman.cfg.check
rm -rf %{buildroot}%{etcdir}/check/

# remove created log/db files
rm -f %{buildroot}%{logdir}/*.log %{buildroot}%{vardir}/db/*.db


%pre
# User & Group
if getent group %{mmgroup} >/dev/null; then
	echo "system group for %{pname} already exists: %{mmgroup}"
else
	if [ -n "%{mmgroupid}" ]; then
		echo "system group for %{pname} needs to be created: %{mmgroup}/%{mmgroupid}"
		groupadd -r -g %{mmgroupid} %{mmgroup} >/dev/null
	else
		echo "system group for %{pname} needs to be created: %{mmgroup}"
		groupadd -r %{mmgroup} >/dev/null
	fi
fi

if getent passwd %{mmuser} >/dev/null; then
	echo "system user for %{pname} already exists: %{mmuser}"
	homedir=$(getent passwd %{mmuser} | awk -F: '{ print $6 }')
	if [ "$homedir" != "%{vardir}" ]; then
		echo "system user for %{pname} already exists: %{mmuser} bu has not required home directory: %{vardir} (current: $homedir)"
		exit 1
	fi
else
	if [ -n "%{mmuserid}" ]; then
		echo "system user for %{pname} needs to be created: %{mmuser}/%{mmuserid}"
    		useradd -r -u %{mmuserid} -g %{mmgroup} -d %{vardir} -s /sbin/nologin -c "Mailman3, the mailing-list manager" %{mmuser} >/dev/null
	else
		echo "system user for %{pname} needs to be created: %{mmuser}"
    		useradd -r -g %{mmgroup} -d %{vardir} -s /sbin/nologin -c "Mailman3, the mailing-list manager" %{mmuser} >/dev/null
	fi
fi

# SELinux
for selinuxvariant in %{selinux_variants}; do
    %selinux_relabel_pre -s ${selinuxvariant}
done


%post
# SELinux
for selinuxvariant in %{selinux_variants}; do
    %selinux_modules_install -s ${selinuxvariant} %{_datadir}/selinux/${selinuxvariant}/%{pname}.pp || :
done

declare -A portlabel
portlabel[%{restapiport}]="mailman_restapi_port_t"
portlabel[%{lmtpport}]="mailman_lmtp_port_t"
portlabel[%{webport}]="mailman_web_port_t"

for port in ${!portlabel[@]}; do
    if semanage port -l | grep -q "^${portlabel[$port]}\s*tcp\s*$port$"; then
        echo "SELinux adjustments for %{pname} port tcp/$port (${portlabel[$port]}) already done"
    else
        echo "SELinux adjustments for %{pname} port tcp/$port (${portlabel[$port]})"
        semanage port -a -t ${portlabel[$port]} -p tcp $port
    fi
done

# SELinux
for dir in %{basedir} %{vardir} %{logdir} %{lockdir} %{rundir} %{etcdir}; do
    echo "SELinux fixfiles for: %{pname} ($dir)"
    /usr/sbin/fixfiles -R %{name} restore $dir >/dev/null
done

# Owner
find %{spooldir} %{vardir} %{logdir} %{lockdir} %{rundir} %{_sysconfdir}/mailman.cfg ! -user %{mmuser} | while read entry; do
	echo "Adjust user to %{mmuser} of entry: $entry"
	chown %{mmuser} "$entry"
done

# Group
find %{spooldir} %{vardir} %{logdir} %{lockdir} %{rundir} %{_sysconfdir}/mailman.cfg ! -group %{mmgroup} -a ! -group mail | while read entry; do
	echo "Adjust group to %{mmgroup} of entry: $entry"
	chgrp %{mmgroup} "$entry"
done

# replace password/key placeholders
ymd=$(date '+%Y%m%d')
sed_expression=""
for entry in SECRET_KEY MAILMAN_ARCHIVER_KEY RESTAPIPASS; do
	pass="date.$ymd.secret.$(uuidgen | md5sum | base64 | cut -c 1-16)"
	[ -n "$sed_expression" ] && sed_expression="${sed_expression};"
	sed_expression="${sed_expression}s,@${entry}@,$pass,g"
done
	
## substitute all placeholders
find %{_sysconfdir}/mailman.cfg %{etcdir} -type f | while read file; do
	sed -i -e "$sed_expression" $file
done

## systemd/service
%systemd_post %{pname}.service
%systemd_post %{pname}-web.service

%if 0%{?mailman3_cron}
## crontab -> nothing todo
%else
## systemd/timers
## macro #systemd_post will not enable the timers -> enable them here
## timers will only run if main service is running because of "PartOf" property
%define systemctl_enable_if_not_active() { \
if systemctl -q is-active %1; then \
	echo "Timer already enabled: %1"; \
else \
	echo "Timer will be enabled: %1"; \
	systemctl enable %1; \
fi }

echo "Enable timers (will only run if main services are active)"
# mailman
%systemctl_enable_if_not_active %{basename:%{SOURCE310}}
%systemctl_enable_if_not_active %{basename:%{SOURCE311}}
%systemctl_enable_if_not_active %{basename:%{SOURCE310}}
%systemctl_enable_if_not_active %{basename:%{SOURCE311}}
# mailman-web
%systemctl_enable_if_not_active %{basename:%{SOURCE410}}
%systemctl_enable_if_not_active %{basename:%{SOURCE411}}
%systemctl_enable_if_not_active %{basename:%{SOURCE412}}
%systemctl_enable_if_not_active %{basename:%{SOURCE413}}
%systemctl_enable_if_not_active %{basename:%{SOURCE414}}
%systemctl_enable_if_not_active %{basename:%{SOURCE415}}
%systemctl_enable_if_not_active %{basename:%{SOURCE416}}
%endif

# check for required postfix extension
echo
echo "## CHECK postfix configuration:"
echo -n "# transport_maps extension CHECK: "
postconf_transport_maps=$(postconf -h transport_maps)
if echo "$postconf_transport_maps" | grep "hash:%{vardir}/data/postfix_lmtp"; then
	echo "# transport_maps extension OK"
else
	echo
	echo "# transport_maps misses extension"
	echo -n "postconf -e '"
	echo -n "transport_maps = ${postconf_transport_maps}${postconf_transport_maps:+ }hash:%{vardir}/data/postfix_lmtp"
	echo "'"
fi	

echo -n "# local_recipient_maps extension CHECK: "
postconf_local_recipient_maps=$(postconf -h local_recipient_maps)
if echo "$postconf_local_recipient_maps" | grep "hash:%{vardir}/data/postfix_lmtp"; then
	echo "# local_recipient_maps extension OK"
else
	echo
	echo "# local_recipient_maps misses extension"
	echo -n "postconf -e '"
	echo -n "local_recipient_maps = ${postconf_local_recipient_maps}${postconf_local_recipient_maps:+ }hash:%{vardir}/data/postfix_lmtp"
	echo "'"
fi	

echo -n "# relay_domains extension CHECK: "
postconf_relay_domains=$(postconf -h relay_domains)
if echo "$postconf_relay_domains" | grep "hash:%{vardir}/data/postfix_domains"; then
	echo "# relay_domains extension OK"
else
	echo
	echo "# relay_domains misses extension"
	echo -n "postconf -e '"
	echo -n "relay_domains = ${postconf_relay_domains}${postconf_relay_domains:+ }hash:%{vardir}/data/postfix_domains"
	echo "'"
fi	

echo -n "# recipient_delimiter CHECK: "
postconf_recipient_delimiter=$(postconf -h recipient_delimiter)
if echo "$postconf_recipient_delimiter" | grep '^\+$'; then
	echo "# recipient_delimiter OK"
else
	echo
	echo "# recipient_delimiter misses extension"
	echo "postconf -e 'recipient_delimiter = +'"
fi	

cat <<END

## CHECK ALSO: %{etcdir}/settings.py 
 - ALLOWED_HOSTS
 - ADMINS
 - CSRF_TRUSTED_ORIGINS
 - *CAPTCHA* service configuration+activation

## CHECK ALSO: %{etcdir}/settings.py 
 - DEFAULT_FROM_EMAIL
 - SERVER_EMAIL
Current:
END

grep -E '^(DEFAULT_FROM_EMAIL|SERVER_EMAIL)' %{etcdir}/settings.py

cat <<END

## CHECK ALSO: %{_sysconfdir}/mailman.cfg
 - site_owner
Current:
END

grep -E '^(site_owner)' %{_sysconfdir}/mailman.cfg

cat <<END

## CHECK ALSO: %{_httpd_confdir}/%{pname}.conf
 - Access Control for django's admin portal
END


echo


%preun
## systemd/service
%systemd_preun %{basename:%{SOURCE310}}
%systemd_preun %{basename:%{SOURCE311}}

%if 0%{?mailman3_cron}
## crontab -> nothing todo
%else
## systemd/timers
# mailman
%systemd_preun %{basename:%{SOURCE310}}
%systemd_preun %{basename:%{SOURCE311}}
# mailman-web
%systemd_preun %{basename:%{SOURCE410}}
%systemd_preun %{basename:%{SOURCE411}}
%systemd_preun %{basename:%{SOURCE412}}
%systemd_preun %{basename:%{SOURCE413}}
%systemd_preun %{basename:%{SOURCE414}}
%systemd_preun %{basename:%{SOURCE415}}
%systemd_preun %{basename:%{SOURCE416}}
%endif

if [ $1 -eq 0 ] ; then
    for selinuxvariant in %{selinux_variants}; do
        %selinux_modules_uninstall -s ${selinuxvariant} %{_datadir}/selinux/${selinuxvariant}/%{pname}.pp || :
    done
fi


%postun
## systemd/service
%systemd_postun %{basename:%{SOURCE310}}
%systemd_postun %{basename:%{SOURCE311}}

%if 0%{?mailman3_cron}
## crontab -> nothing todo
%else
## systemd/timers
# mailman
%systemd_postun %{basename:%{SOURCE310}}
%systemd_postun %{basename:%{SOURCE311}}
# mailman-web
%systemd_postun %{basename:%{SOURCE410}}
%systemd_postun %{basename:%{SOURCE411}}
%systemd_postun %{basename:%{SOURCE412}}
%systemd_postun %{basename:%{SOURCE413}}
%systemd_postun %{basename:%{SOURCE414}}
%systemd_postun %{basename:%{SOURCE415}}
%systemd_postun %{basename:%{SOURCE416}}
%endif

# SELinux
if [ $1 -eq 0 ] ; then
    semanage port -l | grep -q "^mailman_.*\s*tcp\s*" | while read port; do
        echo "SELinux delete for %{pname} port tcp/$port"
        semanage port -d -p tcp $port
    done
fi


%posttrans
# SELinux
for selinuxvariant in %{selinux_variants}; do
    %selinux_relabel_post -s ${selinuxvariant}
done

# webinterface setup
echo "Run as %{mmuser}: %{bindir}/mailman-web check"
su - -s /bin/bash %{mmuser} -c "%{bindir}/mailman-web check"

echo "Run as %{mmuser}: %{bindir}/mailman-web migrate"
su - -s /bin/bash %{mmuser} -c "%{bindir}/mailman-web migrate"

echo "Run as %{mmuser}: %{bindir}/mailman-web collectstatic --noinput"
su - -s /bin/bash %{mmuser} -c "%{bindir}/mailman-web collectstatic --noinput"

echo "Run as %{mmuser}: %{bindir}/mailman-web compress"
su - -s /bin/bash %{mmuser} -c "%{bindir}/mailman-web compress"


%files

%{_unitdir}/*.service
%{_tmpfilesdir}
%config(noreplace) %attr(640,%{mmuser},%{mmgroup}) %{_sysconfdir}/mailman.cfg
%{_sysconfdir}/logrotate.d/%{pname}
%dir %attr(755,%{mmuser},mail)       %{vardir}
%dir %attr(770,%{mmuser},%{mmgroup}) %{vardir}/db
%dir %attr(2770,%{mmuser},mail)      %{vardir}/data
%dir %attr(775,%{mmuser},%{mmgroup}) %{vardir}/web/static
%dir %attr(770,%{mmuser},%{mmgroup}) %{spooldir}
%dir %attr(770,%{mmuser},%{mmgroup}) %{logdir}
%dir %attr(770,%{mmuser},%{mmgroup}) %{rundir}
%dir %attr(770,%{mmuser},%{mmgroup}) %{lockdir}

%if 0%{?mailman3_cron}
%config(noreplace) %{_sysconfdir}/cron.d/
%else
%{_unitdir}/*.timer
%endif

# webinterface
%config(noreplace) %{_sysconfdir}/%{pname}/gunicorn.conf.py
%config(noreplace) %{_sysconfdir}/%{pname}/settings.py
%config(noreplace) %{_sysconfdir}/%{pname}/hyperkitty.cfg
%config(noreplace) %{_httpd_confdir}/%{pname}.conf

%{_sysconfdir}/%{pname}/gunicorn.conf.py.dist
%{_sysconfdir}/%{pname}/settings.py.dist
%{_sysconfdir}/%{pname}/hyperkitty.cfg.dist
%{_httpd_confdir}/%{pname}.conf.dist

# SELinux
%{_datadir}/selinux/*/%{pname}.pp


%if 0%{?mailman3_virtualenv}
### VIRTUALENV PACKAGING
%{basedir}
%attr(770,%{mmuser},%{mmgroup}) %{vardir}/.bash_profile


%else
### BUNDLED-AS-REQUIRED PACKAGING
%{usersitedir}
%{sharedstatesitedir}
%dir %attr(700,%{mmuser},%{mmgroup}) %{vardir}/.local

%attr(755,root,root)    %{_bindir}/*
%attr(755,root,root)    %{bindir}

%if 0%{?b_e_dkimpy}
%{_mandir}/*
%endif

%if %{noarch}
%else
# package binary libs
%{_libdir}/*
%endif


%endif


%changelog
* Sat Apr 22 2023 Peter Bieringer <pb@bieringer.de> - 3.3.8-8
- Further adjustments for Fedora and EL

* Thu Apr 13 2023 Peter Bieringer <pb@bieringer.de> - 3.3.8-7
- Fix native build by using USER_SITE directory for by OS+EPEL unsupported but required modules

* Thu Apr 13 2023 Peter Bieringer <pb@bieringer.de> - 3.3.8-6
- Replace packaged public_suffix_list.dat by softlink to file provided by RPM publicsuffix-list
- Install module requests 'explicity' earlier to avoid unexpected Internet access during build of 'publicsuffix2'

* Wed Apr 12 2023 Peter Bieringer <pb@bieringer.de> - 3.3.8-5
- Fix build toggle logic

* Wed Apr 12 2023 Peter Bieringer <pb@bieringer.de> - 3.3.8-4
- Use systemd-timer units instead of cron jobs by default
- Extend SELinux policy

* Fri Apr 07 2023 Peter Bieringer <pb@bieringer.de> - 3.3.8-3
- Replace PIP bundle tar.gz by dedicated sources and add required build dependencies
- Implement (unfortunatly broken on F37/F38/EL9) native packaging method as an alternative
- Enforce Python 3.9 on EL8
- Extend SELinux policy for F38

* Mon Apr 03 2023 Peter Bieringer <pb@bieringer.de> - 3.3.8-2
- extend for optional bundled version
- add patch for Woosh
- Extend SELinux policy

* Mon Apr 03 2023 Peter Bieringer <pb@bieringer.de> - 3.3.8-1
- Initial virtualenv edition based on https://kojipkgs.fedoraproject.org//packages/mailman3/3.3.4/6.fc36/src/mailman3-3.3.4-6.fc36.src.rpm following https://docs.mailman3.org/en/latest/install/virtualenv.html#virtualenv-install
- Enable (optional) recaptcha/hcaptcha/friendlycaptcha protection for subscription/login/password-reset
- Default configuration: sqlite3/hyperkitty/whoosh
