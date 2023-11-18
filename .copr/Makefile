rpmdev-spectool:
	if rpm -q rpmdevtools; then echo "RPM rpmdevtools is already installed"; else echo "RPM rpmdevtools need to be installed first"; dnf install -y rpmdevtools; fi

curl:
	if rpm -q curl; then echo "RPM curl is already installed"; else echo "RPM curl need to be installed first"; dnf install -y curl; fi

download: rpmdev-spectool curl
	rpmdev-spectool $(spec) | awk '$$1 ~ /^Source/ && $$2 ~ /^http/ { print $$2 }' | while read url; do \
		echo "INFO  : Download source if missing or checksum not equal: $$url"; \
		file=$$(basename $$url); \
		package=$$(echo $$file | sed 's/-[0-9].*//g'); \
		urlIndex="https://pypi.org/simple/$$package/"; \
		echo "INFO  : Download index for $$package: $$urlIndex"; \
		indexEntry=$$(curl -L -s $$urlIndex | grep ">$$file<"); \
		checksumEntry=$$(echo "$$indexEntry" | sed 's/.*sha256=\([0-9a-f]*\)".*/\1/g'); \
		urlEntry=$$(echo "$$indexEntry" | sed 's/.*href="\(.*\)#.*/\1/g'); \
		if [ -n "$$indexEntry" -a -n "$$checksumEntry" -a -n "$$urlEntry" ]; then \
			echo "INFO  : Download index for $$package: $$urlIndex (SUCCESSFUL)"; \
		else \
			echo "ERROR : Download index for $$package: $$urlIndex (NOT-SUCCESSFUL)"; \
			echo "ERROR : Download index for $$package: indexEntry=$$indexEntry"; \
			echo "ERROR : Download index for $$package: checksumEntry=$$checksumEntry"; \
			echo "ERROR : Download index for $$package: urlEntry=$$urlEntry"; \
			exit 1; \
		fi; \
		if [ -e $$file ]; then \
			echo "INFO  : index entry for $$file has checksum: $$checksumEntry"; \
			checksumExisting=$$(sha256sum $$file | awk '{ print $$1 }'); \
			echo "INFO  : local $$file has checksum: $$checksumExisting"; \
			if [ "$$checksumEntry" = "$$checksumExisting" ]; then \
				echo "INFO  : Analyse checksum for $$file (CHECKSUM-MATCH)"; \
				continue; \
			else \
				echo "NOTICE: Analyse checksum for $$file (CHECKSUM-MISMATCH)"; \
				download=1; \
			fi; \
		else  \
			echo "NOTICE: Download source: $$urlEntry (MISSING)"; \
			download=1; \
		fi; \
		if [ $$download -eq 1 ]; then \
			echo "INFO  : Download source: $$urlEntry to file $$file"; \
			curl -s -o $$file $$urlEntry; \
			r=$$?; \
			if [ $$r -eq 0 ]; then \
				echo "INFO  : Download source: $$urlEntry (SUCCESS)"; \
			else \
				echo "ERROR : Download source: $$urlEntry (ERROR)"; \
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
