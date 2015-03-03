Name:           ogdi
Version:        3.2.0
Release:        0.20.beta2%{?dist}
Summary:        Open Geographic Datastore Interface
Group:          Applications/Engineering
License:        BSD
URL:            http://ogdi.sourceforge.net/
Source0:	http://netcologne.dl.sourceforge.net/project/ogdi/ogdi/3.2.0beta2/ogdi-3.2.0.beta2.tar.gz
#Source0:        http://dl.sourceforge.net/ogdi/%{name}-%{version}.beta2.tar.gz
Source1:        http://ogdi.sourceforge.net/ogdi.pdf
Patch0:         ogdi-3.2.0.beta2-projfix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-root-%(id -u -n)

BuildRequires:  unixODBC-devel zlib-devel 
BuildRequires:  expat-devel proj-devel tcl-devel 

%description
OGDI is the Open Geographic Datastore Interface. OGDI is an
application programming interface (API) that uses a standardized
access methods to work in conjunction with GIS software packages (the
application) and various geospatial data products. OGDI uses a
client/server architecture to facilitate the dissemination of
geospatial data products over any TCP/IP network, and a
driver-oriented approach to facilitate access to several geospatial
data products/formats.

%package devel
Summary:        OGDI header files and documentation
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       zlib-devel expat-devel proj-devel

%description devel
OGDI header files and developer's documentation.

%package odbc
Summary:        ODBC driver for OGDI
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description odbc
ODBC driver for OGDI.

%package tcl
Summary:        TCL wrapper for OGDI
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description tcl
TCL wrapper for OGDI.

%prep
%setup -q -n %{name}-%{version}.beta2
%patch0 -p1 -b .projfix

# include documentation
cp -p %{SOURCE1} .

%build

TOPDIR=`pwd`; TARGET=Linux; export TOPDIR TARGET
INST_LIB=%{_libdir}/;export INST_LIB
export CFG=debug # for -g

# do not compile with ssp. it will trigger internal bugs (to_fix_upstream)
OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//g'`
export CFLAGS="$OPT_FLAGS -fPIC -DPIC -DDONT_TD_VOID -DUSE_TERMIO" 
%configure \
        --with-binconfigs \
        --with-expat \
        --with-proj \
        --with-zlib 

# WARNING !!!
# using %{?_smp_mflags} may break build
make 

# build tcl interface
make -C ogdi/tcl_interface \
          TCL_LINKLIB="-ltcl"

# build contributions
make -C contrib/gdal

# build odbc drivers
ODBC_LINKLIB="-lodbc"
make -C ogdi/attr_driver/odbc \
          ODBC_LINKLIB="-lodbc"

%install
rm -rf %{buildroot}

# export env
TOPDIR=`pwd`; TARGET=Linux; export TOPDIR TARGET

make install \
        INST_INCLUDE=%{buildroot}%{_includedir}/%{name} \
        INST_LIB=%{buildroot}%{_libdir} \
        INST_BIN=%{buildroot}%{_bindir}

# install plugins olso
make install -C ogdi/tcl_interface \
        INST_LIB=%{buildroot}%{_libdir}
make install -C contrib/gdal \
        INST_LIB=%{buildroot}%{_libdir}
make install -C ogdi/attr_driver/odbc \
        INST_LIB=%{buildroot}%{_libdir}

# remove example binary
rm %{buildroot}%{_bindir}/example?

# we have multilib ogdi-config
%if "%{_lib}" == "lib"
%define cpuarch 32
%else
%define cpuarch 64
%endif

# fix file(s) for multilib issue
touch -r ogdi-config.in ogdi-config

# install pkgconfig file and ogdi-config
mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -p -m 644 ogdi.pc %{buildroot}%{_libdir}/pkgconfig/
install -p -m 755 ogdi-config %{buildroot}%{_bindir}/ogdi-config-%{cpuarch}
# ogdi-config wrapper for multiarch
cat > %{buildroot}%{_bindir}/%{name}-config <<EOF
#!/bin/bash

ARCH=\$(uname -m)
case \$ARCH in
x86_64 | ppc64 | ia64 | s390x | sparc64 | alpha | alphaev6 )
ogdi-config-64 \${*}
;;
*)
ogdi-config-32 \${*}
;;
esac
EOF
chmod 755 %{buildroot}%{_bindir}/%{name}-config
touch -r ogdi-config.in %{buildroot}%{_bindir}/%{name}-config

%clean
rm -rf %{buildroot}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE NEWS ChangeLog README
%{_bindir}/gltpd
%{_bindir}/ogdi_*
%{_libdir}/libogdi.so.*
%dir %{_libdir}/ogdi
%exclude %{_libdir}/%{name}/liblodbc.so
%exclude %{_libdir}/%{name}/libecs_tcl.so
%{_libdir}/%{name}/lib*.so

%files devel
%defattr(-,root,root,-)
%doc ogdi.pdf
%doc ogdi/examples/example1/example1.c
%doc ogdi/examples/example2/example2.c
%{_bindir}/%{name}-config
%{_bindir}/%{name}-config-%{cpuarch}
%{_libdir}/pkgconfig/%{name}.pc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/libogdi.so

%files odbc
%defattr(-,root,root,-)
%{_libdir}/%{name}/liblodbc.so

%files tcl
%defattr(-,root,root,-)
%{_libdir}/%{name}/libecs_tcl.so

%changelog
* Tue Mar 3 2015 Devrim Gündüz <devrim@gunduz.org> - 3.2.0-0.20.beta2
- Initial packaging for Fmach repo, based on Fedora spec file.
