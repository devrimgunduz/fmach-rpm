Name:		pdal-fedora
Version:	1.0
Release:	1
Summary:	PDAL RPMs for Fedora - Yum Repository Configuration
Group:		System Environment/Base
License:	BSD
URL:		http://pdal.s3-website-us-east-1.amazonaws.com/rpms/
Source0:	http://pdal.s3-website-us-east-1.amazonaws.com/rpms/RPM-GPG-KEY-PDAL
Source2:	pdal-fedora.repo
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	fedora-release

%description
This package contains yum configuration for Fedora, and also the GPG
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

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Thu Mar 5 2015 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial version.
