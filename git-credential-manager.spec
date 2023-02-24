#
# spec file for package git-credential-manager
#
# Copyright (c) 2023 Alec Su
#

Name:           git-credential-manager
Version:        2.0.931
Release:        0
Summary:        Secure, cross-platform Git credential storage
License:        MIT
URL:            https://github.com/GitCredentialManager/git-credential-manager
Source0:        https://github.com/GitCredentialManager/git-credential-manager/archive/refs/tags/v%{version}.tar.gz
Patch0:        add-arm64.patch
Patch1:        runtime-arm64.patch
Patch2:        install-buildoutput.patch
Requires:      git
%if 0%{?suse_version}
Requires:      libopenssl1_1
BuildRequires: libopenssl1_1
%else
Requires:      openssl-libs
BuildRequires: openssl-libs
%endif
%if 0%{?suse_version} && 0%{?suse_version} <= 1500
Requires:      libicu69
BuildRequires: libicu69
%else
Requires:      libicu
BuildRequires: libicu
%endif
BuildRequires: dotnet-sdk-6.0
BuildRequires: which
ExclusiveArch: aarch64 x86_64

%description
Cross Platform Git Credential Manager command line utility.
GCM supports authentication with a number of Git hosting providers
including GitHub, BitBucket, and Azure DevOps.
For more information see https://aka.ms/gcm

%prep
%setup -q

%ifarch aarch64
%patch0 -p1
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

