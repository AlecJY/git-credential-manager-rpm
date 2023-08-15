#
# spec file for package git-credential-manager
#
# Copyright (c) 2023 Alec Su
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

%global debug_package     %{nil}
%global _build_id_links   none
%global __os_install_post %{nil}

Name:           git-credential-manager
Version:        2.3.1
Release:        0
Summary:        Secure, cross-platform Git credential storage
License:        MIT
URL:            https://github.com/git-ecosystem/git-credential-manager
Source0:        https://github.com/git-ecosystem/git-credential-manager/archive/refs/tags/v%{version}.tar.gz
Patch0:         linux-only.patch
Patch1:         runtime-arm64.patch
Patch2:         install-buildoutput.patch
Requires:       git
%if 0%{?suse_version}
Requires:       libopenssl1_1
BuildRequires:  libopenssl1_1
%else
Requires:       openssl-libs
BuildRequires:  openssl-libs
%endif
%if 0%{?suse_version} && 0%{?suse_version} <= 1500
Requires:       libicu69
BuildRequires:  libicu69
%else
Requires:       libicu
BuildRequires:  libicu
%endif
BuildRequires:  dotnet-sdk-7.0
BuildRequires:  which
ExclusiveArch:  aarch64 x86_64

%description
Cross Platform Git Credential Manager command line utility.
GCM supports authentication with a number of Git hosting providers
including GitHub, BitBucket, and Azure DevOps.
For more information see https://aka.ms/gcm

%prep
%setup -q

%patch0 -p1

%ifarch aarch64
%patch1 -p1
%endif

%patch2 -p1

%build
dotnet restore
dotnet build Git-Credential-Manager.sln -c LinuxRelease

%install
%{__mkdir} -p %{buildroot}%{_libdir}
%{__cp} -r ./buildoutput/share/gcm-core/ %{buildroot}%{_libdir}
%{__mkdir} -p %{buildroot}%{_bindir}
%{__ln_s} -f %{_libdir}/gcm-core/git-credential-manager %{buildroot}%{_bindir}/git-credential-manager
%{__ln_s} -f %{_libdir}/gcm-core/git-credential-manager %{buildroot}%{_bindir}/git-credential-manager-core

%files
%{_bindir}/git-credential-manager
%{_bindir}/git-credential-manager-core
%{_libdir}/gcm-core/
%license LICENSE

%changelog

