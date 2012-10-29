Summary:	GObject and GUI library for high level crypto parsing and display
Name:		gcr
Version:	3.6.1
Release:	1
License:	LGPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gcr/3.6/%{name}-%{version}.tar.xz
# Source0-md5:	44f54b95d12caaf65139b84df418ea96
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gnupg
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+3-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libgcrypt-devel
BuildRequires:	libtasn1-devel
BuildRequires:	libtool
BuildRequires:	p11-kit-devel
BuildRequires:	pkg-config
Requires:	%{name}-libs = %{version}-%{release}
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	gtk+-update-icon-cache
Requires(post,postun):	shared-mime-info
Requires(post,postun):	desktop-file-utils
Requires:	gnupg
Requires:	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/gcr-3

%description
gcr is a library for displaying certificates, and crypto UI, accessing
key stores. It also provides a viewer for crypto files on the GNOME
desktop.
gck is a library for accessing PKCS#11 modules like smart cards.

%package libs
Summary:	gcr and gck libraries
Group:		Libraries

%description libs
This package provides gcr and gck libraries.

%package devel
Summary:	Header files for gcr and gck libraries
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for gcr and gck libraries.

%package apidocs
Summary:	gcr and gck API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
API and gck documentation for gcr library.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I build/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static		\
	--disable-update-mime		\
	--disable-update-icon-cache	\
	--disable-silent-rules		\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmock-test-module.*

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_gsettings_cache
%update_icon_cache hicolor
%update_mime_database
%update_desktop_database

%postun
%update_gsettings_cache
%update_icon_cache hicolor
%update_mime_database
%update_desktop_database

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README
%dir %{_libexecdir}
%attr(755,root,root) %{_bindir}/gcr-viewer
%attr(755,root,root) %{_libexecdir}/gcr-prompter
%{_datadir}/GConf/gsettings/org.gnome.crypto.pgp.convert
%{_datadir}/GConf/gsettings/org.gnome.crypto.pgp_keyservers.convert
%{_datadir}/dbus-1/services/org.gnome.keyring.PrivatePrompter.service
%{_datadir}/dbus-1/services/org.gnome.keyring.SystemPrompter.service
%{_datadir}/gcr-3
%{_datadir}/glib-2.0/schemas/org.gnome.crypto.pgp.gschema.xml
%{_datadir}/mime/packages/gcr-crypto-types.xml

%{_desktopdir}/gcr-prompter.desktop
%{_desktopdir}/gcr-viewer.desktop
%{_iconsdir}/hicolor/*/*/*.png

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libgck-1.so.?
%attr(755,root,root) %ghost %{_libdir}/libgcr-3.so.?
%attr(755,root,root) %ghost %{_libdir}/libgcr-base-3.so.?
%attr(755,root,root) %{_libdir}/libgck-1.so.*.*.*
%attr(755,root,root) %{_libdir}/libgcr-3.so.*.*.*
%attr(755,root,root) %{_libdir}/libgcr-base-3.so.*.*.*
%{_libdir}/girepository-1.0/Gck-1.typelib
%{_libdir}/girepository-1.0/Gcr-3.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_datadir}/gir-1.0/Gck-1.gir
%{_datadir}/gir-1.0/Gcr-3.gir
%{_includedir}/gck-1
%{_includedir}/gcr-3
%{_pkgconfigdir}/*.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gck
%{_gtkdocdir}/gcr-3

