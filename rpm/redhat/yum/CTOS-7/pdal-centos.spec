Name:		pdal-centos
Version:	1.0
Release:	1
Summary:	PDAL RPMs for CentOS - Yum Repository Configuration
Group:		System Environment/Base
License:	BSD
URL:		http://fmach.postgres.club
Source0:	http://fmach.postgres.club/RPM-GPG-KEY-PDAL
Source2:	pdal-centos.repo
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	centos-release

%description
This package contains yum configuration for CentOS, and also the GPG
key for PDAL RPMs.

%prep
%setup -q  -c -T

%build

%install
rm -rf %{buildroot}

install -Dpm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PDAL

install -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE2}  \
	%{buildroot}%{_sysconfdir}/yum.repos.d/

%clean
rm -rf %{buildroot}

%post 
/bin/rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PDAL

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Thu Mar 5 2015 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial version.
