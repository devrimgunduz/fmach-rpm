Summary:	LAS 1.0/1.1/1.2 ASPRS LiDAR data translation toolset
Name:		liblas
Version:	1.8.0
Release:	1%{?dist}
License:	BSD
Group:		Development/Libraries
Source:		http://download.osgeo.org/%{name}/libLAS-%{version}.tar.bz2
URL:		http://www.liblas.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	cmake, libgeotiff-devel, boost-devel >= 1.57 laszip

%description
libLAS is a C/C++ library for reading and writing the very common LAS LiDAR format.
The ASPRS LAS format is a sequential binary format used to store data from LiDAR
sensors and by LiDAR processing software for data interchange and archival.

%prep
%setup -q -n libLAS-%{version}

%build
cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr -D GEOTIFF_INCLUDE_DIR=%{_includedir}/libgeotiff/ .

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS COPYING INSTALL README.txt LICENSE.txt
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
   /usr/lib/liblas.so
   /usr/lib/liblas.so.2.3.0
   /usr/lib/liblas.so.3
   /usr/lib/liblas_c.so
   /usr/lib/liblas_c.so.2.3.0
   /usr/lib/liblas_c.so.3
%{_datadir}/cmake/libLAS-%{version}/liblas-config-version.cmake
%{_datadir}/cmake/libLAS-%{version}/liblas-config.cmake
%{_datadir}/cmake/libLAS-%{version}/liblas-depends-release.cmake
%{_datadir}/cmake/libLAS-%{version}/liblas-depends.cmake
%{_datadir}/%{name}/doc/*

%changelog
* Tue Jan 13 2015 Devrim GUNDUZ <devrim@gunduz.org> 1.3.0-1
- Initial packaging

