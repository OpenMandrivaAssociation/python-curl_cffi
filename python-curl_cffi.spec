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
# libcurl-impersonate.a is a relocatable object, not LLVM bitcode.
CFLAGS="${CFLAGS//-flto/}"
LDFLAGS="${LDFLAGS//-flto/}"
pip wheel --wheel-dir ../RPMBUILD_wheels --no-deps --no-build-isolation --verbose .

%install
set -euo pipefail
%py_install
PYTHONPATH=%{buildroot}%{python_sitearch} python -c 'import curl_cffi; from curl_cffi import Curl; print(curl_cffi.__version__)'

%files
%doc README.md
%license LICENSE
%{_bindir}/curl-cffi
%{python_sitearch}/curl_cffi
%{python_sitearch}/curl_cffi-%{version}.dist-info
