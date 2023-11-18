rpmdev-spectool:
	if rpm -q rpmdevtools; then echo "RPM rpmdevtools is already installed"; else echo "RPM rpmdevtools need to be installed first"; dnf install -y rpmdevtools; fi

curl:
	if rpm -q curl; then echo "RPM curl is already installed"; else echo "RPM curl need to be installed first"; dnf install -y curl; fi

download: rpmdev-spectool curl
	rpmdev-spectool $(spec) | awk '$$1 ~ /^Source/ && $$2 ~ /^http/ { print $$2 }' | while read url; do \
		echo "Download source if missing: $$url"; \
		file=$$(basename $$url); \
		if [ -e $$file ]; then \
			echo "Download source if missing: $$url (CHECK-FOR-NEWER)"; \
			curl -s -o $$file -z $$file $$url; \
			r=$$?; \
		else \
			echo "Download source if missing: $$url (MISSING)"; \
			curl -s -o $$file $$url; \
			r=$$?; \
		fi; \
		if [ $$r -eq 0 ]; then \
			echo "Download source if missing: $$url (SUCCESS)"; \
		else \
			echo "Download source if missing: $$url (ERROR)"; \
			exit 1; \
		fi; \
	done

srpm:	download
	if [ -n "$(outdir)" ]; then \
		rpmbuild -bs $(spec) --undefine=_disable_source_fetch --define "_topdir ." --define "_sourcedir ." --define "_srcrpmdir $(outdir)"; \
	else \
		rpmbuild -bs $(spec) --undefine=_disable_source_fetch --define "_topdir ." --define "_sourcedir ." --define "_srcrpmdir ."; \
	fi
