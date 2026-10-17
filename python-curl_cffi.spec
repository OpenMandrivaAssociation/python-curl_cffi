Name:		python-curl_cffi
Version:	0.16.3
Release:	1
Summary:	libcurl FFI bindings with browser impersonation
License:	MIT
Group:		Development/Python
URL:		https://github.com/lexiforest/curl_cffi
Source0:	https://files.pythonhosted.org/packages/source/c/curl_cffi/curl_cffi-%{version}.tar.gz
Patch0:		curl_cffi-0.16.3-static-link.patch

BuildRequires:	python
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(cffi)
BuildRequires:	python%{pyver}dist(wheel)
BuildRequires:	clang
BuildRequires:	pkgconfig(libffi)
BuildRequires:	curl-impersonate
BuildRequires:	%mklibname stdc++ -d

%description
Python bindings for a browser-impersonating libcurl. The extension is linked
against the static curl-impersonate archive, not a prebuilt upstream blob.

%prep
%autosetup -n curl_cffi-%{version} -p1

%build
set -euo pipefail
export IMPERSONATE_BUILD_DIR=%{_libdir}/curl-impersonate
test -f "$IMPERSONATE_BUILD_DIR/libcurl-impersonate.a"
test -f "$IMPERSONATE_BUILD_DIR/include/curl/curl.h"
mkdir -p ../RPMBUILD_wheels
# rpm exports RPM_OPT_FLAGS, not CFLAGS. The static archive is a
# relocatable object, so drop -flto before the extension is linked.
# --no-undefined rejects the Python symbols that the interpreter
# provides when the module is loaded.
CFLAGS="${CFLAGS:-$RPM_OPT_FLAGS}"
LDFLAGS="${LDFLAGS:-$RPM_LD_FLAGS}"
CFLAGS="${CFLAGS//-flto/}"
LDFLAGS="${LDFLAGS//-flto/}"
LDFLAGS="${LDFLAGS//-Wl,--no-undefined/}"
export CFLAGS LDFLAGS
pip wheel --wheel-dir ../RPMBUILD_wheels --no-deps --no-build-isolation --verbose .

%install
# nounset trips rpm's install footer, which tests an unset DONT_CLEANUP.
set -eo pipefail
%py_install
# -P keeps the unpacked source tree off sys.path. Without it, import
# finds the in-tree package, which has no built _wrapper extension.
PYTHONPATH=%{buildroot}%{python_sitearch} python -P -c 'import curl_cffi; from curl_cffi import Curl; print(curl_cffi.__version__)'

%files
%doc README.md
%license LICENSE
%{_bindir}/curl-cffi
%{python_sitearch}/curl_cffi
%{python_sitearch}/curl_cffi-%{version}.dist-info
