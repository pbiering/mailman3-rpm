rpmdev-spectool:
	if rpm -q rpmdevtools; then echo "RPM rpmdevtools is already installed"; else echo "RPM rpmdevtools need to be installed first"; dnf install -y rpmdevtools; fi

curl:
	if rpm -q curl; then echo "RPM curl is already installed"; else echo "RPM curl need to be installed first"; dnf install -y curl; fi

download: rpmdev-spectool curl
	rpmdev-spectool $(spec) | awk '$$1 ~ /^Source/ && $$2 ~ /^http/ { print $$2 }' | while read url; do \
		file=$$(basename $$url); \
		package=$$(echo $$file | sed 's/-[0-9].*//g'); \
		echo "INFO  : download source  $$file"; \
		urlIndex="https://pypi.org/simple/$$package/"; \
		echo "INFO  : download index   $$package: $$urlIndex"; \
		indexEntry=$$(curl -L -s $$urlIndex | grep ">$$file<"); \
		checksumEntry=$$(echo "$$indexEntry" | sed 's/.*sha256=\([0-9a-f]*\)".*/\1/g'); \
		urlEntry=$$(echo "$$indexEntry" | sed 's/.*href="\(.*\)#.*/\1/g'); \
		if [ -n "$$indexEntry" -a -n "$$checksumEntry" -a -n "$$urlEntry" ]; then \
			echo "INFO  : download index   $$package: $$urlIndex (SUCCESSFUL)"; \
		else \
			echo "ERROR : download index   $$package: $$urlIndex (NOT-SUCCESSFUL)"; \
			echo "ERROR : download index   $$package: indexEntry=$$indexEntry"; \
			echo "ERROR : download index   $$package: checksumEntry=$$checksumEntry"; \
			echo "ERROR : download index   $$package: urlEntry=$$urlEntry"; \
			exit 1; \
		fi; \
		if [ -e $$file ]; then \
			echo "INFO  : index entry for  $$file has checksum: $$checksumEntry"; \
			checksumExisting=$$(sha256sum $$file | awk '{ print $$1 }'); \
			echo "INFO  : local            $$file has checksum: $$checksumExisting"; \
			if [ "$$checksumEntry" = "$$checksumExisting" ]; then \
				echo "INFO  : analyse checksum $$file (CHECKSUM-MATCH)"; \
				continue; \
			else \
				echo "NOTICE: analyse checksum $$file (CHECKSUM-MISMATCH)"; \
				download=1; \
			fi; \
		else  \
			echo "NOTICE: download source: $$urlEntry (MISSING)"; \
			download=1; \
		fi; \
		if [ $$download -eq 1 ]; then \
			echo "INFO  : download source: $$urlEntry to file $$file"; \
			curl -s -o $$file $$urlEntry; \
			r=$$?; \
			if [ $$r -eq 0 ]; then \
				echo "INFO  : download source: $$urlEntry (SUCCESS)"; \
				echo "INFO  : index entry for  $$file has checksum: $$checksumEntry"; \
				checksumExisting=$$(sha256sum $$file | awk '{ print $$1 }'); \
				echo "INFO  : local            $$file has checksum: $$checksumExisting"; \
				if [ "$$checksumEntry" = "$$checksumExisting" ]; then \
					echo "INFO  : analyse checksum $$file (CHECKSUM-MATCH)"; \
					continue; \
				else \
					echo "NOTICE: analyse checksum $$file (CHECKSUM-MISMATCH)"; \
					exit 1; \
				fi; \
			else \
				echo "ERROR : download source: $$urlEntry (ERROR)"; \
				exit 1; \
			fi; \
		fi; \
	done

srpm:	download
	if [ -n "$(outdir)" ]; then \
		rpmbuild -bs $(spec) --undefine=_disable_source_fetch --define "_topdir ." --define "_sourcedir ." --define "_srcrpmdir $(outdir)"; \
	else \
		rpmbuild -bs $(spec) --undefine=_disable_source_fetch --define "_topdir ." --define "_sourcedir ." --define "_srcrpmdir ."; \
	fi
