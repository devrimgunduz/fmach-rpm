Summary:	Point Data Abstraction Library
Name:		PDAL
Version:	0.9.9
Release:	2%{?dist}
License:	BSD
Group:		Applications/Libraries
Source:		https://github.com/%{name}/%{name}/archive/%{version}.tar.gz
URL:		http://www.pdal.io
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	cmake boost-devel >= 1.57, proj >= 4.9.0, boost >= 1.57
Requires:	gdal >= 1.11, libgeotiff >= 1.4.0, pcl >= 1.7.2
Requires:	points2grid >= 1.3.0, nitro >= 2.7, laszip >= 2.2.0

%description
PDAL is a BSD licensed library for translating and manipulating point cloud
data of various formats. It is a library that is analogous to the GDAL raster
library. PDAL is focussed on reading, writing, and translating point cloud
data from the ever-growing constellation of data formats. While PDAL is not
explicitly limited to working with LiDAR data formats, its wides format
coverage is in that domain.

PDAL is related to Point Cloud Library (PCL) in the sense that both work with
point data, but PDAL’s niche is data translation and processing pipelines, and
PCL’s is more in the algorithmic exploition domain. There is cross over of both
niches, however, and PDAL provides a user the ability to exploit data using
PCL’s techniques.

%package devel
Summary:        PDAL development header files and libraries
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The pdal-devel package contains the header files and libraries needed to
compile C or C++ applications which will directly interact with PDAL.

%prep
%setup -q
#find . -type f -print0 | xargs -0 sed -i 's/CMAKE_INSTALL_PREFIX}\/lib/CMAKE_INSTALL_LIBDIR}/g'

%build
cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr \
	-D PDAL_LIB_INSTALL_DIR:PATH=%{_lib} \
	-D CMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
	-D CMAKE_VERBOSE_MAKEFILE=ON  \
        -D WITH_GEOTIFF=ON \
        -D GEOTIFF_INCLUDE_DIR=%{_includedir}/libgeotiff \
        -D WITH_LASZIP=ON .

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%{_bindir}/pdal
%{_bindir}/pdal-config
%{_libdir}/libpdal_plugin_reader_pgpointcloud.so
%{_libdir}/libpdal_plugin_writer_pgpointcloud.so
%{_libdir}/libpdal_util.so
%{_libdir}/libpdalcpp.so

%files devel
%defattr(-,root,root)
%{_includedir}/pdal/*.hpp
%{_includedir}/pdal/*.h
%{_includedir}/pdal/plang/*.hpp
%{_includedir}/pdal/util/*.hpp
/usr/lib/pdal/cmake/PDAL*.cmake

%changelog
* Fri Apr 10 2015 Devrim GUNDUZ <devrim@gunduz.org> 0.9.9-2
- Add -devel subpackage, and move related files there.

* Fri Apr 10 2015 Devrim GUNDUZ <devrim@gunduz.org> 0.9.9-1
- Update to 0.9.9

* Tue Mar 10 2015 Devrim GUNDUZ <devrim@gunduz.org> 0.9.8-3
- Add support for more stuff.

* Sun Mar 8 2015 Devrim GUNDUZ <devrim@gunduz.org> 0.9.8-2
- Rebuild with new GDAL and the new build points2grid.

* Tue Jan 13 2015 Devrim GUNDUZ <devrim@gunduz.org> 0.9.8-1
- Initial packaging

