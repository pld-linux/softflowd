Summary:	Network traffic analyser capable of Cisco NetFlow data export
Name:		softflowd
Version:	0.9.8
Release:	0.1
License:	BSD
Group:		Applications/Networking
Source0:	http://www.mindrot.org/files/softflowd/%{name}-%{version}.tar.gz
# Source0-md5:	0054d1c80494396cc15edb0a1c7748b1
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.mindrot.org/projects/softflowd/
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
softflowd is a software implementation of a flow-based network traffic
monitor. softflowd reads network traffic and gathers information about
active traffic flows. A "traffic flow" is communication between two IP
addresses or (if the overlying protocol is TCP or UDP) address/port
tuples. The intended use of softflowd is as a software implementation
of Cisco's NetFlow traffic account system. softflowd supports data
export using versions 1, 5 or 9 of the NetFlow protocol.

%prep
%setup -q
%build
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/softflowd
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/softflowd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog README TODO

%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*

%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
