Summary:	LAS 1.0/1.1/1.2 ASPRS LiDAR data translation toolset
Name:		liblas
Version:	1.8.0
Release:	1%{?dist}
License:	BSD
Group:		Development/Libraries
Source:		http://download.osgeo.org/%{name}/libLAS-%{version}.tar.bz2
URL:		http://www.liblas.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	cmake, libgeotiff-devel, boost-devel >= 1.53 laszip

%description
libLAS is a C/C++ library for reading and writing the very common LAS LiDAR
format. The ASPRS LAS format is a sequential binary format used to store data
from LiDAR sensors and by LiDAR processing software for data interchange and
archival.

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
%{__rm} -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS COPYING INSTALL README.txt LICENSE.txt
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
%{_includedir}/liblas/*.hpp
%{_includedir}/liblas/capi/*.h
%{_includedir}/liblas/detail/*.hpp
%{_includedir}/liblas/detail/index/*.hpp
%{_includedir}/liblas/detail/reader/*.hpp
%{_includedir}/liblas/detail/writer/*.hpp
%{_includedir}/liblas/external/property_tree/detail/*.hpp
%{_includedir}/liblas/external/property_tree/*.hpp
%{_libdir}/liblas.so*
%{_libdir}/liblas_c.so*
%{_datadir}/cmake/libLAS-%{version}/liblas-config-version.cmake
%{_datadir}/cmake/libLAS-%{version}/liblas-config.cmake
%{_datadir}/cmake/libLAS-%{version}/liblas-depends-release.cmake
%{_datadir}/cmake/libLAS-%{version}/liblas-depends.cmake
%{_datadir}/%{name}/doc/*

%changelog
* Tue Jan 13 2015 Devrim GUNDUZ <devrim@gunduz.org> 1.3.0-1
- Initial packaging
