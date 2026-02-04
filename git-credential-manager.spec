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

%global dotnet_version    8.0.403

Name:           git-credential-manager
Version:        2.7.2
Release:        0
Summary:        Secure, cross-platform Git credential storage
License:        MIT
URL:            https://github.com/git-ecosystem/git-credential-manager
Source0:        https://github.com/git-ecosystem/git-credential-manager/archive/refs/tags/v%{version}.tar.gz
# Prebuilt dotnet binary from https://dotnet.microsoft.com/en-us/download/dotnet/8.0
Source1:        dotnet-sdk-%{dotnet_version}-linux-arm64.tar.gz
Source2:        dotnet-sdk-%{dotnet_version}-linux-x64.tar.gz
# Pre-downloaded NuGet dependencies
Source3:        nuget-packages.tar.gz
Patch0:         linux-only.patch
Patch1:         install-buildoutput.patch
Requires:       git
%if 0%{?suse_version}
Requires:       libopenssl3
BuildRequires:  libopenssl3
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
BuildRequires:  which
ExclusiveArch:  aarch64 x86_64

%description
Cross Platform Git Credential Manager command line utility.
GCM supports authentication with a number of Git hosting providers
including GitHub, BitBucket, and Azure DevOps.
For more information see https://aka.ms/gcm

%prep
%ifarch aarch64
%setup -q -a 1 -a 3
%elifarch x86_64
%setup -q -a 2 -a 3
%endif

%patch -P0 -p1
%patch -P1 -p1

%build
PATH=$PATH:${PWD}
dotnet restore --packages ./packages
dotnet build Git-Credential-Manager.sln -c LinuxRelease --source ./packages

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

