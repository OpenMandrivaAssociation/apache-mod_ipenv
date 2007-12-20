#Module-Specific definitions
%define mod_name mod_ipenv
%define mod_conf A92_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Mod_ipenv is a DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	1.0.2
Release:	%mkrel 4
Group:		System/Servers
License:	GPL
URL:		http://mod-ipenv.sourceforge.net/
Source0:	http://ovh.dl.sourceforge.net/sourceforge/mod-ipenv/mod-ipenv-%{version}.tar.bz2
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
ipenv is the module to set/unset environment variables based on client IP
addresses or client hostnames.

This is useful for these purposes.
 -access controls based on IP addresses and host names
  by corporating with mod_access(mod_authz_host for apache 2.2 or later).
 -URL rewritings based on IP addressed and host names
  by corporating with mod_rewrite.

%prep

%setup -q -n mod-ipenv-%{version}

cp %{SOURCE1} %{mod_conf}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_sbindir}/apxs -c %{mod_name}.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc sample CHANGES LICENCE README README.jp
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
