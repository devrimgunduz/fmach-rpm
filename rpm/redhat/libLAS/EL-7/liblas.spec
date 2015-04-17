Summary:	LAS 1.0/1.1/1.2 ASPRS LiDAR data translation toolset
Name:		liblas
Version:	1.8.0
Release:	2%{?dist}
License:	BSD
Group:		Development/Libraries
Source:		http://download.osgeo.org/%{name}/libLAS-%{version}.tar.bz2
URL:		http://www.liblas.org/
BuildRequires:	cmake, libgeotiff-devel, boost-devel >= 1.53 laszip
Requires:       %{name}-libs = %{version}-%{release}

%description
libLAS is a C/C++ library for reading and writing the very common LAS LiDAR
format. The ASPRS LAS format is a sequential binary format used to store data
from LiDAR sensors and by LiDAR processing software for data interchange and
archival.

%package devel
Summary:        The development files for liblas
Group:          Development/Libraries
Requires:	%{name} = %{version}-%{release}

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
cmake	-DWITH_GDAL:BOOL=ON \
	-DWITH_GEOTIFF:BOOL=ON \
	-DGEOTIFF_INCLUDE_DIR:STRING="/usr/include/libgeotiff" \
	-DWITH_LASZIP:BOOL=OFF \
	-DWITH_TESTS:BOOL=OFF \
	-DWITH_UTILITIES:BOOL=ON \
	-DCMAKE_INSTALL_PREFIX:PATH=/usr \
	-DLIBLAS_LIB_SUBDIR:PATH=%{_lib} \
	-DCMAKE_BUILD_TYPE:STRING="Release" ../%{name}-%{version}/ .

%install
%make_install

%clean
%{__rm} -rf %{buildroot}

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files libs
%{_libdir}/liblas.so*
%{_libdir}/liblas_c.so*

%files
%doc AUTHORS INSTALL README.txt LICENSE.txt
%license COPYING
%dir %{_includedir}/liblas
%dir %{_datadir}/cmake/libLAS-%{version}
%{_bindir}/las2las
%{_bindir}/las2ogr
%{_bindir}/las2txt
%{_bindir}/lasblock
%{_bindir}/lasinfo
%{_bindir}/liblas-config
%{_bindir}/ts2las
%{_bindir}/txt2las

%files devel
%{_includedir}/liblas/*.hpp
%{_includedir}/liblas/capi/*.h
%{_includedir}/liblas/detail/*.hpp
%{_includedir}/liblas/detail/index/*.hpp
%{_includedir}/liblas/detail/reader/*.hpp
%{_includedir}/liblas/detail/writer/*.hpp
%{_includedir}/liblas/external/property_tree/detail/*.hpp
%{_includedir}/liblas/external/property_tree/*.hpp
%{_datadir}/cmake/libLAS-%{version}/liblas-config-version.cmake
%{_datadir}/cmake/libLAS-%{version}/liblas-config.cmake
%{_datadir}/cmake/libLAS-%{version}/liblas-depends-release.cmake
%{_datadir}/cmake/libLAS-%{version}/liblas-depends.cmake
%{_datadir}/%{name}/doc/*

%changelog
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

* Tue Jan 13 2015 Devrim GUNDUZ <devrim@gunduz.org> 1.8.0-1
- Initial packaging
