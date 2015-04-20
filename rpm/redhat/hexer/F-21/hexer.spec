Summary:	LAS and OGR hexagonal density and boundary surface generation
Name:		hexer
Version:	1.3.0
Release:	2%{?dist}
License:	GLPLv2
Source:		https://github.com/hobu/hexer/archive/%{version}.tar.gz
URL:		https://github.com/hobu/hexer
BuildRequires:	cmake, gdal-devel => 1.9.0
BuildRequires:	boost-program-options >= 1.57, boost-thread >= 1.57, boost-iostreams >= 1.57
BuildRequires:	boost-filesystem >= 1.57, boost-system >= 1.57, boost-random >= 1.57
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}, gdal-libs >= 1.9.0

%description
Hexer is a LGPL C++ library that provides some classes for generating hexbin
density surfaces and multipolygon boundaries for large point sets. Hexer
supports two operations at this time, density and boundary. You use hexer
through the curse command.

%package libs
Summary:	The shared libraries required for hexer
Group:		Applications/Databases

%description libs
The hexer-libs package provides the essential shared libraries for any
hexer client program or interface. You will need to install this package
to use hexer

%package devel
Summary:	The development files for hexer
Group:		Development/Libraries
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Development headers and libraries for hexer

%prep
%setup -q

%build
%cmake	-D HEXER_LIB_DIR=%{_libdir} \
	-D LIB_INSTALL_DIR=%{_lib} \
	-D HEXER_HAVE_GDAL=ON .

make %{?_smp_mflags}

%install
make %{?_smp_mflags} install/fast DESTDIR=%{buildroot}

%post -p /sbin/ldconfig
%post libs -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%doc README.md
%license COPYING
%{_bindir}/curse
%{_libdir}/libhexer.so.1.0.2

%files devel
%{_includedir}/%{name}/

%files libs
%{_libdir}/libhexer.so

%changelog
* Mon Apr 20 2015 Devrim GUNDUZ <devrim@gunduz.org> 1.3.0-2
- Various updates:
 - Update license
 - Own directories in main package
 - omit deprecated Group: tags and %%clean section
 - Use better macros for make and cmake
 - use %%{?_isa} macro in subpkg dependencies
 - have %%build section envoke 'make'
 - Update %%install section
 - Improve cmake build parameters
 - move libhexer.so symlink to -libs subpkg
 - Split -devel and -libs subpackages
 - Use %%license macro
 - Get rid of BuildRoot definition
 - No need to cleanup buildroot during %%install
 - Remove %%defattr
 - Run ldconfig
 - Build with GDAL support

* Tue Jan 13 2015 Devrim GUNDUZ <devrim@gunduz.org> 1.3.0-1
- Initial packaging

