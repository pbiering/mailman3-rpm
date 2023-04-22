all: clean srpm rpm

rpm:
	for srpms in *.src.rpm; do \
		echo "BUILD: create RPM from SRPM: $$srpms"; \
		rpmbuild --rebuild $$srpms; \
	done

rpm-virtualenv:
	for srpms in *.src.rpm; do \
		echo "BUILD: create RPM from SRPM: $$srpms"; \
		rpmbuild --rebuild $$srpms -D "mailman3_virtualenv 1"; \
	done


clean:
	echo "CLEAN: *.src.rpm"
	if ls -1 *.src.rpm >/dev/null 2>&1; then ls -1 *.src.rpm  | xargs rm; fi

distclean: clean
	echo "CLEAN: downloaded *.tar.gz"
	if ls -1 *.tar.gz  >/dev/null 2>&1; then ls -1 *.tar.gz   | xargs rm; fi

srpm:
	echo "BUILD: create SRPM like COPR is doing"
	make -f ./.copr/Makefile srpm outdir="." spec="mailman3.spec"

srpm-el8:
	echo "BUILD: create SRPM like COPR is doing for EL8"
	make -f ./.copr/Makefile srpm outdir="." spec="mailman3.spec" define="-D 'rhel 8'"
