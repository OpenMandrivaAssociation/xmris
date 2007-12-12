%define name	xmris
%define version 4.0.5
%define release %mkrel 4

Name:		%{name}
Summary:	A version of 'Mr Do' video game for X
Version: 	%{version}
Release:	%{release}
Source0:	http://www.cs.bris.ac.uk/~nathan/xmris/%{name}.%{version}.tar.bz2
Source10:	%{name}.16.png
Source11:	%{name}.32.png
Source12:	%{name}.48.png
Patch0:		xmris-config.patch.bz2
License: 	GPL
Group:		Games/Arcade
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
Buildrequires: XFree86-devel
#(nl) needed for rman
Buildrequires: xorg-x11
URL:		http://www.cs.bris.ac.uk/~nathan/xmris

%description
Mr Is is a version of the Mr Do video arcade game for the X Window System.

%prep
%setup -q -n %{name}.%{version}
%patch -p1

%build
xmkmf -a
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/X11R6
mkdir -p $RPM_BUILD_ROOT/var/lib/games/xmris
make install install.man DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT/usr/X11R6/* $RPM_BUILD_ROOT/%{_prefix}/
mkdir -p $RPM_BUILD_ROOT/%{_mandir}
mv $RPM_BUILD_ROOT/%{_prefix}/man/* $RPM_BUILD_ROOT/%{_mandir}

rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/xmsit.*
chmod 755 $RPM_BUILD_ROOT/var/lib/games/xmris

# menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
mkdir -p $RPM_BUILD_ROOT%{_miconsdir}
mkdir -p $RPM_BUILD_ROOT%{_liconsdir}
cat << EOF > $RPM_BUILD_ROOT/%_menudir/%name
?package(xmris): \
	needs="X11"\
	section="Amusement/Arcade"\
	title="XMrIs"\
	longtitle="Mr. Is, a Mr. Do clone for X"\
	command="%{_bindir}/xmris"\
	icon="xmris.png"
EOF
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m 644 %{SOURCE11} $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m 644 %{SOURCE12} $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%post
%{update_menus}

%postun
%{clean_menus}

%clean
#rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root,755)
%doc COPYRIGHT CHANGES* README* COPYING-2.0 ChangeLog
%{_bindir}/xmris
%{_bindir}/xmred
%config(noreplace) %{_sysconfdir}/X11/app-defaults/Xmris
%config(noreplace) %{_sysconfdir}/X11/app-defaults/xmris
%{_libdir}/X11/app-defaults
%{_libdir}/X11/doc/html/xmred.1.html
%{_libdir}/X11/doc/html/xmris.1.html
%{_libdir}/X11/doc/html/xmsit.1.html
/var/lib/games/xmris


%{_mandir}/man1/*
%{_menudir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

