Summary:	LAS 1.0/1.1/1.2 ASPRS LiDAR data translation toolset
Name:		liblas
Version:	1.8.0
Release:	3%{?dist}
License:	BSD and Boost
Source:		http://download.osgeo.org/%{name}/libLAS-%{version}.tar.bz2
URL:		http://www.liblas.org/
BuildRequires:	cmake, libgeotiff-devel, boost-devel >= 1.53 laszip-devel
BuildRequires:	libtiff-devel, gdal-devel
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}, laszip

%description
libLAS is a C/C++ library for reading and writing the very common LAS LiDAR
format. The ASPRS LAS format is a sequential binary format used to store data
from LiDAR sensors and by LiDAR processing software for data interchange and
archival.

%package devel
Summary:        The development files for liblas
Group:          Development/Libraries
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Development headers and libraries for liblas.

%package libs
Summary:        The shared libraries required for liblas
Group:          Applications/Databases

%description libs
The liblas-libs package provides the essential shared libraries for any
liblasL client program or interface. You will need to install this package
to use liblas

%prep
%setup -q -n libLAS-%{version}

%build
%cmake	-DWITH_GDAL:BOOL=ON \
	-DWITH_GEOTIFF:BOOL=ON \
	-DGEOTIFF_INCLUDE_DIR:PATH="$(pkg-config --variable=includedir libgeotiff)" \
	-DWITH_LASZIP:BOOL=ON \
	-DWITH_TESTS:BOOL=OFF \
	-DWITH_UTILITIES:BOOL=ON \
	-DLIBLAS_LIB_SUBDIR:PATH=%{_lib} \
	-DCMAKE_BUILD_TYPE:STRING="Release" \
	-DWITH_PKGCONFIG:BOOL=OFF \
	-DCMAKE_SKIP_RPATH:BOOL=ON .

make %{?_smp_mflags}

%install
make install/fast DESTDIR=%{buildroot}

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files libs
%license LICENSE.txt
%{_libdir}/liblas.so
%{_libdir}/liblas_c.so

%files
%doc AUTHORS README.txt
%{_includedir}/liblas
%{_datadir}/cmake/libLAS-%{version}
%{_bindir}/las2las
%{_bindir}/las2ogr
%{_bindir}/las2txt
%{_bindir}/lasblock
%{_bindir}/lasinfo
%{_bindir}/ts2las
%{_bindir}/txt2las
%{_libdir}/liblas.so.2.3.0
%{_libdir}/liblas.so.3
%{_libdir}/liblas_c.so.2.3.0
%{_libdir}/liblas_c.so.3

%files devel
%{_bindir}/liblas-config
%{_includedir}/liblas/
%{_datadir}/cmake/libLAS-%{version}/
%{_datadir}/%{name}/doc/

%changelog
* Fri Apr 17 2015 Devrim GUNDUZ <devrim@gunduz.org> 1.8.0-3
- Various updates, per Fedora review from Rex:
 - Update license
 - omit INSTALL from %%doc
 - Own directories in -devel subpackage
 - omit deprecated Group: tags and %%clean section
 - Use better macros for make and cmake
 - use %%{?_isa} macro in subpkg dependencies
 - have %build section envoke 'make'
 - Update %%install section
 - Improve cmake build parameters, also fix rpath
 - move liblaszip.so symlink to -devel subpkg
 - move liblas-config to -devel subpackage
 - Split -devel and -libs subpackages

* Fri Apr 17 2015 Devrim GUNDUZ <devrim@gunduz.org> 1.8.0-2
- Various updates:
  * Split -devel and -libs subpackages
  * Use %%license macro
  * Use %%make_install macro
  * Get rid of BuildRoot definition
  * No need to cleanup buildroot during %%install
  * Remove %%defattr
  * Run ldconfig
  * Fix version numbers in spec file
  * BR laszip-devel, and require laszip, per recent laszip changes.

* Tue Jan 13 2015 Devrim GUNDUZ <devrim@gunduz.org> 1.8.0-1
- Initial packaging
