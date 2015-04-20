Summary:	Extensible library solution for reading and writing National Imagery Transmission Format (NITF)
Name:		nitro
Version:	2.7
Release:	2%{?dist}
License:	GPL and GLPLv2
Source:		nitro-2.7.tar.bz2
URL:		https://github.com/hobu/nitro
BuildRequires:	cmake

%description
Nitro is a library that provides NITF support for PDAL to write LAS-in-NITF
files for writers.nitf.

%prep
%setup -q

%build
%cmake	-D STATIC_BUILD:BOOL=OFF \
	-D BUILD_SHARED_LIBS:BOOL=ON \
	-D NITRO_LIB_SUBDIR=%{_libdir} .

make %{?_smp_mflags}

%install
make install/fast DESTDIR=%{buildroot}

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files
%doc README.md
%license COPYING COPYING.LESSER
%{_includedir}/nitro/
%{_libdir}/libnitf-c.so
%{_libdir}/libnitf-cpp.so
%{_usr}/pkgconfig/libnitf.pc

%changelog
* Mon Apr 20 2015 Devrim Gündüz <devrim@gunduz.org> 2.7.0-2
- Various updates:
 - Own directories in main package
 - omit deprecated Group: tags and %%clean section
 - Use better macros for make and cmake
 - have %%build section envoke 'make'
 - Update %%install section
 - Improve cmake build parameters
 - Use %%license macro
 - Get rid of BuildRoot definition
 - No need to cleanup buildroot during %%install
 - Remove %%defattr
 - Run ldconfig
 - Update license

* Tue Jan 13 2015 Devrim Gündüz <devrim@gunduz.org> 2.7.0-1
- Initial packaging

