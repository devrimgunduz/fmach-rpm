%global apiversion 1.7

Name:           pcl
Version:        1.7.2
Release:        3%{?dist}
Summary:        Library for point cloud processing

Group:          System Environment/Libraries
License:        BSD
URL:            http://pointclouds.org/
Source0:        https://github.com/PointCloudLibrary/%{name}/archive/%{name}-%{version}.tar.gz
# Only enable sse2, and only on x86_64
Patch0:         %{name}-1.7.2-sse2.patch
# Patch to compile against system metslib
Patch1:         %{name}-1.7.2-metslib.patch
# Patch for PCLConfig.cmake to find pcl
Patch2:         %{name}-1.7.2-fedora.patch
# Exclude the "build" directory from doxygen processing.
Patch3:         %{name}-1.7.2-doxyfix.patch
# Pass -DBOOST_NEXT_PRIOR_HPP_INCLUDED to moc.
Patch4:         %{name}-0ddf-boost157.patch
# Add patch for vtk include path
Patch5:		%{name}-1.7.2-vtk-include.patch
Patch6:		pcl-1.7.2-vtk-includedir.patch

# For plain building
BuildRequires:  cmake, gcc-c++, boost-devel
# Documentation
BuildRequires:  doxygen, graphviz, python-sphinx

# mandatory
BuildRequires:  eigen3-static, flann-devel, cminpack-devel, vtk-devel, gl2ps-devel, hdf5-devel, python-devel, libxml2-devel, metslib-static, netcdf-cxx-devel, jsoncpp-devel
# optional
BuildRequires:  qhull-devel, libusb1-devel, gtest-devel, qtwebkit-devel, python-sphinx
%ifarch %{ix86} x86_64
BuildRequires:  openni-devel
%endif
BuildRequires:	libpcap-devel
BuildRequires:	boost-system >= 1.57, boost-filesystem >= 1.57, boost-thread >= 1.57, boost-date-time >= 1.57, boost-iostreams >= 1.57, boost-chrono >= 1.57

%description
The Point Cloud Library (or PCL) is a large scale, open project for point
cloud processing.

The PCL framework contains numerous state-of-the art algorithms including
filtering, feature estimation, surface reconstruction, registration, model
fitting and segmentation. 

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       eigen3-devel, qhull-devel, cminpack-devel, flann-devel, vtk-devel
%ifarch %{ix86} x86_64
Requires:       openni-devel
%endif

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        tools
Summary:        Point cloud tools and viewers
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description    tools
This package contains tools for point cloud file processing and viewers
for point cloud files and live Kinect data.


%package        doc
Summary:        PCL API documentation
Group:          Documentation
%if ! 0%{?rhel} || 0%{?rhel} >= 6
BuildArch:      noarch
%endif

%description    doc
The %{name}-doc package contains API documentation for the Point Cloud
Library.


%prep
%setup -qn %{name}-%{name}-%{version}
%patch0 -p1 -b .sse2
%patch1 -p0 -b .metslib
%patch2 -p0 -b .fedora
%patch3 -p0 -b .doxyfix
%patch4 -p1 -b .boost157
%patch5 -p0 -b .vtk
%patch6 -p0 -b .vtkincludepatch
# Just to make it obvious we're not using any of these
rm -fr recognition/include/pcl/recognition/3rdparty/metslib
rm -fr surface/src/3rdparty/opennurbs
rm -rf surface/include/pcl/surface/3rdparty/opennurbs

# Get rid of doxylink stuff (not in Fedora yet)
sed -i "s/, 'sphinxcontrib.doxylink.doxylink'//g" doc/advanced/content/conf.py doc/tutorials/content/conf.py

%build
mkdir build
pushd build
%cmake \
  -DWITH_DOCS=ON \
  -DWITH_TUTORIALS=ON \
  -DCMAKE_BUILD_TYPE=NONE \
  -DBUILD_apps=ON \
  -DBUILD_global_tests=OFF \
  -DOPENNI_INCLUDE_DIR:PATH=/usr/include/ni \
  -DLIB_INSTALL_DIR=%{_lib} \
%ifarch x86_64  %{?ix86}:
  -DPCL_ENABLE_SSE=ON \
%else
  -DPCL_ENABLE_SSE=OFF \
%endif
  -DPCL_PKGCONFIG_SUFFIX:STRING="" \
  -DBUILD_documentation=ON \
  -DCMAKE_SKIP_RPATH=ON \
  ..

# Don't use mflags, we're hitting out of memory errors on the koji builders
make
make doc tutorials advanced
popd

%install
pushd build
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool archives
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Just a dummy test
rm -f $RPM_BUILD_ROOT%{_bindir}/timed_trigger_test

# Remove installed documentation (will use %doc)
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc

# Rename the documentation folders from "html"
mv doc/doxygen/html doc/doxygen/api
mv doc/tutorials/html doc/tutorials/tutorials
mv doc/advanced/html doc/advanced/advanced

cp -fr ../doc/advanced/content/files/* doc/advanced/advanced
cp -fr ../doc/tutorials/content/sources doc/tutorials/tutorials
popd

for f in $RPM_BUILD_ROOT%{_bindir}/{openni_image,pcd_grabber_viewer,pcd_viewer,openni_viewer,oni_viewer}; do
	if [ -f $f ]; then
		mv $f $RPM_BUILD_ROOT%{_bindir}/pcl_$(basename $f)
	fi
done
rm $RPM_BUILD_ROOT%{_bindir}/{openni_fast_mesh,openni_ii_normal_estimation,openni_voxel_grid} ||:

mkdir -p $RPM_BUILD_ROOT%{_libdir}/cmake/pcl
mv $RPM_BUILD_ROOT%{_datadir}/%{name}-*/*.cmake $RPM_BUILD_ROOT%{_libdir}/cmake/pcl

#%check
#make -C build test || true

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS.txt LICENSE.txt
%{_libdir}/*.so.*
%{_datadir}/%{name}-%{apiversion}

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/pcl

%files tools
%{_bindir}/pcl_*
# There are no .desktop files because the GUI tools are rather examples
# to understand a particular feature of PCL.

%files doc
%doc build/doc/doxygen/api
%doc build/doc/tutorials/tutorials
%doc build/doc/advanced/advanced

%changelog
* Mon Jan 26 2015 Petr Machata <pmachata@redhat.com> - 1.7.2-3
- Rebuild for boost 1.57.0
- Pass -DBOOST_NEXT_PRIOR_HPP_INCLUDED to qt4-moc in apps/CMakeLists.txt
  (pcl-0ddf-boost157.patch)

* Mon Dec 29 2014 Rich Mattes <richmattes@gmail.com> - 1.7.2-2
- Fix pkgconfig to require libopenni (rhbz#1177244)
- Disable latex doxygen documentation

* Tue Dec 16 2014 Rich Mattes <richmattes@gmail.com> - 1.7.2-1
- Update to release 1.7.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Petr Machata <pmachata@redhat.com> - 1.7.1-3
- Rebuild for boost 1.55.0

* Fri Mar 21 2014 Rich Mattes <richmattes@gmail.com> - 1.7.1-2
- Rebuild for new eigen3
- Set PCL_ROOT to the CMAKE_INSTALL_PREFIX
- Fix usage of VTK_DEFINITIONS (rhbz#1079531)

* Sat Oct 26 2013 Rich Mattes <richmattes@gmail.com> - 1.7.1-1
- Update to release 1.7.1

* Sat Sep 14 2013 Rich Mattes <richmattes@gmail.com> - 1.7.0-4
- Add patch to remove openni-dev from pkgconfig files (rhbz#1007941)
- Add patch to generate pcl_geometry pkgconfig file again

* Sun Sep 08 2013 Rich Mattes <richmattes@gmail.com> - 1.7.0-3
- Fix hard-coded vtk library dependencies in PCLConfig.cmake

* Thu Aug 29 2013 Rich Mattes <richmattes@gmail.com> - 1.7.0-2
- Fix PCLConfig.cmake so PCL can discover itself

* Wed Aug 21 2013 Rich Mattes <richmattes@gmail.com> - 1.7.0-1
- Update to 1.7.0
- Update vtk 6 patch for 1.7.0

* Sat Jul 27 2013 pmachata@redhat.com - 1.6.0-7
- Rebuild for boost 1.54.0

* Fri Jul 12 2013 Orion Poplawski <orion@cora.nwra.com> - 1.6.0-6
- Rebuild for vtk 6.0.0
- Add patch for vtk 6 support

* Sat Jun 29 2013 Rich Mattes <richmattes@gmail.com> - 1.6.0-5
- Rebuild for new eigen3
- Change eigen3 BR to -static
- Add ARM support

* Fri Mar 08 2013 Karsten Hopp <karsten@redhat.com> 1.6.0-4
- more fixes for archs without openni

* Sun Feb 17 2013 Rich Mattes <richmattes@gmail.com> - 1.6.0-3
- Fixed bogus changelog dates
- Fixed build errors due to boost 1.53 and/or gcc 4.8

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.6.0-3
- Rebuild for Boost-1.53.0

* Tue Sep 25 2012 Rich Mattes <richmattes@gmail.com> - 1.6.0-2
- Disabled march=native flag in PCLConfig.cmake

* Mon Aug 06 2012 Rich Mattes <richmattes@gmail.com> - 1.6.0-1
- Update to release 1.6.0

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 25 2012 Rich Mattes <richmattes@gmail.com> - 1.5.1-3
- Rebuild for new vtk

* Thu Apr 19 2012 Tim Niemueller <tim@niemueller.de> - 1.5.1-2
- Pass proper LIB_INSTALL_DIR, install wrong cmake files otherwise

* Mon Apr 02 2012 Rich Mattes <richmattes@gmail.com> - 1.5.1-1
- Update to release 1.5.1
- Add new patch for gcc-4.7 fixes

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for c++ ABI breakage

* Mon Jan 16 2012 Rich Mattes <richmattes@gmail.com> - 1.4.0-1
- Update to release 1.4.0
- Add patch for gcc-4.7 fixes

* Mon Jan 16 2012 Tim Niemueller <tim@niemueller.de> - 1.3.1-5
- Update patch to fix PCLConfig.cmake

* Sat Jan 14 2012 Rich Mattes <richmattes@gmail.com> - 1.3.1-4
- Rebuild for gcc-4.7 and flann-1.7.1

* Sun Jan 08 2012 Dan Horák <dan[at]danny.cz> - 1.3.1-3
- openni is exclusive for x86

* Fri Dec 23 2011 Tim Niemueller <tim@niemueller.de> - 1.3.1-2
- Make sure documentation is not in main package

* Sun Dec 04 2011 Tim Niemueller <tim@niemueller.de> - 1.3.1-1
- Update to 1.3.1

* Tue Nov 22 2011 Tim Niemueller <tim@niemueller.de> - 1.3.0-1
- Update to 1.3.0

* Sat Oct 22 2011 Tim Niemueller <tim@niemueller.de> - 1.2.0-1
- Update to 1.2.0

* Tue Oct 04 2011 Tim Niemueller <tim@niemueller.de> - 1.1.1-2
- Change vtkWidgets to vtkRendering as import library flags to fix crash
  for binaries compiled with the installed PCL

* Tue Sep 20 2011 Tim Niemueller <tim@niemueller.de> - 1.1.1-1
- Update to 1.1.1

* Wed Jul 27 2011 Tim Niemueller <tim@niemueller.de> - 1.1.0-1
- Update to 1.1.0

* Wed Apr 06 2011 Tim Niemueller <tim@niemueller.de> - 1.0.0-0.1.svn366
- Initial package

