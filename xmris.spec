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
License: 	GPL
Group:		Games/Arcade
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
Buildrequires: X11-devel
#(nl) needed for rman
Buildrequires: xorg-x11 imake
URL:		http://www.cs.bris.ac.uk/~nathan/xmris

%description
Mr Is is a version of the Mr Do video arcade game for the X Window System.

%prep
%setup -q -n %{name}.%{version}
%patch -p1

%build
xmkmf -a
perl -p -i -e "s|XAPPLOADDIR = .*|XAPPLOADDIR = %{_datadir}/X11/app-defaults|" Makefile
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/X11R6
mkdir -p $RPM_BUILD_ROOT/var/lib/games/xmris
make install install.man DESTDIR=$RPM_BUILD_ROOT

# A link to ../../../etc/X11/app-defaults is made
APPDEF=%{buildroot}%{_libdir}/X11/app-defaults
if   [ -L $APPDEF ]; then rm    $APPDEF
elif [ -d $APPDEF ]; then rmdir $APPDEF
fi

mkdir -p $RPM_BUILD_ROOT/%{_mandir}

chmod 755 $RPM_BUILD_ROOT/var/lib/games/xmris

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
#rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root,755)
%doc COPYRIGHT CHANGES* README* COPYING-2.0 ChangeLog
%{_bindir}/xmris
%{_bindir}/xmred
%{_datadir}/X11/app-defaults/Xmris
%{_gamesdatadir}/%{name}/gardens
/var/lib/games/xmris
%{_mandir}/man1/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

