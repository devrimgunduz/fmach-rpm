Summary:	Point Data Abstraction Library
Name:		PDAL
Version:	0.9.9
Release:	3%{?dist}
License:	BSD
Source:		https://github.com/%{name}/%{name}/archive/%{version}.tar.gz
URL:		http://www.pdal.io
BuildRequires:	cmake boost-devel >= 1.57, proj >= 4.9.0, boost >= 1.57
BuildRequires:	hexer-devel, postgresql-devel, geos-devel
BuildRequires:	pcl-devel, openni-devel, qhull-devel, zlib-devel, eigen3-devel
BuildRequires:	python-devel
Requires:	gdal >= 1.11, libgeotiff >= 1.4.0, pcl >= 1.7.2, hexer
Requires:	points2grid >= 1.3.0, nitro >= 2.7, laszip >= 2.2.0
Requires:	postgresql, geos, pcl, openni, qhull
Requires:	zlib, eigen3
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

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
Summary:	PDAL development header files and libraries
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The pdal-devel package contains the header files and libraries needed to
compile C or C++ applications which will directly interact with PDAL.

%package libs
Summary:	The shared libraries required for PDAL
Group:		Development/Libraries

%description libs
The pdal-libs package provides the essential shared libraries for any
PDAL client program or interface. You will need to install this package
to use PDAL

%prep
%setup -q

%build
%cmake	-D PDAL_LIB_INSTALL_DIR:PATH=%{_lib} \
	-D CMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
	-D CMAKE_VERBOSE_MAKEFILE=ON  \
	-D WITH_GEOTIFF=ON \
	-D GEOTIFF_INCLUDE_DIR=%{_includedir}/libgeotiff \
	-D WITH_LASZIP=ON \
	-D PDAL_HAVE_HEXER=ON \
	-D PDAL_HAVE_GEOS=ON \
	-D PDAL_HAVE_PYTHON=ON \
	-D BUILD_PLUGIN_PYTHON=ON \
	-D BUILD_PLUGIN_HEXBIN=ON \
	-D PDAL_HAVE_LIBGEOTIFF=ON \
	-D BUILD_PLUGIN_PCL=ON \
	-D POSTGRESQL_INCLUDE_DIR=%{_includedir}/pgsql \
	-D POSTGRESQL_LIBRARIES=%{_libdir}/libpq.so \
	-D OPENNI2_INCLUDE_DIRS:PATH=%{_includedir}/ni \
	-D OPENNI2_LIBRARY:FILEPATH=%{_libdir}/libOpenNI.so .

make %{?_smp_mflags}

%install
make install/fast DESTDIR=%{buildroot}
# Remove duplicated cmake files
%{__rm} -f %{buildroot}/usr/lib/pdal/cmake/PDAL*.cmake


%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files
%license LICENSE.txt
%doc doc/
%{_bindir}/pdal
%{_bindir}/pdal-config

%files libs
%{_libdir}/libpdal_plugin_reader_pgpointcloud.so
%{_libdir}/libpdal_plugin_writer_pgpointcloud.so
%{_libdir}/libpdal_util.so
%{_libdir}/libpdalcpp.so
%{_libdir}/libpdal_plugin_filter_ground.so
%{_libdir}/libpdal_plugin_filter_hexbin.so
%{_libdir}/libpdal_plugin_filter_pclblock.so
%{_libdir}/libpdal_plugin_filter_predicate.so
%{_libdir}/libpdal_plugin_filter_programmable.so
%{_libdir}/libpdal_plugin_kernel_ground.so
%{_libdir}/libpdal_plugin_kernel_pcl.so
%{_libdir}/libpdal_plugin_kernel_smooth.so
%{_libdir}/libpdal_plugin_kernel_view.so
%{_libdir}/libpdal_plugin_reader_pcd.so
%{_libdir}/libpdal_plugin_writer_pcd.so
%{_libdir}/libpdal_plugin_writer_pclvisualizer.so

%files devel
%{_includedir}/pdal/
%{_libdir}/pdal/cmake/PDAL*.cmake

%changelog
* Mon Apr 20 2015 Devrim GUNDUZ <devrim@gunduz.org> 0.9.9-3
- Various updates:
 - Build with hexer support
 - Own directories in devel subpackage
 - omit deprecated Group: tags and %%clean section
 - Use better macros for make and cmake
 - use %%{?_isa} macro in subpkg dependencies
 - have %%build section envoke 'make'
 - Update %%install section
 - Improve cmake build parameters
 - Use %%license macro
 - Add %%doc
 - Get rid of BuildRoot definition
 - No need to cleanup buildroot during %%install
 - Remove %%defattr
 - Run ldconfig
 - Add PostgreSQL and PointCloud support
 - Add Python and PCL plugins
 - Build with GEOS and OPENNI2 support
 - Update BR and Requires
 - Add -libs subpackage, and move related files there

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

