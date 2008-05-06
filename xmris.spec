%define name	xmris
%define version 4.0.5
%define release %mkrel 5

Name:		%{name}
Summary:	A version of 'Mr Do' video game for X
Version: 	%{version}
Release:	%{release}
Source0:	http://www.cs.bris.ac.uk/~nathan/xmris/%{name}.%{version}.tar.bz2
Source10:	%{name}.16.png
Source11:	%{name}.32.png
Source12:	%{name}.48.png
Patch0:		xmris-config.patch.bz2
Patch1:		xmris-scoring.patch
Patch2:		xmris-signal-handling.patch
Patch3:		xmris-wm-protocol.patch
License: 	GPL
Group:		Games/Arcade
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
Buildrequires:	libxt-devel imake
URL:		http://www.cs.bris.ac.uk/~nathan/xmris

%description
Mr Is is a version of the Mr Do video arcade game for the X Window System.

%prep
%setup -q -n %{name}.%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
xmkmf -a
perl -p -i -e "s|XAPPLOADDIR = .*|XAPPLOADDIR = %{_datadir}/X11/app-defaults|" Makefile
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p  $RPM_BUILD_ROOT/var/lib/games/xmris
cat > $RPM_BUILD_ROOT/var/lib/games/xmris/xmris.scores << EOF
+0
+8182
EOF
make install install.man DESTDIR=$RPM_BUILD_ROOT

# A link to ../../../etc/X11/app-defaults is made and named lib in x86_64
APPDEF=%{buildroot}/usr/lib/X11/app-defaults
if   [ -L $APPDEF ]; then rm    $APPDEF
elif [ -d $APPDEF ]; then rmdir $APPDEF
fi

mkdir -p $RPM_BUILD_ROOT/%{_mandir}

# menu
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
mkdir -p $RPM_BUILD_ROOT%{_miconsdir}
mkdir -p $RPM_BUILD_ROOT%{_liconsdir}
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%name.desktop
[Desktop Entry]
Type=Application
Categories=Game;ArcadeGame;
Name=XMrIs
Comment=Mr. Is, a Mr. Do clone for X
Exec=%{_bindir}/xmrisIcon=xmris
EOF
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m 644 %{SOURCE11} $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m 644 %{SOURCE12} $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%post
%{update_menus}

%postun
%{clean_menus}

%clean
chmod 755 $RPM_BUILD_ROOT/var/lib/games/xmris
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, games, 755)
%doc COPYRIGHT CHANGES* README* COPYING-2.0 ChangeLog
%{_gamesbindir}/xmred
%attr(2755, root, games) %{_gamesbindir}/xmris
%{_datadir}/X11/app-defaults/Xmris
%{_gamesdatadir}/%{name}/gardens
%{_mandir}/man1/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%defattr(-, games, games,2575)
%dir %{_localstatedir}/games/xmris
%defattr(-, games, games,464)
%{_localstatedir}/games/xmris/xmris.scores
