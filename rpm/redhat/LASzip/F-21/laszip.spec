Summary:	Quickly turns bulky LAS files into compant LAZ files
Name:		laszip
Version:	2.2.0
Release:	4%{?dist}
License:	LGPLv2
Source0:	https://github.com/LASzip/LASzip/releases/download/v%{version}/%{name}-src-%{version}.tar.gz
URL:		http://www.laszip.org/

%description
LASzip - a free product of rapidlasso GmbH - quickly turns bulky LAS files into
compact LAZ files without information loss.

%package devel
Summary:	The development files for laszip
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers and libraries for laszip

%prep
%setup -q -n %{name}-src-%{version}

%build
CFLAGS="$CFLAGS -lstdc++" ; export CFLAGS
%configure --includedir=%{_includedir}/laszip --disable-static
%{__make} %{?_smp_mflags}

%install
%make_install

# Remove .la files
%{__rm} -f %{buildroot}%{_libdir}/liblaszip.la

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files
%doc AUTHORS
%license COPYING
%{_bindir}/laszippertest
%{_libdir}/liblaszip.so*

%files devel
%{_includedir}/laszip/

%changelog
* Fri Apr 17 2015 Devrim GUNDUZ <devrim@gunduz.org> 2.2.0-4
- More fixes per Fedora review:
 - Update license
 - omit liblaszip.a static library
 - fix liblaszip undefined symbols, by adding -lstdc++ CFLAG
 - omit INSTALL from %%doc
 - Own %%{_includedir}/laszip/ directory
 - devel subpkg now depends on main package
 - omit deprecated Group: tags and %%clean section
 - drop not needed dependency to cmake

* Fri Apr 17 2015 Devrim GUNDUZ <devrim@gunduz.org> 2.2.0-3
- Various fixes per Fedora review #1199296
  * Add devel subpackage
  * Use %%license macro
  * Use %%make_install macro
  * Get rid of BuildRoot definition
  * No need to cleanup buildroot during %%install
  * Remove %%defattr
  * Run ldconfig 
  * Fix version numbers

* Fri Mar 6 2015 Devrim GUNDUZ <devrim@gunduz.org> 2.2.0-2
- Rebuild with new liblas.

* Fri Mar 6 2015 Devrim GUNDUZ <devrim@gunduz.org> 2.2.0-2
- Rebuild with new liblas.

* Tue Jan 13 2015 Devrim GUNDUZ <devrim@gunduz.org> 2.2.0-1
- Initial packaging

